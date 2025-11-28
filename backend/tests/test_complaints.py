"""
Tests for complaint endpoints
"""
import pytest
from rest_framework import status
from complaints.models import Complaint, ComplaintEvent, ComplaintComment
from io import BytesIO
from PIL import Image


@pytest.fixture
def create_complaint(db, student_user, category, campus):
    """Factory fixture for creating complaints"""
    def make_complaint(**kwargs):
        defaults = {
            'title': 'Test Complaint',
            'description': 'Test description',
            'location': 'Test Location',
            'submitter': student_user,
            'category': category,
            'campus': campus,
            'status': 'new',
            'priority': 'medium',
            'urgency': 'low',
        }
        defaults.update(kwargs)
        return Complaint.objects.create(**defaults)
    
    return make_complaint


@pytest.mark.django_db
class TestComplaintCreation:
    """Test complaint creation"""
    
    def test_create_complaint_success(self, authenticated_client, category, campus):
        """Test successful complaint creation"""
        data = {
            'title': 'Broken projector',
            'description': 'The projector in room 301 is not working',
            'location': 'Room 301',
            'category': category.id,
            'campus': campus.id,
        }
        
        response = authenticated_client.post('/api/complaints/', data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'tracking_id' in response.data
        assert response.data['title'] == 'Broken projector'
        
        # Verify complaint created
        complaint = Complaint.objects.get(tracking_id=response.data['tracking_id'])
        assert complaint.submitter == authenticated_client.user
        assert complaint.status == 'new'
        
        # Verify event logged
        assert ComplaintEvent.objects.filter(
            complaint=complaint,
            event_type='created'
        ).exists()
    
    def test_create_complaint_with_files(self, authenticated_client, category, campus):
        """Test complaint creation with file upload"""
        # Create a test image
        image = Image.new('RGB', (100, 100), color='red')
        image_file = BytesIO()
        image.save(image_file, 'JPEG')
        image_file.seek(0)
        image_file.name = 'test.jpg'
        
        data = {
            'title': 'Test with file',
            'description': 'Test description',
            'location': 'Test Location',
            'category': category.id,
            'campus': campus.id,
            'uploaded_files': [image_file],
        }
        
        response = authenticated_client.post('/api/complaints/', data, format='multipart')
        
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify file uploaded
        complaint = Complaint.objects.get(tracking_id=response.data['tracking_id'])
        assert complaint.files.count() > 0
    
    def test_create_anonymous_complaint(self, api_client):
        """Test anonymous complaint creation"""
        data = {
            'title': 'Anonymous complaint',
            'description': 'Test description',
            'location': 'Test Location',
        }
        
        response = api_client.post('/api/public/submit/', data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'tracking_id' in response.data


@pytest.mark.django_db
class TestComplaintRetrieval:
    """Test complaint retrieval"""
    
    def test_list_complaints_student(self, authenticated_client, create_complaint):
        """Test student can only see own complaints"""
        # Create complaint for student
        complaint1 = create_complaint(submitter=authenticated_client.user)
        
        # Create complaint for another user
        from django.contrib.auth import get_user_model
        User = get_user_model()
        other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='Pass123!'
        )
        complaint2 = create_complaint(submitter=other_user)
        
        response = authenticated_client.get('/api/complaints/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['id'] == complaint1.id
    
    def test_get_complaint_detail(self, authenticated_client, create_complaint):
        """Test getting complaint details"""
        complaint = create_complaint(submitter=authenticated_client.user)
        
        response = authenticated_client.get(f'/api/complaints/{complaint.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == complaint.id
        assert response.data['title'] == complaint.title
        assert 'files' in response.data
        assert 'comments' in response.data
        assert 'events' in response.data
    
    def test_track_complaint_by_tracking_id(self, api_client, create_complaint, student_user):
        """Test tracking complaint by tracking ID"""
        complaint = create_complaint(submitter=student_user)
        
        response = api_client.get(f'/api/public/track/{complaint.tracking_id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == complaint.title
        assert response.data['status'] == complaint.status


@pytest.mark.django_db
class TestComplaintAssignment:
    """Test complaint assignment"""
    
    def test_assign_complaint(self, api_client, create_complaint, student_user, staff_user, admin_user):
        """Test assigning complaint to staff"""
        complaint = create_complaint(submitter=student_user)
        
        # Login as admin
        from rest_framework.authtoken.models import Token
        token = Token.objects.create(user=admin_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        data = {'assigned_to': staff_user.id}
        response = api_client.post(f'/api/complaints/{complaint.id}/assign/', data)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify assignment
        complaint.refresh_from_db()
        assert complaint.assigned_to == staff_user
        assert complaint.status == 'assigned'
        assert complaint.assigned_at is not None
        
        # Verify event logged
        assert ComplaintEvent.objects.filter(
            complaint=complaint,
            event_type='assigned'
        ).exists()
    
    def test_assign_complaint_permission_denied(self, authenticated_client, create_complaint, staff_user):
        """Test student cannot assign complaints"""
        complaint = create_complaint(submitter=authenticated_client.user)
        
        data = {'assigned_to': staff_user.id}
        response = authenticated_client.post(f'/api/complaints/{complaint.id}/assign/', data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestComplaintStatus:
    """Test complaint status updates"""
    
    def test_update_status(self, api_client, create_complaint, student_user, staff_user):
        """Test updating complaint status"""
        complaint = create_complaint(
            submitter=student_user,
            assigned_to=staff_user,
            status='assigned'
        )
        
        # Login as assigned staff
        from rest_framework.authtoken.models import Token
        token = Token.objects.create(user=staff_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        data = {
            'status': 'in_progress',
            'notes': 'Started working on this'
        }
        response = api_client.post(f'/api/complaints/{complaint.id}/status/', data)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify status updated
        complaint.refresh_from_db()
        assert complaint.status == 'in_progress'
        assert complaint.in_progress_at is not None
        
        # Verify event logged
        event = ComplaintEvent.objects.filter(
            complaint=complaint,
            event_type='status_changed'
        ).first()
        assert event is not None
        assert event.old_value == 'assigned'
        assert event.new_value == 'in_progress'
    
    def test_update_status_permission_denied(self, authenticated_client, create_complaint, staff_user):
        """Test student cannot update status of unassigned complaint"""
        complaint = create_complaint(
            submitter=authenticated_client.user,
            assigned_to=staff_user
        )
        
        data = {'status': 'in_progress'}
        response = authenticated_client.post(f'/api/complaints/{complaint.id}/status/', data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestComplaintComments:
    """Test complaint comments"""
    
    def test_add_comment(self, authenticated_client, create_complaint):
        """Test adding comment to complaint"""
        complaint = create_complaint(submitter=authenticated_client.user)
        
        data = {
            'content': 'This is a test comment',
            'is_internal': False
        }
        response = authenticated_client.post(f'/api/complaints/{complaint.id}/comments/', data)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify comment created
        assert ComplaintComment.objects.filter(
            complaint=complaint,
            author=authenticated_client.user
        ).exists()
        
        # Verify event logged
        assert ComplaintEvent.objects.filter(
            complaint=complaint,
            event_type='comment_added'
        ).exists()
    
    def test_list_comments(self, authenticated_client, create_complaint):
        """Test listing comments"""
        complaint = create_complaint(submitter=authenticated_client.user)
        
        # Create some comments
        ComplaintComment.objects.create(
            complaint=complaint,
            author=authenticated_client.user,
            content='Comment 1'
        )
        ComplaintComment.objects.create(
            complaint=complaint,
            author=authenticated_client.user,
            content='Comment 2'
        )
        
        response = authenticated_client.get(f'/api/complaints/{complaint.id}/comments/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
    
    def test_threaded_comments(self, authenticated_client, create_complaint):
        """Test threaded comment replies"""
        complaint = create_complaint(submitter=authenticated_client.user)
        
        # Create parent comment
        parent = ComplaintComment.objects.create(
            complaint=complaint,
            author=authenticated_client.user,
            content='Parent comment'
        )
        
        # Create reply
        data = {
            'content': 'Reply to parent',
            'parent': parent.id,
            'is_internal': False
        }
        response = authenticated_client.post(f'/api/complaints/{complaint.id}/comments/', data)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify reply created
        reply = ComplaintComment.objects.get(parent=parent)
        assert reply.content == 'Reply to parent'


@pytest.mark.django_db
class TestComplaintFeedback:
    """Test complaint feedback"""
    
    def test_submit_feedback(self, authenticated_client, create_complaint):
        """Test submitting feedback for resolved complaint"""
        complaint = create_complaint(
            submitter=authenticated_client.user,
            status='resolved'
        )
        
        data = {
            'feedback_rating': 5,
            'feedback_comment': 'Excellent service!'
        }
        response = authenticated_client.patch(f'/api/complaints/{complaint.id}/feedback/', data)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify feedback saved
        complaint.refresh_from_db()
        assert complaint.feedback_rating == 5
        assert complaint.feedback_comment == 'Excellent service!'
