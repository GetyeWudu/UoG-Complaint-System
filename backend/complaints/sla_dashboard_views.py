"""
SLA Dashboard and Breach Monitoring Views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Q, Count, Avg, F
from datetime import timedelta, datetime
from .models import Complaint, SLAConfiguration
from .sla_service import check_and_update_sla_breaches, auto_escalate_breached_complaints


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sla_dashboard(request):
    """
    Get comprehensive SLA dashboard data
    """
    now = timezone.now()
    
    # Update SLA breaches first
    breached_complaints = check_and_update_sla_breaches()
    
    # Get all active complaints
    active_complaints = Complaint.objects.filter(
        status__in=['new', 'assigned', 'in_progress', 'pending']
    )
    
    # SLA Breach Statistics
    response_breaches = active_complaints.filter(sla_response_breached=True).count()
    resolution_breaches = active_complaints.filter(sla_resolution_breached=True).count()
    
    # Complaints at risk (80% of SLA time used)
    at_risk_complaints = []
    for complaint in active_complaints:
        if complaint.sla_response_hours and not complaint.first_response_at:
            hours_elapsed = (now - complaint.created_at).total_seconds() / 3600
            risk_percentage = (hours_elapsed / complaint.sla_response_hours) * 100
            if risk_percentage >= 80 and risk_percentage < 100:
                at_risk_complaints.append({
                    'id': complaint.id,
                    'tracking_id': complaint.tracking_id,
                    'title': complaint.title,
                    'risk_percentage': round(risk_percentage, 1),
                    'hours_remaining': complaint.sla_response_hours - hours_elapsed,
                    'type': 'response'
                })
        
        if complaint.sla_resolution_hours and complaint.status not in ['resolved', 'closed']:
            hours_elapsed = (now - complaint.created_at).total_seconds() / 3600
            risk_percentage = (hours_elapsed / complaint.sla_resolution_hours) * 100
            if risk_percentage >= 80 and risk_percentage < 100:
                at_risk_complaints.append({
                    'id': complaint.id,
                    'tracking_id': complaint.tracking_id,
                    'title': complaint.title,
                    'risk_percentage': round(risk_percentage, 1),
                    'hours_remaining': complaint.sla_resolution_hours - hours_elapsed,
                    'type': 'resolution'
                })
    
    # Recent breaches (last 24 hours)
    recent_breaches = Complaint.objects.filter(
        Q(sla_response_breached=True) | Q(sla_resolution_breached=True),
        sla_breach_notified_at__gte=now - timedelta(hours=24)
    ).values(
        'id', 'tracking_id', 'title', 'priority', 'category__name',
        'sla_response_breached', 'sla_resolution_breached', 'created_at'
    )
    
    # SLA Performance by Category
    category_performance = Complaint.objects.filter(
        created_at__gte=now - timedelta(days=30)
    ).values('category__name').annotate(
        total_complaints=Count('id'),
        response_breaches=Count('id', filter=Q(sla_response_breached=True)),
        resolution_breaches=Count('id', filter=Q(sla_resolution_breached=True)),
        avg_response_time=Avg(
            F('first_response_at') - F('created_at'),
            filter=Q(first_response_at__isnull=False)
        ),
        avg_resolution_time=Avg(
            F('resolved_at') - F('created_at'),
            filter=Q(resolved_at__isnull=False)
        )
    )
    
    # Escalation Statistics
    escalated_complaints = Complaint.objects.filter(escalated=True)
    escalation_stats = {
        'total_escalated': escalated_complaints.count(),
        'auto_escalated': escalated_complaints.filter(escalation_reason__icontains='automatic').count(),
        'manual_escalated': escalated_complaints.exclude(escalation_reason__icontains='automatic').count(),
        'by_level': escalated_complaints.values('escalation_level').annotate(count=Count('id'))
    }
    
    return Response({
        'summary': {
            'total_active_complaints': active_complaints.count(),
            'response_breaches': response_breaches,
            'resolution_breaches': resolution_breaches,
            'at_risk_count': len(at_risk_complaints),
            'recent_breaches_24h': len(recent_breaches)
        },
        'at_risk_complaints': at_risk_complaints[:10],  # Top 10 most at risk
        'recent_breaches': list(recent_breaches)[:20],  # Last 20 breaches
        'category_performance': list(category_performance),
        'escalation_stats': escalation_stats,
        'last_updated': now.isoformat()
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def manual_escalate_complaint(request, complaint_id):
    """
    Manually escalate a specific complaint
    """
    try:
        complaint = Complaint.objects.get(id=complaint_id)
        reason = request.data.get('reason', 'Manual escalation')
        target_level = request.data.get('target_level')
        
        from .sla_service import escalate_complaint
        escalated_to = escalate_complaint(
            complaint, 
            escalated_by=request.user, 
            reason=reason,
            target_level=target_level
        )
        
        if escalated_to:
            return Response({
                'success': True,
                'message': f'Complaint escalated to {escalated_to.get_full_name()}',
                'escalated_to': escalated_to.get_full_name(),
                'escalation_level': complaint.escalation_level
            })
        else:
            return Response({
                'success': False,
                'message': 'No suitable escalation target found'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Complaint.DoesNotExist:
        return Response({
            'error': 'Complaint not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_sla_check(request):
    """
    Manually trigger SLA breach check and auto-escalation
    """
    if not request.user.role in ['admin', 'super_admin']:
        return Response({
            'error': 'Permission denied'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Run SLA checks
    breached_complaints = check_and_update_sla_breaches()
    escalated_count = auto_escalate_breached_complaints()
    
    return Response({
        'success': True,
        'breaches_detected': len(breached_complaints),
        'auto_escalated': escalated_count,
        'message': f'SLA check complete. {len(breached_complaints)} breaches detected, {escalated_count} complaints auto-escalated.'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sla_breach_alerts(request):
    """
    Get real-time SLA breach alerts for current user
    """
    user = request.user
    now = timezone.now()
    
    # Get complaints assigned to user that are at risk or breached
    user_complaints = Complaint.objects.filter(
        assigned_to=user,
        status__in=['assigned', 'in_progress', 'pending']
    )
    
    alerts = []
    
    for complaint in user_complaints:
        # Check response SLA
        if not complaint.first_response_at and complaint.sla_response_hours:
            hours_elapsed = (now - complaint.created_at).total_seconds() / 3600
            
            if complaint.sla_response_breached:
                alerts.append({
                    'type': 'breach',
                    'sla_type': 'response',
                    'complaint_id': complaint.id,
                    'tracking_id': complaint.tracking_id,
                    'title': complaint.title,
                    'priority': complaint.priority,
                    'hours_overdue': hours_elapsed - complaint.sla_response_hours,
                    'message': f'Response SLA breached by {hours_elapsed - complaint.sla_response_hours:.1f} hours'
                })
            elif hours_elapsed >= complaint.sla_response_hours * 0.8:  # 80% threshold
                alerts.append({
                    'type': 'warning',
                    'sla_type': 'response',
                    'complaint_id': complaint.id,
                    'tracking_id': complaint.tracking_id,
                    'title': complaint.title,
                    'priority': complaint.priority,
                    'hours_remaining': complaint.sla_response_hours - hours_elapsed,
                    'message': f'Response due in {complaint.sla_response_hours - hours_elapsed:.1f} hours'
                })
        
        # Check resolution SLA
        if complaint.status not in ['resolved', 'closed'] and complaint.sla_resolution_hours:
            hours_elapsed = (now - complaint.created_at).total_seconds() / 3600
            
            if complaint.sla_resolution_breached:
                alerts.append({
                    'type': 'breach',
                    'sla_type': 'resolution',
                    'complaint_id': complaint.id,
                    'tracking_id': complaint.tracking_id,
                    'title': complaint.title,
                    'priority': complaint.priority,
                    'hours_overdue': hours_elapsed - complaint.sla_resolution_hours,
                    'message': f'Resolution SLA breached by {hours_elapsed - complaint.sla_resolution_hours:.1f} hours'
                })
            elif hours_elapsed >= complaint.sla_resolution_hours * 0.8:  # 80% threshold
                alerts.append({
                    'type': 'warning',
                    'sla_type': 'resolution',
                    'complaint_id': complaint.id,
                    'tracking_id': complaint.tracking_id,
                    'title': complaint.title,
                    'priority': complaint.priority,
                    'hours_remaining': complaint.sla_resolution_hours - hours_elapsed,
                    'message': f'Resolution due in {complaint.sla_resolution_hours - hours_elapsed:.1f} hours'
                })
    
    # Sort by urgency (breaches first, then by time remaining)
    alerts.sort(key=lambda x: (
        0 if x['type'] == 'breach' else 1,
        x.get('hours_overdue', 0) if x['type'] == 'breach' else -x.get('hours_remaining', 0)
    ))
    
    return Response({
        'alerts': alerts,
        'breach_count': len([a for a in alerts if a['type'] == 'breach']),
        'warning_count': len([a for a in alerts if a['type'] == 'warning']),
        'last_updated': now.isoformat()
    })