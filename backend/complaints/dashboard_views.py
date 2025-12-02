"""
Role-based dashboard views for different user roles
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg, F, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Complaint, ComplaintEvent, Category
from accounts.models import CustomUser, Department, College, Campus
from .serializers import ComplaintSerializer
import logging

logger = logging.getLogger(__name__)


class BaseDashboardView(viewsets.ViewSet):
    """Base class for dashboard views"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_user_role(self):
        return getattr(self.request.user, 'role', 'student')
    
    def get_user_campus(self):
        return getattr(self.request.user, 'campus', None)
    
    def get_user_department(self):
        return getattr(self.request.user, 'department', None)
    
    def get_user_college(self):
        dept = self.get_user_department()
        return dept.college if dept else None


class StudentDashboardView(BaseDashboardView):
    """Student Dashboard - My complaints, status, history"""
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        user = request.user
        complaints = Complaint.objects.filter(submitter=user)
        
        # Calculate stats
        total = complaints.count()
        open_count = complaints.filter(status__in=['new', 'assigned', 'in_progress', 'pending']).count()
        resolved_count = complaints.filter(status='resolved').count()
        closed_count = complaints.filter(status='closed').count()
        
        # Average response time
        responded = complaints.exclude(first_response_at__isnull=True)
        avg_response_time = None
        if responded.exists():
            response_times = [
                (c.first_response_at - c.created_at).total_seconds() / 3600
                for c in responded
            ]
            avg_response_time = sum(response_times) / len(response_times) if response_times else None
        
        # Average rating
        rated = complaints.exclude(feedback_rating__isnull=True)
        avg_rating = rated.aggregate(Avg('feedback_rating'))['feedback_rating__avg']
        
        # SLA breaches
        sla_breaches = complaints.filter(
            Q(sla_response_breached=True) | Q(sla_resolution_breached=True)
        ).count()
        
        return Response({
            'total_complaints': total,
            'open_complaints': open_count,
            'resolved_complaints': resolved_count,
            'closed_complaints': closed_count,
            'average_response_time_hours': round(avg_response_time, 2) if avg_response_time else None,
            'average_rating': round(avg_rating, 2) if avg_rating else None,
            'sla_breaches': sla_breaches,
        })
    
    @action(detail=False, methods=['get'])
    def recent_complaints(self, request):
        user = request.user
        complaints = Complaint.objects.filter(submitter=user).order_by('-created_at')[:10]
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        user = request.user
        complaints = Complaint.objects.filter(submitter=user).order_by('-created_at')
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data)


class DeanDashboardView(BaseDashboardView):
    """Dean Dashboard - College-level complaints and analytics"""
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        user = request.user
        college = self.get_user_college()
        
        if not college:
            return Response({'error': 'User is not associated with a college'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Get all complaints from departments in this college
        departments = Department.objects.filter(college=college)
        complaints = Complaint.objects.filter(department__in=departments)
        
        # Stats by department
        dept_stats = []
        for dept in departments:
            dept_complaints = complaints.filter(department=dept)
            dept_stats.append({
                'department': dept.name,
                'total': dept_complaints.count(),
                'open': dept_complaints.filter(status__in=['new', 'assigned', 'in_progress']).count(),
                'resolved': dept_complaints.filter(status='resolved').count(),
            })
        
        # Overall stats
        total = complaints.count()
        unresolved = complaints.filter(
            status__in=['new', 'assigned', 'in_progress', 'pending']
        ).count()
        sla_breaches = complaints.filter(
            Q(sla_response_breached=True) | Q(sla_resolution_breached=True)
        ).count()
        
        # Average resolution time
        resolved = complaints.filter(status__in=['resolved', 'closed'])
        avg_resolution_time = None
        if resolved.exists():
            resolution_times = [
                (c.resolved_at or c.closed_at or c.updated_at) - c.created_at
                for c in resolved if c.resolved_at or c.closed_at
            ]
            if resolution_times:
                avg_resolution_time = sum(t.total_seconds() / 3600 for t in resolution_times) / len(resolution_times)
        
        # Top categories
        top_categories = complaints.values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        return Response({
            'college': college.name,
            'total_complaints': total,
            'unresolved_complaints': unresolved,
            'sla_breaches': sla_breaches,
            'average_resolution_time_hours': round(avg_resolution_time, 2) if avg_resolution_time else None,
            'department_stats': dept_stats,
            'top_categories': list(top_categories),
        })
    
    @action(detail=False, methods=['get'])
    def pending_approvals(self, request):
        user = request.user
        college = self.get_user_college()
        
        if not college:
            return Response([])
        
        departments = Department.objects.filter(college=college)
        complaints = Complaint.objects.filter(
            department__in=departments,
            requires_approval=True,
            approved_by__isnull=True
        ).order_by('-created_at')
        
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data)


class ProctorDashboardView(BaseDashboardView):
    """Proctor Dashboard - Exam and security-related complaints"""
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        # Get security/exam related complaints
        security_category = Category.objects.filter(name__icontains='security').first()
        exam_category = Category.objects.filter(name__icontains='exam').first()
        
        categories = [c for c in [security_category, exam_category] if c]
        
        if not categories:
            complaints = Complaint.objects.none()
        else:
            complaints = Complaint.objects.filter(
                Q(category__in=categories) | 
                Q(sub_category__category__in=categories)
            )
        
        total = complaints.count()
        pending_investigation = complaints.filter(status__in=['new', 'assigned']).count()
        in_progress = complaints.filter(status='in_progress').count()
        resolved = complaints.filter(status='resolved').count()
        
        return Response({
            'total_incidents': total,
            'pending_investigation': pending_investigation,
            'in_progress': in_progress,
            'resolved': resolved,
        })
    
    @action(detail=False, methods=['get'])
    def exam_complaints(self, request):
        exam_category = Category.objects.filter(name__icontains='exam').first()
        if not exam_category:
            return Response([])
        
        complaints = Complaint.objects.filter(
            Q(category=exam_category) | Q(sub_category__category=exam_category)
        ).order_by('-created_at')
        
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data)


class AdminDashboardView(BaseDashboardView):
    """Admin Dashboard - System-wide overview"""
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        complaints = Complaint.objects.all()
        
        # Overall stats
        total = complaints.count()
        new = complaints.filter(status='new').count()
        in_progress = complaints.filter(status='in_progress').count()
        resolved = complaints.filter(status='resolved').count()
        closed = complaints.filter(status='closed').count()
        
        # SLA breaches
        sla_breaches = complaints.filter(
            Q(sla_response_breached=True) | Q(sla_resolution_breached=True)
        ).count()
        
        # By campus
        campus_stats = []
        for campus in Campus.objects.all():
            campus_complaints = complaints.filter(campus=campus)
            campus_stats.append({
                'campus': campus.name,
                'total': campus_complaints.count(),
                'open': campus_complaints.filter(status__in=['new', 'assigned', 'in_progress']).count(),
            })
        
        # By category
        category_stats = complaints.values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # Recent activity
        recent_events = ComplaintEvent.objects.all().order_by('-timestamp')[:20]
        
        # Average satisfaction rating
        rated_complaints = complaints.exclude(feedback_rating__isnull=True)
        avg_satisfaction = rated_complaints.aggregate(Avg('feedback_rating'))['feedback_rating__avg']
        total_ratings = rated_complaints.count()
        
        return Response({
            'total_complaints': total,
            'new_complaints': new,
            'in_progress': in_progress,
            'resolved': resolved,
            'closed': closed,
            'sla_breaches': sla_breaches,
            'average_satisfaction': round(avg_satisfaction, 2) if avg_satisfaction else None,
            'total_ratings': total_ratings,
            'campus_stats': list(campus_stats),
            'category_stats': list(category_stats),
        })


class DepartmentHeadDashboardView(BaseDashboardView):
    """Department Head Dashboard - Department-level management"""
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        user = request.user
        department = self.get_user_department()
        
        if not department:
            return Response({'error': 'User is not associated with a department'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        complaints = Complaint.objects.filter(department=department)
        
        # Overall stats
        total = complaints.count()
        new = complaints.filter(status='new').count()
        assigned = complaints.filter(status='assigned').count()
        in_progress = complaints.filter(status='in_progress').count()
        resolved = complaints.filter(status='resolved').count()
        
        # Staff workload
        staff_workload = []
        staff_members = CustomUser.objects.filter(
            department=department,
            role__in=['academic', 'non_academic', 'maintenance']
        )
        
        for staff in staff_members:
            assigned_count = complaints.filter(assigned_to=staff).count()
            open_count = complaints.filter(
                assigned_to=staff,
                status__in=['assigned', 'in_progress']
            ).count()
            staff_workload.append({
                'staff_name': staff.get_full_name() or staff.username,
                'total_assigned': assigned_count,
                'open_assigned': open_count,
            })
        
        # Pending approvals
        pending_approvals = complaints.filter(
            requires_approval=True,
            approved_by__isnull=True
        ).count()
        
        # SLA breaches
        sla_breaches = complaints.filter(
            Q(sla_response_breached=True) | Q(sla_resolution_breached=True)
        ).count()
        
        return Response({
            'department': department.name,
            'total_complaints': total,
            'new_complaints': new,
            'assigned': assigned,
            'in_progress': in_progress,
            'resolved': resolved,
            'pending_approvals': pending_approvals,
            'sla_breaches': sla_breaches,
            'staff_workload': staff_workload,
        })


class MaintenanceWorkerDashboardView(BaseDashboardView):
    """Maintenance Worker Dashboard - Assigned maintenance tasks"""
    
    @action(detail=False, methods=['get'])
    def tasks(self, request):
        user = request.user
        
        # Get ALL complaints assigned to this maintenance worker
        complaints = Complaint.objects.filter(assigned_to=user).order_by('-created_at')
        
        # Filter by status
        open_tasks = complaints.filter(status__in=['new', 'assigned', 'in_progress'])
        completed_tasks = complaints.filter(status__in=['resolved', 'closed'])
        
        return Response({
            'open_tasks': ComplaintSerializer(open_tasks, many=True).data,
            'completed_tasks': ComplaintSerializer(completed_tasks, many=True).data,
            'total_open': open_tasks.count(),
            'total_completed': completed_tasks.count(),
        })


class CampusDirectorDashboardView(BaseDashboardView):
    """Campus Director Dashboard - Campus-wide overview"""
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        user = request.user
        campus = self.get_user_campus()
        
        if not campus:
            return Response({'error': 'User is not associated with a campus'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        complaints = Complaint.objects.filter(campus=campus)
        
        # Overall stats
        total = complaints.count()
        critical = complaints.filter(priority='critical').count()
        high = complaints.filter(priority='high').count()
        unresolved = complaints.filter(
            status__in=['new', 'assigned', 'in_progress', 'pending']
        ).count()
        
        # SLA compliance
        sla_breaches = complaints.filter(
            Q(sla_response_breached=True) | Q(sla_resolution_breached=True)
        ).count()
        sla_compliance = ((total - sla_breaches) / total * 100) if total > 0 else 100
        
        # By category
        category_stats = complaints.values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # Critical incidents
        critical_incidents = complaints.filter(
            priority='critical',
            status__in=['new', 'assigned', 'in_progress']
        ).order_by('-created_at')[:10]
        
        return Response({
            'campus': campus.name,
            'total_complaints': total,
            'critical_complaints': critical,
            'high_priority': high,
            'unresolved': unresolved,
            'sla_breaches': sla_breaches,
            'sla_compliance_percent': round(sla_compliance, 2),
            'category_stats': list(category_stats),
            'critical_incidents': ComplaintSerializer(critical_incidents, many=True).data,
        })


class SuperAdminDashboardView(BaseDashboardView):
    """Super Admin Dashboard - System-wide analytics and management"""
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        complaints = Complaint.objects.all()
        users = CustomUser.objects.all()
        
        # System-wide stats
        total_complaints = complaints.count()
        total_users = users.count()
        
        # By role
        user_by_role = users.values('role').annotate(count=Count('id'))
        
        # Complaint trends (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_complaints = complaints.filter(created_at__gte=thirty_days_ago)
        
        # SLA compliance
        sla_breaches = complaints.filter(
            Q(sla_response_breached=True) | Q(sla_resolution_breached=True)
        ).count()
        
        # Satisfaction
        rated = complaints.exclude(feedback_rating__isnull=True)
        avg_satisfaction = rated.aggregate(Avg('feedback_rating'))['feedback_rating__avg']
        
        return Response({
            'total_complaints': total_complaints,
            'total_users': total_users,
            'users_by_role': list(user_by_role),
            'complaints_last_30_days': recent_complaints.count(),
            'sla_breaches': sla_breaches,
            'average_satisfaction': round(avg_satisfaction, 2) if avg_satisfaction else None,
        })

