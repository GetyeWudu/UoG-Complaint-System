from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
import uuid
import logging

from .models import Complaint, ComplaintFile, ComplaintComment, ComplaintEvent
from .serializers import (
    ComplaintSerializer, ComplaintFileSerializer, 
    ComplaintCommentSerializer, ComplaintEventSerializer
)
from .ai_service import analyze_urgency
from accounts.serializers import UserSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


class StaffListView(generics.ListAPIView):
    """List all staff members (non-students)"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.exclude(role='student')

class AnonymousComplaintView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        location = request.data.get('location')
        
        track_id = f"CMP-{str(uuid.uuid4())[:4].upper()}"
        
        # USE NEW AI SERVICE
        urgency_score = analyze_urgency(description)
        
        Complaint.objects.create(
            title=title, description=description, location=location,
            urgency=urgency_score,
            tracking_id=track_id, user=None
        )
        return Response({"tracking_id": track_id, "message": "Submitted!"})

class TrackComplaintView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, tracking_id):
        try:
            c = Complaint.objects.get(tracking_id=tracking_id)
            return Response({
                "title": c.title, "status": c.status, 
                "urgency": c.urgency, "location": c.location, 
                "created_at": c.created_at
            })
        except Complaint.DoesNotExist:
            return Response({"error": "Invalid ID"}, status=404)

class ComplaintListCreateView(generics.ListCreateAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', 'student')
        
        # 1. Student: See ONLY their own
        if role == 'student':
            return Complaint.objects.filter(submitter=user)
            
        # 2. Proctor: See ONLY "Facility" issues
        if role == 'proctor':
            return Complaint.objects.filter(is_facility=True)
            
        # 3. Dept Head: See ONLY "Academic" issues from THEIR department
        if role == 'dept_head':
            if user.department:
                # Find complaints from their department
                return Complaint.objects.filter(
                    is_academic=True, 
                    department=user.department
                )
            return Complaint.objects.none()

        # 4. Admin & Super Admin: See Everything
        if role in ['admin', 'super_admin']:
            return Complaint.objects.all().order_by('-created_at')
        
        # 5. Other staff: See assigned complaints
        return Complaint.objects.filter(assigned_to=user).order_by('-created_at')

    def perform_create(self, serializer):
        from django.utils import timezone
        
        description = serializer.validated_data.get('description', '')
        
        # AI ANALYSIS for urgency
        urgency_score = analyze_urgency(description)
        
        # Generate tracking ID
        track_id = f"CMP-{str(uuid.uuid4())[:8].upper()}"
        
        # Create complaint
        complaint = serializer.save(
            submitter=self.request.user, 
            urgency=urgency_score, 
            tracking_id=track_id,
            status='new'
        )
        
        # Apply auto-routing rules
        apply_routing_rules(complaint)
        
        # Handle file uploads
        files = self.request.FILES.getlist('uploaded_files')
        if files:
            from .validators import validate_file_size, validate_file_extension, sanitize_filename
            
            for file in files:
                try:
                    validate_file_size(file)
                    validate_file_extension(file)
                    
                    safe_filename = sanitize_filename(file.name)
                    
                    ComplaintFile.objects.create(
                        complaint=complaint,
                        uploaded_by=self.request.user,
                        file=file,
                        filename=safe_filename,
                        file_size=file.size,
                        mime_type=file.content_type
                    )
                except Exception as e:
                    # Log error but don't fail the complaint creation
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to upload file {file.name}: {str(e)}")
        
        # Log creation event
        ComplaintEvent.objects.create(
            complaint=complaint,
            event_type='created',
            actor=self.request.user,
            notes='Complaint created'
        )
        
        # Send confirmation email
        if self.request.user.email:
            from accounts.utils import send_email
            from django.conf import settings
            
            send_email(
                template_type='submission_confirmation',
                recipient=self.request.user.email,
                context={
                    'submitter_name': self.request.user.get_full_name() or self.request.user.username,
                    'tracking_id': complaint.tracking_id,
                    'title': complaint.title,
                    'status': complaint.get_status_display(),
                    'complaint_url': f"{settings.FRONTEND_URL}/complaints/{complaint.id}",
                }
            )

class ComplaintDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        """Send notifications when complaint status changes"""
        from .notifications import (
            notify_complaint_reviewed,
            notify_complaint_assigned,
            notify_complaint_in_progress,
            notify_complaint_resolved,
            notify_complaint_rejected,
            notify_complaint_closed
        )
        
        old_status = self.get_object().status
        complaint = serializer.save()
        new_status = complaint.status
        
        # Send notification if status changed
        if old_status != new_status:
            if new_status == 'assigned':
                notify_complaint_assigned(complaint)
            elif new_status == 'in_progress':
                notify_complaint_in_progress(complaint)
            elif new_status == 'resolved':
                notify_complaint_resolved(complaint)
            elif new_status == 'rejected':
                notify_complaint_rejected(complaint)
            elif new_status == 'closed':
                notify_complaint_closed(complaint)
            else:
                # For any other status change, send generic review notification
                notify_complaint_reviewed(complaint)
        
        # Log the status change
        ComplaintEvent.objects.create(
            complaint=complaint,
            event_type='status_change',
            description=f'Status changed from {old_status} to {new_status}',
            user=self.request.user
        )

# --- NEW VIEW FOR FEEDBACK ---
class ComplaintFeedbackView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, pk):
        try:
            complaint = Complaint.objects.get(pk=pk)
            complaint.feedback_rating = request.data.get('feedback_rating')
            complaint.feedback_comment = request.data.get('feedback_comment', '')
            complaint.save()
            return Response({'status': 'feedback saved'})
        except Complaint.DoesNotExist:
            return Response({'error': 'Complaint not found'}, status=404)



# File Management Views
class ComplaintFileUploadView(APIView):
    """
    Upload files to a complaint
    POST /api/complaints/{complaint_id}/files/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, complaint_id):
        try:
            complaint = Complaint.objects.get(pk=complaint_id)
        except Complaint.DoesNotExist:
            return Response({'error': 'Complaint not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check permissions
        user = request.user
        if complaint.submitter and complaint.submitter != user and user.role not in ['admin', 'super_admin']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        files = request.FILES.getlist('files')
        if not files:
            return Response({'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_files = []
        errors = []
        
        for file in files:
            try:
                from .validators import validate_file_size, validate_file_extension, sanitize_filename
                
                # Validate file
                validate_file_size(file)
                validate_file_extension(file)
                
                # Sanitize filename
                safe_filename = sanitize_filename(file.name)
                
                # Create ComplaintFile
                complaint_file = ComplaintFile.objects.create(
                    complaint=complaint,
                    uploaded_by=user,
                    file=file,
                    filename=safe_filename,
                    file_size=file.size,
                    mime_type=file.content_type
                )
                
                uploaded_files.append({
                    'id': complaint_file.id,
                    'filename': complaint_file.filename,
                    'size': complaint_file.file_size,
                    'url': f'/api/complaints/files/{complaint_file.id}/download/'
                })
                
                # Log event
                ComplaintEvent.objects.create(
                    complaint=complaint,
                    event_type='file_attached',
                    actor=user,
                    notes=f'Uploaded file: {safe_filename}'
                )
                
            except Exception as e:
                errors.append({'file': file.name, 'error': str(e)})
        
        return Response({
            'uploaded': uploaded_files,
            'errors': errors,
            'message': f'{len(uploaded_files)} file(s) uploaded successfully'
        }, status=status.HTTP_201_CREATED if uploaded_files else status.HTTP_400_BAD_REQUEST)


class ComplaintFileDownloadView(APIView):
    """
    Download a complaint file (authenticated)
    GET /api/complaints/files/{file_id}/download/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, file_id):
        try:
            complaint_file = ComplaintFile.objects.get(pk=file_id)
        except ComplaintFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check permissions
        complaint = complaint_file.complaint
        user = request.user
        
        # Allow access if:
        # - User is the submitter
        # - User is assigned to the complaint
        # - User is admin/super_admin
        # - User is dept_head of the complaint's department
        can_access = (
            (complaint.submitter and complaint.submitter == user) or
            complaint.assigned_to == user or
            user.role in ['admin', 'super_admin'] or
            (user.role == 'dept_head' and complaint.department == user.department)
        )
        
        if not can_access:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Serve file
        from django.http import FileResponse
        import os
        
        if not complaint_file.file:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        
        response = FileResponse(complaint_file.file.open('rb'))
        response['Content-Type'] = complaint_file.mime_type
        response['Content-Disposition'] = f'attachment; filename="{complaint_file.filename}"'
        
        return response


class ComplaintFileDeleteView(APIView):
    """
    Delete a complaint file
    DELETE /api/complaints/files/{file_id}/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, file_id):
        try:
            complaint_file = ComplaintFile.objects.get(pk=file_id)
        except ComplaintFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check permissions (only uploader or admin can delete)
        user = request.user
        if complaint_file.uploaded_by != user and user.role not in ['admin', 'super_admin']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Log event
        ComplaintEvent.objects.create(
            complaint=complaint_file.complaint,
            event_type='file_attached',
            actor=user,
            notes=f'Deleted file: {complaint_file.filename}'
        )
        
        # Delete file
        filename = complaint_file.filename
        complaint_file.file.delete()
        complaint_file.delete()
        
        return Response({
            'message': f'File {filename} deleted successfully'
        }, status=status.HTTP_200_OK)


# Comment Management Views
class ComplaintCommentListCreateView(generics.ListCreateAPIView):
    """
    List and create comments for a complaint
    GET/POST /api/complaints/{complaint_id}/comments/
    """
    serializer_class = ComplaintCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        complaint_id = self.kwargs['complaint_id']
        # Only return top-level comments (replies are nested in serializer)
        return ComplaintComment.objects.filter(complaint_id=complaint_id, parent__isnull=True)
    
    def perform_create(self, serializer):
        complaint_id = self.kwargs['complaint_id']
        complaint = Complaint.objects.get(pk=complaint_id)
        
        comment = serializer.save(
            complaint=complaint,
            author=self.request.user
        )
        
        # Log event
        ComplaintEvent.objects.create(
            complaint=complaint,
            event_type='comment_added',
            actor=self.request.user,
            notes=f'Added comment'
        )


# Assignment & Workflow Views
class ComplaintAssignView(APIView):
    """
    Assign complaint to a user
    POST /api/complaints/{complaint_id}/assign/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, complaint_id):
        try:
            complaint = Complaint.objects.get(pk=complaint_id)
        except Complaint.DoesNotExist:
            return Response({'error': 'Complaint not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check permissions (only dept_head, admin, super_admin can assign)
        user = request.user
        if user.role not in ['dept_head', 'admin', 'super_admin']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        assigned_to_id = request.data.get('assigned_to')
        if not assigned_to_id:
            return Response({'error': 'assigned_to is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            assigned_user = User.objects.get(pk=assigned_to_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update complaint
        old_assignee = complaint.assigned_to
        complaint.assigned_to = assigned_user
        complaint.status = 'assigned'
        
        if not complaint.assigned_at:
            complaint.assigned_at = timezone.now()
        
        complaint.save()
        
        # Log event
        ComplaintEvent.objects.create(
            complaint=complaint,
            event_type='assigned',
            actor=user,
            old_value=old_assignee.username if old_assignee else 'None',
            new_value=assigned_user.username,
            notes=f'Assigned to {assigned_user.get_full_name() or assigned_user.username}'
        )
        
        # Send notification email
        from accounts.utils import send_email
        send_email(
            template_type='assignment_notification',
            recipient=assigned_user.email,
            context={
                'assignee_name': assigned_user.get_full_name() or assigned_user.username,
                'tracking_id': complaint.tracking_id,
                'title': complaint.title,
                'priority': complaint.get_priority_display(),
                'complaint_url': f"{settings.FRONTEND_URL}/complaints/{complaint.id}",
            }
        )
        
        return Response({
            'message': 'Complaint assigned successfully',
            'complaint': ComplaintSerializer(complaint, context={'request': request}).data
        }, status=status.HTTP_200_OK)


class ComplaintStatusUpdateView(APIView):
    """
    Update complaint status
    POST /api/complaints/{complaint_id}/status/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, complaint_id):
        try:
            complaint = Complaint.objects.get(pk=complaint_id)
        except Complaint.DoesNotExist:
            return Response({'error': 'Complaint not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        new_status = request.data.get('status')
        notes = request.data.get('notes', '')
        
        if not new_status:
            return Response({'error': 'status is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate status
        valid_statuses = dict(Complaint.STATUS_CHOICES).keys()
        if new_status not in valid_statuses:
            return Response({'error': f'Invalid status. Valid options: {", ".join(valid_statuses)}'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Check permissions
        can_update = (
            complaint.assigned_to == user or
            user.role in ['dept_head', 'admin', 'super_admin']
        )
        
        if not can_update:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Update status
        old_status = complaint.status
        complaint.status = new_status
        
        # Update timestamps
        if new_status == 'in_progress' and not complaint.in_progress_at:
            complaint.in_progress_at = timezone.now()
        elif new_status == 'resolved' and not complaint.resolved_at:
            complaint.resolved_at = timezone.now()
        elif new_status == 'closed' and not complaint.closed_at:
            complaint.closed_at = timezone.now()
        
        complaint.save()
        
        # Log event
        ComplaintEvent.objects.create(
            complaint=complaint,
            event_type='status_changed',
            actor=user,
            old_value=old_status,
            new_value=new_status,
            notes=notes
        )
        
        # Send notification to submitter
        if complaint.submitter and complaint.submitter.email:
            from accounts.utils import send_email
            send_email(
                template_type='status_change',
                recipient=complaint.submitter.email,
                context={
                    'submitter_name': complaint.submitter.get_full_name() or complaint.submitter.username,
                    'tracking_id': complaint.tracking_id,
                    'title': complaint.title,
                    'old_status': old_status,
                    'new_status': new_status,
                    'notes': notes,
                    'complaint_url': f"{settings.FRONTEND_URL}/complaints/{complaint.id}",
                }
            )
        
        return Response({
            'message': 'Status updated successfully',
            'complaint': ComplaintSerializer(complaint, context={'request': request}).data
        }, status=status.HTTP_200_OK)


# Auto-routing
def apply_routing_rules(complaint):
    """
    Apply routing rules to automatically assign complaint
    """
    from .models import RoutingRule
    
    # Get applicable rules
    rules = RoutingRule.objects.filter(
        is_active=True
    ).order_by('-priority')
    
    for rule in rules:
        # Check if rule matches
        matches = True
        
        if rule.category and complaint.category != rule.category:
            matches = False
        if rule.sub_category and complaint.sub_category != rule.sub_category:
            matches = False
        if rule.campus and complaint.campus != rule.campus:
            matches = False
        
        if matches:
            # Apply rule
            if rule.assign_to_user:
                complaint.assigned_to = rule.assign_to_user
                complaint.status = 'assigned'
                complaint.assigned_at = timezone.now()
            
            if rule.assign_to_department:
                complaint.department = rule.assign_to_department
            
            if rule.set_priority:
                complaint.priority = rule.set_priority
            
            complaint.save()
            
            # Log event
            ComplaintEvent.objects.create(
                complaint=complaint,
                event_type='assigned',
                actor=None,
                notes=f'Auto-assigned by rule: {rule.name}'
            )
            
            return True
    
    return False
