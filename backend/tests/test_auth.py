"""
Tests for authentication endpoints
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from accounts.models import PasswordResetToken, ActivityLog

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration"""
    
    def test_register_success(self, api_client):
        """Test successful user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'NewPass123!',
            'password_confirm': 'NewPass123!',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'student'
        }
        
        response = api_client.post('/api/auth/register/', data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'token' in response.data
        assert 'user' in response.data
        assert response.data['user']['username'] == 'newuser'
        
        # Verify user created
        user = User.objects.get(username='newuser')
        assert user.email == 'newuser@example.com'
        assert user.check_password('NewPass123!')
    
    def test_register_password_mismatch(self, api_client):
        """Test registration with mismatched passwords"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'NewPass123!',
            'password_confirm': 'DifferentPass123!',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'student'
        }
        
        response = api_client.post('/api/auth/register/', data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_weak_password(self, api_client):
        """Test registration with weak password"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'weak',
            'password_confirm': 'weak',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'student'
        }
        
        response = api_client.post('/api/auth/register/', data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_duplicate_email(self, api_client, student_user):
        """Test registration with duplicate email"""
        data = {
            'username': 'newuser',
            'email': student_user.email,
            'password': 'NewPass123!',
            'password_confirm': 'NewPass123!',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'student'
        }
        
        response = api_client.post('/api/auth/register/', data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserLogin:
    """Test user login"""
    
    def test_login_success(self, api_client, student_user):
        """Test successful login"""
        data = {
            'username': student_user.username,
            'password': 'TestPass123!'
        }
        
        response = api_client.post('/api/auth/login/', data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        assert response.data['username'] == student_user.username
        assert response.data['role'] == 'student'
        
        # Verify activity log
        assert ActivityLog.objects.filter(
            user=student_user,
            action='login'
        ).exists()
    
    def test_login_invalid_credentials(self, api_client, student_user):
        """Test login with invalid credentials"""
        data = {
            'username': student_user.username,
            'password': 'WrongPassword'
        }
        
        response = api_client.post('/api/auth/login/', data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # Verify failed login logged
        assert ActivityLog.objects.filter(
            user=student_user,
            action='login_failed'
        ).exists()
    
    def test_login_account_lockout(self, api_client, student_user):
        """Test account lockout after multiple failed attempts"""
        data = {
            'username': student_user.username,
            'password': 'WrongPassword'
        }
        
        # Make 5 failed attempts
        for _ in range(5):
            api_client.post('/api/auth/login/', data)
        
        # Verify account is locked
        student_user.refresh_from_db()
        assert student_user.failed_login_attempts >= 5
        assert student_user.account_locked_until is not None
        
        # Try to login with correct password
        data['password'] = 'TestPass123!'
        response = api_client.post('/api/auth/login/', data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestPasswordReset:
    """Test password reset"""
    
    def test_password_reset_request(self, api_client, student_user):
        """Test password reset request"""
        data = {'email': student_user.email}
        
        response = api_client.post('/api/auth/password-reset/request/', data)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify token created
        assert PasswordResetToken.objects.filter(user=student_user).exists()
        
        # Verify activity log
        assert ActivityLog.objects.filter(
            user=student_user,
            action='password_reset_request'
        ).exists()
    
    def test_password_reset_confirm(self, api_client, student_user):
        """Test password reset confirmation"""
        # Create reset token
        from django.utils import timezone
        from datetime import timedelta
        import secrets
        
        token = secrets.token_urlsafe(32)
        reset_token = PasswordResetToken.objects.create(
            user=student_user,
            token=token,
            expires_at=timezone.now() + timedelta(hours=1)
        )
        
        data = {
            'token': token,
            'password': 'NewPassword123!',
            'password_confirm': 'NewPassword123!'
        }
        
        response = api_client.post('/api/auth/password-reset/confirm/', data)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify password changed
        student_user.refresh_from_db()
        assert student_user.check_password('NewPassword123!')
        
        # Verify token marked as used
        reset_token.refresh_from_db()
        assert reset_token.used is True
    
    def test_password_reset_expired_token(self, api_client, student_user):
        """Test password reset with expired token"""
        from django.utils import timezone
        from datetime import timedelta
        import secrets
        
        token = secrets.token_urlsafe(32)
        PasswordResetToken.objects.create(
            user=student_user,
            token=token,
            expires_at=timezone.now() - timedelta(hours=1)  # Expired
        )
        
        data = {
            'token': token,
            'password': 'NewPassword123!',
            'password_confirm': 'NewPassword123!'
        }
        
        response = api_client.post('/api/auth/password-reset/confirm/', data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserProfile:
    """Test user profile endpoints"""
    
    def test_get_current_user(self, authenticated_client):
        """Test getting current user profile"""
        response = authenticated_client.get('/api/auth/me/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == authenticated_client.user.username
    
    def test_update_current_user(self, authenticated_client):
        """Test updating current user profile"""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        response = authenticated_client.patch('/api/auth/me/', data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'
        assert response.data['last_name'] == 'Name'
