"""
SLA tracking and automatic escalation service
"""
from .models import Complaint, SLAConfiguration, ComplaintEvent
from accounts.models import CustomUser
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta


def get_sla_for_complaint(complaint):
    """
    Get SLA configuration for a complaint based on priority, category, and campus.
    Returns: SLAConfiguration or None
    """
    if not complaint:
        return None
    
    # Try to find specific SLA config
    sla = SLAConfiguration.objects.filter(
        priority=complaint.priority,
        is_active=True
    )
    
    # Filter by category if available
    if complaint.category:
        sla = sla.filter(
            Q(category=complaint.category) | Q(category__isnull=True)
        )
    
    # Filter by campus if available
    if complaint.campus:
        sla = sla.filter(
            Q(campus=complaint.campus) | Q(campus__isnull=True)
        )
    
    # Order by specificity (category/campus specific first)
    # Use Case/When for ordering by null fields
    from django.db.models import Case, When, Value, IntegerField
    
    sla = sla.annotate(
        category_priority=Case(
            When(category__isnull=False, then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        ),
        campus_priority=Case(
            When(campus__isnull=False, then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        )
    ).order_by('-category_priority', '-campus_priority').first()
    
    return sla


def apply_sla_to_complaint(complaint):
    """
    Apply SLA configuration to a complaint.
    Updates complaint with SLA times.
    """
    if not complaint:
        return
    
    sla = get_sla_for_complaint(complaint)
    
    if sla:
        complaint.sla_response_hours = sla.response_time_hours
        complaint.sla_resolution_hours = sla.resolution_time_hours
        complaint.save()
        
        return sla
    
    # Default SLA if no configuration found
    default_slas = {
        'critical': {'response': 2, 'resolution': 24},
        'high': {'response': 8, 'resolution': 72},
        'medium': {'response': 24, 'resolution': 168},  # 7 days
        'low': {'response': 72, 'resolution': 720},  # 30 days
    }
    
    priority = complaint.priority or 'medium'
    defaults = default_slas.get(priority, default_slas['medium'])
    
    complaint.sla_response_hours = defaults['response']
    complaint.sla_resolution_hours = defaults['resolution']
    complaint.save()
    
    return None


def check_and_update_sla_breaches():
    """
    Check all open complaints for SLA breaches and update flags.
    This should be called periodically (e.g., via cron job).
    Returns: list of breached complaints
    """
    now = timezone.now()
    breached_complaints = []
    
    # Get all open complaints
    open_complaints = Complaint.objects.filter(
        status__in=['new', 'assigned', 'in_progress', 'pending']
    )
    
    for complaint in open_complaints:
        # Ensure SLA is set
        if not complaint.sla_response_hours or not complaint.sla_resolution_hours:
            apply_sla_to_complaint(complaint)
        
        breach_detected = False
        
        # Check response SLA
        if not complaint.first_response_at:
            hours_since_creation = (now - complaint.created_at).total_seconds() / 3600
            if hours_since_creation > complaint.sla_response_hours:
                if not complaint.sla_response_breached:
                    complaint.sla_response_breached = True
                    breach_detected = True
                    
                    # Create event
                    ComplaintEvent.objects.create(
                        complaint=complaint,
                        event_type='sla_breached',
                        notes=f"Response SLA breached ({complaint.sla_response_hours}h)"
                    )
        
        # Check resolution SLA
        if complaint.status not in ['resolved', 'closed']:
            hours_since_creation = (now - complaint.created_at).total_seconds() / 3600
            if hours_since_creation > complaint.sla_resolution_hours:
                if not complaint.sla_resolution_breached:
                    complaint.sla_resolution_breached = True
                    breach_detected = True
                    
                    # Create event
                    ComplaintEvent.objects.create(
                        complaint=complaint,
                        event_type='sla_breached',
                        notes=f"Resolution SLA breached ({complaint.sla_resolution_hours}h)"
                    )
        
        if breach_detected:
            complaint.sla_breach_notified_at = now
            complaint.save()
            breached_complaints.append(complaint)
    
    return breached_complaints


def escalate_complaint(complaint, escalated_by, reason='', target_level=None):
    """
    Escalate a complaint to the next level.
    
    Escalation levels:
    0 = None
    1 = Department Head
    2 = Dean
    3 = Campus Director
    4 = Admin
    """
    if not complaint:
        return None
    
    # Determine escalation level
    if target_level is None:
        current_level = complaint.escalation_level
        target_level = current_level + 1
    
    # Get escalation target based on level
    escalated_to = None
    
    if target_level == 1:  # Department Head
        if complaint.department and complaint.department.head:
            escalated_to = complaint.department.head
    elif target_level == 2:  # Dean
        if complaint.department and complaint.department.college and complaint.department.college.dean:
            escalated_to = complaint.department.college.dean
    elif target_level == 3:  # Campus Director
        if complaint.campus and complaint.campus.director:
            escalated_to = complaint.campus.director
    elif target_level >= 4:  # Admin
        # Get first available admin
        escalated_to = CustomUser.objects.filter(
            role__in=['admin', 'super_admin'],
            is_active=True
        ).first()
    
    if escalated_to:
        complaint.escalated = True
        complaint.escalated_at = timezone.now()
        complaint.escalated_to = escalated_to
        complaint.escalation_level = target_level
        complaint.escalation_reason = reason
        complaint.save()
        
        # Create event
        ComplaintEvent.objects.create(
            complaint=complaint,
            event_type='escalated',
            actor=escalated_by,
            notes=f"Escalated to level {target_level}: {reason}"
        )
        
        return escalated_to
    
    return None


def auto_escalate_breached_complaints():
    """
    Automatically escalate complaints that have breached SLA.
    This should be called periodically.
    """
    breached = check_and_update_sla_breaches()
    escalated_count = 0
    
    for complaint in breached:
        # Only auto-escalate if not already escalated or if escalation level is low
        if not complaint.escalated or complaint.escalation_level < 2:
            escalated_to = escalate_complaint(
                complaint,
                escalated_by=None,  # System escalation
                reason=f"Automatic escalation due to SLA breach",
                target_level=complaint.escalation_level + 1
            )
            if escalated_to:
                escalated_count += 1
    
    return escalated_count


def record_first_response(complaint, responder):
    """
    Record the first response to a complaint.
    """
    if not complaint.first_response_at:
        complaint.first_response_at = timezone.now()
        complaint.save()
        
        # Create event
        ComplaintEvent.objects.create(
            complaint=complaint,
            event_type='first_response',
            actor=responder,
            notes="First response recorded"
        )

