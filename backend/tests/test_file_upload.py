"""
Tests for file upload functionality
"""
import pytest
from rest_framework import status
from complaints.models import ComplaintFile
from complaints.validators import (
    validate_file_size, validate_file_extension, sanitize_filename
)
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


@pytest.fixture
def create_test_image():
    """Create a test image file"""
    def make_image(format='JPEG', size=(100, 100)):
        image = Image.new('RGB', size, color='red')
        image_file = BytesIO()
        image.save(image_file, format)
        image_file.seek(0)
        return image_file
    return make_image


@pytest.mark.unit
class TestFileValidators:
    """Test file validation functions"""
    
    def test_validate_file_size_success(self):
        """Test file size validation passes for valid file"""
        file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        file.size = 1024 * 1024  # 1MB
        
        # Should not raise exception
        validate_file_size(file)
    
    def test_validate_file_size_too_large(self):
        """Test file size validation fails for large file"""
        file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        file.size = 20 * 1024 * 1024  # 20MB (exceeds 10MB limit)
        
        with pytest.raises(ValidationError):
            validate_file_size(file)
    
    def test_validate_file_extension_success(self):
        """Test file extension validation passes for allowed types"""
        allowed_files = [
            SimpleUploadedFile("test.jpg", b"content", content_type="image/jpeg"),
            SimpleUploadedFile("test.png", b"content", content_type="image/png"),
            SimpleUploadedFile("test.pdf", b"content", content_type="application/pdf"),
        ]
        
        for file in allowed_files:
            validate_file_extension(file)  # Should not raise
    
    def test_validate_file_extension_not_allowed(self):
        """Test file extension validation fails for disallowed types"""
        file = SimpleUploadedFile("test.exe", b"content", content_type="application/x-msdownload")
        
        with pytest.raises(ValidationError):
            validate_file_extension(file)
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        test_cases = [
            ("normal_file.jpg", "normal_file.jpg"),
            ("file with spaces.jpg", "file_with_spaces.jpg"),
            ("../../../etc/passwd", "etcpasswd"),
            ("file<>:\"|?*.jpg", "file.jpg"),
            ("very_long_" + "a" * 200 + ".jpg", "very_long_" + "a" * 91 + ".jpg"),
        ]
        
        for input_name, expected in test_cases:
            result = sanitize_filename(input_name)
            assert len(result) <= 104  # 100 chars + extension


@pytest.mark.django_db
class TestFileUpload:
    """Test file upload endpoints"""
    
    def test_upload_file_to_complaint(self, authenticated_client, create_complaint, create_test_image):
        """Test uploading file to complaint"""
        complaint = create_complaint(submitter=authenticated_client.user)
        
        image_file = create_test_image()
        image_file.name = 'test.jpg'
        
        data = {'files': [image_file]}
        response = authenticated_client.post(
            f'/api/complaints/{complaint.id}/files/',
            data,
            format='multipart'
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data['uploaded']) == 1
        
        # Verify file created
        assert ComplaintFile.objects.filter(complaint=complaint).exists()
    
    def test_upload_multiple_files(self, authenticated_client, create_complaint, create_test_image):
        """Test uploading multiple files"""
        complaint = create_complaint(submitter=authenticated_client.user)
        
        files = []
        for i in range(3):
            image_file = create_test_image()
            image_file.name = f'test{i}.jpg'
            files.append(image_file)
        
        data = {'files': files}
        response = authenticated_client.post(
            f'/api/complaints/{complaint.id}/files/',
            data,
            format='multipart'
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data['uploaded']) == 3
        assert ComplaintFile.objects.filter(complaint=complaint).count() == 3
    
    def test_upload_invalid_file_type(self, authenticated_client, create_complaint):
        """Test uploading invalid file type"""
        complaint = create_complaint(submitter=authenticated_client.user)
        
        file = SimpleUploadedFile("test.exe", b"malicious_content")
        
        data = {'files': [file]}
        response = authenticated_client.post(
            f'/api/complaints/{complaint.id}/files/',
            data,
            format='multipart'
        )
        
        # Should have errors
        assert len(response.data['errors']) > 0
    
    def test_download_file(self, authenticated_client, create_complaint, create_test_image):
        """Test downloading file"""
        complaint = create_complaint(submitter=authenticated_client.user)
        
        # Upload file first
        image_file = create_test_image()
        complaint_file = ComplaintFile.objects.create(
            complaint=complaint,
            uploaded_by=authenticated_client.user,
            file=SimpleUploadedFile("test.jpg", image_file.read(), content_type="image/jpeg"),
            filename="test.jpg",
            file_size=1024,
            mime_type="image/jpeg"
        )
        
        response = authenticated_client.get(f'/api/complaints/files/{complaint_file.id}/download/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'image/jpeg'
    
    def test_download_file_permission_denied(self, api_client, create_complaint, student_user, create_test_image):
        """Test downloading file without permission"""
        # Create complaint for another user
        from django.contrib.auth import get_user_model
        User = get_user_model()
        other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='Pass123!'
        )
        
        complaint = create_complaint(submitter=other_user)
        
        image_file = create_test_image()
        complaint_file = ComplaintFile.objects.create(
            complaint=complaint,
            uploaded_by=other_user,
            file=SimpleUploadedFile("test.jpg", image_file.read(), content_type="image/jpeg"),
            filename="test.jpg",
            file_size=1024,
            mime_type="image/jpeg"
        )
        
        # Login as student_user
        from rest_framework.authtoken.models import Token
        token = Token.objects.create(user=student_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = api_client.get(f'/api/complaints/files/{complaint_file.id}/download/')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_delete_file(self, authenticated_client, create_complaint, create_test_image):
        """Test deleting file"""
        complaint = create_complaint(submitter=authenticated_client.user)
        
        image_file = create_test_image()
        complaint_file = ComplaintFile.objects.create(
            complaint=complaint,
            uploaded_by=authenticated_client.user,
            file=SimpleUploadedFile("test.jpg", image_file.read(), content_type="image/jpeg"),
            filename="test.jpg",
            file_size=1024,
            mime_type="image/jpeg"
        )
        
        response = authenticated_client.delete(f'/api/complaints/files/{complaint_file.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert not ComplaintFile.objects.filter(id=complaint_file.id).exists()
    
    def test_delete_file_permission_denied(self, api_client, create_complaint, student_user, create_test_image):
        """Test deleting file without permission"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='Pass123!'
        )
        
        complaint = create_complaint(submitter=other_user)
        
        image_file = create_test_image()
        complaint_file = ComplaintFile.objects.create(
            complaint=complaint,
            uploaded_by=other_user,
            file=SimpleUploadedFile("test.jpg", image_file.read(), content_type="image/jpeg"),
            filename="test.jpg",
            file_size=1024,
            mime_type="image/jpeg"
        )
        
        # Login as student_user
        from rest_framework.authtoken.models import Token
        token = Token.objects.create(user=student_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = api_client.delete(f'/api/complaints/files/{complaint_file.id}/')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
