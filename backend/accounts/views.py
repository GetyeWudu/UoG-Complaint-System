from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import secrets
import logging

from .models import PasswordResetToken, ActivityLog, Campus, Department
from .serializers import (
    UserRegistrationSerializer, UserSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer, PasswordChangeSerializer, OAuthLinkSerializer,
    CampusSerializer, DepartmentSerializer, ActivityLogSerializer
)
from .utils import send_email, get_client_ip

User = get_user_model()
logger = logging.getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Log activity
        ActivityLog.objects.create(
            user=user,
            action='register',
            description=f'User {user.username} registered',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Create token
        token, created = Token.objects.get_or_create(user=user)
        
        # Send welcome email
        send_email(
            template_type='welcome',
            recipient=user.email,
            context={
                'user_name': user.get_full_name() or user.username,
                'username': user.username,
                'frontend_url': settings.FRONTEND_URL,
            }
        )
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)


class CustomAuthToken(ObtainAuthToken):
    """
    Enhanced login endpoint with activity logging
    POST /api/auth/login/
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            
            # Check if account is locked
            if user.account_locked_until and user.account_locked_until > timezone.now():
                return Response({
                    'error': 'Account is temporarily locked due to multiple failed login attempts. Please try again later.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Reset failed login attempts on successful login
            user.failed_login_attempts = 0
            user.account_locked_until = None
            user.last_login_ip = get_client_ip(request)
            user.save()
            
            # Get or create token
            token, created = Token.objects.get_or_create(user=user)
            
            # Log successful login
            ActivityLog.objects.create(
                user=user,
                action='login',
                description=f'User {user.username} logged in',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'department': user.department.name if user.department else None,
                'campus': user.campus.name if user.campus else None,
            })
            
        except Exception as e:
            # Handle failed login
            username = request.data.get('username')
            if username:
                try:
                    user = User.objects.get(username=username)
                    user.failed_login_attempts += 1
                    
                    # Lock account after 5 failed attempts
                    if user.failed_login_attempts >= 5:
                        user.account_locked_until = timezone.now() + timedelta(minutes=15)
                    
                    user.save()
                    
                    # Log failed login
                    ActivityLog.objects.create(
                        user=user,
                        action='login_failed',
                        description=f'Failed login attempt for {username}',
                        ip_address=get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                except User.DoesNotExist:
                    pass
            
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    Logout endpoint - deletes auth token
    POST /api/auth/logout/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action='logout',
            description=f'User {request.user.username} logged out',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Delete token
        request.user.auth_token.delete()
        
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    """
    Request password reset - sends email with reset token
    POST /api/auth/password-reset/request/
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Generate secure token
        token = secrets.token_urlsafe(32)
        
        # Create reset token
        reset_token = PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timedelta(hours=1),
            ip_address=get_client_ip(request)
        )
        
        # Log activity
        ActivityLog.objects.create(
            user=user,
            action='password_reset_request',
            description=f'Password reset requested for {user.username}',
            ip_address=get_client_ip(request)
        )
        
        # Send reset email
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        send_email(
            template_type='password_reset',
            recipient=user.email,
            context={
                'user_name': user.get_full_name() or user.username,
                'reset_url': reset_url,
                'token': token,
                'expires_in': '1 hour',
            }
        )
        
        return Response({
            'message': 'Password reset email sent. Please check your inbox.'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Confirm password reset with token
    POST /api/auth/password-reset/confirm/
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']
        
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            
            if not reset_token.is_valid():
                return Response({
                    'error': 'Invalid or expired reset token'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update password
            user = reset_token.user
            user.set_password(password)
            user.failed_login_attempts = 0
            user.account_locked_until = None
            user.save()
            
            # Mark token as used
            reset_token.used = True
            reset_token.used_at = timezone.now()
            reset_token.save()
            
            # Log activity
            ActivityLog.objects.create(
                user=user,
                action='password_reset_complete',
                description=f'Password reset completed for {user.username}',
                ip_address=get_client_ip(request)
            )
            
            return Response({
                'message': 'Password reset successful. You can now login with your new password.'
            }, status=status.HTTP_200_OK)
            
        except PasswordResetToken.DoesNotExist:
            return Response({
                'error': 'Invalid reset token'
            }, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    """
    Change password for authenticated user
    POST /api/auth/password-change/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Log activity
        ActivityLog.objects.create(
            user=user,
            action='password_change',
            description=f'Password changed for {user.username}',
            ip_address=get_client_ip(request)
        )
        
        # Delete old token and create new one
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        
        return Response({
            'message': 'Password changed successfully',
            'token': token.key
        }, status=status.HTTP_200_OK)


class OAuthCallbackView(APIView):
    """
    OAuth callback endpoint - handles OAuth provider callback
    POST /api/auth/oauth/callback/
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        # This is a scaffold for OAuth integration
        # In production, this would:
        # 1. Receive authorization code from OAuth provider
        # 2. Exchange code for access token
        # 3. Fetch user info from provider
        # 4. Create or link user account
        
        if not settings.OAUTH_ENABLED:
            return Response({
                'error': 'OAuth is not enabled. Please configure OAuth settings in .env file.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Placeholder implementation
        return Response({
            'message': 'OAuth integration is configured but requires UoG-specific implementation.',
            'instructions': 'Please provide OAuth client credentials in .env file and implement provider-specific logic.'
        }, status=status.HTTP_501_NOT_IMPLEMENTED)


class OAuthLinkView(APIView):
    """
    Link OAuth account to existing user
    POST /api/auth/oauth/link/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = OAuthLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Check if OAuth account is already linked to another user
        existing_user = User.objects.filter(
            oauth_provider=serializer.validated_data['oauth_provider'],
            oauth_id=serializer.validated_data['oauth_id']
        ).exclude(id=user.id).first()
        
        if existing_user:
            return Response({
                'error': 'This OAuth account is already linked to another user.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Link OAuth account
        user.oauth_provider = serializer.validated_data['oauth_provider']
        user.oauth_id = serializer.validated_data['oauth_id']
        user.oauth_linked_at = timezone.now()
        user.save()
        
        # Log activity
        ActivityLog.objects.create(
            user=user,
            action='oauth_linked',
            description=f'OAuth account linked for {user.username}',
            ip_address=get_client_ip(request),
            metadata={'provider': user.oauth_provider}
        )
        
        return Response({
            'message': 'OAuth account linked successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    """
    Get current authenticated user details
    GET /api/auth/me/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        """Update current user profile"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)


# Utility Views
class CampusListView(generics.ListAPIView):
    """List all campuses"""
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    permission_classes = [permissions.AllowAny]


class DepartmentListView(generics.ListAPIView):
    """List all departments"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]


class ActivityLogListView(generics.ListAPIView):
    """
    List activity logs (admin only)
    GET /api/auth/activity-logs/
    """
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Only admins and super admins can see all logs
        if user.role in ['admin', 'super_admin']:
            return ActivityLog.objects.all()
        
        # Regular users can only see their own logs
        return ActivityLog.objects.filter(user=user)
