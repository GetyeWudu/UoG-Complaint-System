"""
Approval workflow views for complaint approvals
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Complaint, ComplaintEvent
from .serializers import ComplaintSerializer
from .notifications import send_complaint_notification
from accounts.models import CustomUser
import logging

logger = logging.getLogger(__name__)


class ApprovalWorkflowViewSet(viewsets.ViewSet):
    """
    ViewSet for handling approval workflow
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get complaints that need approval based on user role"""
        user = self.request.user
        role = user.role
        
        # Base queryset
        queryset = Complaint.objects.filter(requires_approval=True, approved_by__isnull=True)
        
        # Filter based on role
        if role == 'dept_head':
            # Department Head can approve complaints from their department
            if user.department:
                queryset = queryset.filter(department=user.department)
        elif role == 'dean':
            # Dean can approve complaints from their college
            if user.department and user.department.college:
                from accounts.models import Department
                departments = Department.objects.filter(college=user.department.college)
                queryset = queryset.filter(department__in=departments)
        elif role == 'campus_director':
            # Campus Director can approve complaints from their campus
            if user.campus:
                queryset = queryset.filter(campus=user.campus)
        elif role in ['admin', 'super_admin']:
            # Admins can approve any complaint
            pass
        else:
            # Other roles cannot approve
            queryset = queryset.none()
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get list of pending approvals"""
        queryset = self.get_queryset()
        serializer = ComplaintSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a complaint"""
        try:
            complaint = Complaint.objects.get(pk=pk)
        except Complaint.DoesNotExist:
            return Response({'error': 'Complaint not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user can approve
        if not self.can_approve(request.user, complaint):
            return Response(
                {'error': 'You do not have permission to approve this complaint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if already approved
        if complaint.approved_by:
            return Response(
                {'error': 'Complaint already approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get approval notes
        approval_notes = request.data.get('notes', '')
        
        # Approve
        complaint.approved_by = request.user
        complaint.approved_at = timezone.now()
        complaint.approval_notes = approval_notes
        complaint.requires_approval = False
        complaint.save()
        
        # Create event
        ComplaintEvent.objects.create(
            complaint=complaint,
            event_type='status_changed',
            actor=request.user,
            old_value='Pending Approval',
            new_value='Approved',
            notes=f"Approved by {request.user.get_full_name() or request.user.username}: {approval_notes}"
        )
        
        # Send notification
        send_complaint_notification(complaint, 'reviewed', {
            'additional_message': f'Your complaint has been approved. {approval_notes}'
        })
        
        serializer = ComplaintSerializer(complaint)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a complaint approval request"""
        try:
            complaint = Complaint.objects.get(pk=pk)
        except Complaint.DoesNotExist:
            return Response({'error': 'Complaint not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user can approve
        if not self.can_approve(request.user, complaint):
            return Response(
                {'error': 'You do not have permission to reject this complaint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get rejection reason
        rejection_reason = request.data.get('reason', '')
        if not rejection_reason:
            return Response(
                {'error': 'Rejection reason is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Reject
        complaint.status = 'rejected'
        complaint.rejection_reason = rejection_reason
        complaint.requires_approval = False
        complaint.save()
        
        # Create event
        ComplaintEvent.objects.create(
            complaint=complaint,
            event_type='rejected',
            actor=request.user,
            notes=f"Rejected by {request.user.get_full_name() or request.user.username}: {rejection_reason}"
        )
        
        # Send notification
        send_complaint_notification(complaint, 'rejected')
        
        serializer = ComplaintSerializer(complaint)
        return Response(serializer.data)
    
    def can_approve(self, user, complaint):
        """Check if user can approve this complaint"""
        role = user.role
        
        if role in ['admin', 'super_admin']:
            return True
        
        if role == 'dept_head':
            return complaint.department == user.department
        
        if role == 'dean':
            if complaint.department and complaint.department.college:
                return complaint.department.college == user.department.college
        
        if role == 'campus_director':
            return complaint.campus == user.campus
        
        return False
    
    @action(detail=True, methods=['post'])
    def request_approval(self, request, pk=None):
        """Request approval for a complaint"""
        try:
            complaint = Complaint.objects.get(pk=pk)
        except Complaint.DoesNotExist:
            return Response({'error': 'Complaint not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user can request approval (typically assigned staff)
        if complaint.assigned_to != request.user and request.user.role not in ['admin', 'super_admin']:
            return Response(
                {'error': 'You do not have permission to request approval for this complaint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Determine who should approve based on complaint type/priority
        approver = self.determine_approver(complaint)
        
        if not approver:
            return Response(
                {'error': 'Could not determine approver for this complaint'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Request approval
        complaint.requires_approval = True
        complaint.save()
        
        # Create event
        ComplaintEvent.objects.create(
            complaint=complaint,
            event_type='status_changed',
            actor=request.user,
            old_value=complaint.status,
            new_value='Pending Approval',
            notes=f"Approval requested from {approver.get_full_name() or approver.username}"
        )
        
        serializer = ComplaintSerializer(complaint)
        return Response({
            'message': 'Approval requested',
            'approver': approver.get_full_name() or approver.username,
            'complaint': serializer.data
        })
    
    def determine_approver(self, complaint):
        """Determine who should approve based on complaint characteristics"""
        # Priority-based: Critical/High may need Dean/Campus Director approval
        if complaint.priority in ['critical', 'high']:
            # Try Campus Director first
            if complaint.campus and complaint.campus.director:
                return complaint.campus.director
            # Then Dean
            if complaint.department and complaint.department.college and complaint.department.college.dean:
                return complaint.department.college.dean
        
        # Default: Department Head
        if complaint.department and complaint.department.head:
            return complaint.department.head
        
        # Fallback: Admin
        return CustomUser.objects.filter(role__in=['admin', 'super_admin'], is_active=True).first()

