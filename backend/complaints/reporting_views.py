"""
Reporting and export views
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from .models import Complaint
from .reporting import generate_complaints_report, get_dashboard_statistics
from .serializers import ComplaintSerializer
import logging

logger = logging.getLogger(__name__)


class ReportingViewSet(viewsets.ViewSet):
    """
    ViewSet for generating reports and exports
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export complaints as Excel or PDF"""
        format_type = request.query_params.get('format', 'excel')  # 'excel' or 'pdf'
        
        # Get complaints based on user role
        complaints = self.get_complaints_queryset(request.user)
        
        # Apply filters
        status_filter = request.query_params.get('status')
        priority_filter = request.query_params.get('priority')
        category_filter = request.query_params.get('category')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        if status_filter:
            complaints = complaints.filter(status=status_filter)
        if priority_filter:
            complaints = complaints.filter(priority=priority_filter)
        if category_filter:
            complaints = complaints.filter(category_id=category_filter)
        if date_from:
            complaints = complaints.filter(created_at__gte=date_from)
        if date_to:
            complaints = complaints.filter(created_at__lte=date_to)
        
        # Build filters dict for report
        filters = {}
        if status_filter:
            filters['Status'] = status_filter
        if priority_filter:
            filters['Priority'] = priority_filter
        
        try:
            # Generate report
            report_buffer = generate_complaints_report(complaints, format=format_type, filters=filters)
            
            # Determine content type and file extension
            if format_type == 'excel':
                content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                filename = f'complaints_report_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            else:  # PDF
                content_type = 'application/pdf'
                filename = f'complaints_report_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf'
            
            # Create response
            response = HttpResponse(
                report_buffer.read(),
                content_type=content_type
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to generate report: {str(e)}")
            return Response(
                {'error': f'Failed to generate report: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get comprehensive statistics"""
        user = request.user
        role = user.role
        
        # Get date range
        days = int(request.query_params.get('days', 30))
        date_range = (
            timezone.now() - timedelta(days=days),
            timezone.now()
        )
        
        stats = get_dashboard_statistics(user, role, date_range)
        
        return Response(stats)
    
    def get_complaints_queryset(self, user):
        """Get complaints queryset based on user role"""
        role = user.role
        
        if role == 'student':
            return Complaint.objects.filter(submitter=user)
        elif role == 'dept_head':
            if user.department:
                return Complaint.objects.filter(department=user.department)
            return Complaint.objects.none()
        elif role == 'dean':
            if user.department and user.department.college:
                from accounts.models import Department
                departments = Department.objects.filter(college=user.department.college)
                return Complaint.objects.filter(department__in=departments)
            return Complaint.objects.none()
        elif role == 'campus_director':
            if user.campus:
                return Complaint.objects.filter(campus=user.campus)
            return Complaint.objects.none()
        elif role in ['admin', 'super_admin']:
            return Complaint.objects.all()
        else:
            return Complaint.objects.filter(assigned_to=user)

