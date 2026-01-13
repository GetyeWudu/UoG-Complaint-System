from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from decouple import config
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
from .microsoft_oauth import microsoft_oauth_service

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
    Accepts username OR email
    POST /api/auth/login/
    """
    def post(self, request, *args, **kwargs):
        username_or_email = request.data.get('username', '')
        password = request.data.get('password', '')
        
        # Try to find user by username or email
        user = None
        try:
            # First try username
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            # Then try email
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                pass
        
        # Validate password
        if not user or not user.check_password(password):
            # Handle failed login
            if user:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 5:
                    user.account_locked_until = timezone.now() + timedelta(minutes=15)
                user.save()
                
                ActivityLog.objects.create(
                    user=user,
                    action='login_failed',
                    description=f'Failed login attempt for {username_or_email}',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
            
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            
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


class MicrosoftOAuthInitiateView(APIView):
    """
    Initiate Microsoft OAuth login
    GET /api/auth/microsoft/login/
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            if not microsoft_oauth_service.is_configured():
                return Response({
                    'error': 'Microsoft OAuth is not configured. Please check your environment variables.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate authorization URL
            auth_data = microsoft_oauth_service.get_authorization_url()
            
            # Store state in session for verification
            request.session['oauth_state'] = auth_data['state']
            
            return Response({
                'authorization_url': auth_data['authorization_url'],
                'state': auth_data['state']
            })
            
        except Exception as e:
            logger.error(f"Microsoft OAuth initiate error: {e}")
            return Response({
                'error': f'Failed to initiate Microsoft login: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MicrosoftOAuthCallbackView(APIView):
    """
    Handle Microsoft OAuth callback
    Supports both GET (redirect from Microsoft) and POST (from frontend)
    GET/POST /api/auth/microsoft/callback/
    """
    permission_classes = [permissions.AllowAny]
    
    def _process_callback(self, code, state, error, error_description, request):
        """Process OAuth callback - shared logic for GET and POST"""
        try:
            # Check for OAuth errors
            if error:
                error_msg = error_description or error
                return {
                    'success': False,
                    'error': f'Microsoft OAuth error: {error_msg}'
                }
            
            if not code:
                return {
                    'success': False,
                    'error': 'Authorization code is required'
                }
            
            # Verify state parameter (CSRF protection)
            # Note: We verify state from the request data since Django sessions
            # may not persist across the Microsoft redirect. The frontend stores
            # the state in sessionStorage and sends it back for verification.
            # Additional validation: state should be a valid token format
            if not state or len(state) < 20:
                return {
                    'success': False,
                    'error': 'Invalid state parameter. Possible CSRF attack.'
                }
            
            # Optional: Verify against stored state if session is available
            # This provides additional security but won't fail if session is lost
            stored_state = request.session.get('oauth_state')
            if stored_state and stored_state != state:
                logger.warning(f"State mismatch: stored={stored_state[:10]}..., received={state[:10]}...")
                return {
                    'success': False,
                    'error': 'Invalid state parameter. Possible CSRF attack.'
                }
            
            # Exchange code for token
            token_data = microsoft_oauth_service.exchange_code_for_token(code, state)
            access_token = token_data['access_token']
            
            # Get user info from Microsoft Graph
            microsoft_user_data = microsoft_oauth_service.get_user_info(access_token)
            
            # Create or update user
            user, created = microsoft_oauth_service.create_or_update_user(
                microsoft_user_data,
                ip_address=get_client_ip(request)
            )
            
            # Create Django auth token
            token, _ = Token.objects.get_or_create(user=user)
            
            # Log activity
            action = 'microsoft_register' if created else 'microsoft_login'
            ActivityLog.objects.create(
                user=user,
                action=action,
                description=f'User {user.username} {"registered" if created else "logged in"} via Microsoft OAuth',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                metadata={
                    'provider': 'microsoft',
                    'microsoft_id': microsoft_user_data['id']
                }
            )
            
            # Clear OAuth state from session
            if 'oauth_state' in request.session:
                del request.session['oauth_state']
            
            return {
                'success': True,
                'token': token.key,
                'user': UserSerializer(user).data,
                'created': created,
                'message': 'Successfully authenticated with Microsoft'
            }
            
        except Exception as e:
            logger.error(f"Microsoft OAuth callback error: {e}")
            return {
                'success': False,
                'error': f'Microsoft authentication failed: {str(e)}'
            }
    
    def get(self, request):
        """Handle GET request from Microsoft redirect"""
        from django.shortcuts import redirect
        from django.conf import settings
        from urllib.parse import urlencode
        
        code = request.GET.get('code')
        state = request.GET.get('state')
        error = request.GET.get('error')
        error_description = request.GET.get('error_description')
        
        # Process the callback
        result = self._process_callback(code, state, error, error_description, request)
        
        # Get frontend URL from settings
        frontend_url = config('FRONTEND_URL', default='http://localhost:5173')
        callback_url = f"{frontend_url}/auth/microsoft/callback"
        
        if result['success']:
            # Redirect to frontend with token
            # Store user data in session temporarily for frontend to retrieve
            request.session['oauth_user_data'] = result['user']
            request.session['oauth_token'] = result['token']
            from urllib.parse import quote
            # URL encode the token to handle special characters
            encoded_token = quote(result['token'], safe='')
            redirect_url = f"{callback_url}?token={encoded_token}&success=true"
            return redirect(redirect_url)
        else:
            # Redirect to frontend with error
            from urllib.parse import quote
            error_msg = result.get('error', 'Authentication failed')
            redirect_url = f"{callback_url}?error={quote(error_msg)}"
            return redirect(redirect_url)
    
    def post(self, request):
        """Handle POST request from frontend"""
        code = request.data.get('code')
        state = request.data.get('state')
        error = request.data.get('error')
        error_description = request.data.get('error_description')
        
        # Process the callback using shared logic
        result = self._process_callback(code, state, error, error_description, request)
        
        if result['success']:
            return Response({
                'token': result['token'],
                'user': result['user'],
                'created': result.get('created', False),
                'message': result.get('message', 'Successfully authenticated with Microsoft')
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result.get('error', 'Microsoft authentication failed')
            }, status=status.HTTP_400_BAD_REQUEST)


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


class UserListView(generics.ListAPIView):
    """
    Get list of all users (for assignment dropdown)
    GET /api/auth/users/
    """
    queryset = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter users based on role permissions"""
        user = self.request.user
        queryset = super().get_queryset()
        
        # Super admin and admin can see all users
        if user.role in ['super_admin', 'admin']:
            return queryset
        
        # Department heads can see users in their department
        if user.role == 'dept_head' and user.department:
            return queryset.filter(department=user.department)
        
        # Deans can see users in their college
        if user.role == 'dean':
            # Get all departments in dean's college
            from .models import College
            colleges = College.objects.filter(dean=user)
            dept_ids = []
            for college in colleges:
                dept_ids.extend(college.department_set.values_list('id', flat=True))
            return queryset.filter(department__id__in=dept_ids)
        
        # Others can only see users in their campus
        if user.campus:
            return queryset.filter(campus=user.campus)
        
        return queryset


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
