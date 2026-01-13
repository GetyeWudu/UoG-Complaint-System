"""
Microsoft OAuth integration for UoG Complaint System
"""
import requests
import secrets
from urllib.parse import urlencode
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from decouple import config
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class MicrosoftOAuthService:
    """Microsoft OAuth 2.0 service for Azure AD integration"""
    
    def __init__(self):
        self.client_id = config('MICROSOFT_CLIENT_ID', default='')
        self.client_secret = config('MICROSOFT_CLIENT_SECRET', default='')
        self.tenant_id = config('MICROSOFT_TENANT_ID', default='common')
        self.redirect_uri = config('MICROSOFT_REDIRECT_URI', default='')
        
        # Microsoft Graph API endpoints
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.authorization_url = f"{self.authority}/oauth2/v2.0/authorize"
        self.token_url = f"{self.authority}/oauth2/v2.0/token"
        self.graph_api_url = "https://graph.microsoft.com/v1.0"
        
        # OAuth scopes
        self.scopes = [
            'openid',
            'profile',
            'email',
            'User.Read'
        ]
    
    def is_configured(self):
        """Check if Microsoft OAuth is properly configured"""
        return bool(
            self.client_id and 
            self.client_secret and 
            self.redirect_uri and
            config('OAUTH_ENABLED', default=False, cast=bool)
        )
    
    def get_authorization_url(self, state=None):
        """
        Generate Microsoft OAuth authorization URL
        
        Args:
            state: Optional state parameter for CSRF protection
            
        Returns:
            dict: Authorization URL and state
        """
        if not self.is_configured():
            raise ValueError("Microsoft OAuth is not properly configured")
        
        if not state:
            state = secrets.token_urlsafe(32)
        
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.scopes),
            'state': state,
            'response_mode': 'query',
            'prompt': 'select_account'  # Allow user to select account
        }
        
        auth_url = f"{self.authorization_url}?{urlencode(params)}"
        
        return {
            'authorization_url': auth_url,
            'state': state
        }
    
    def exchange_code_for_token(self, code, state=None):
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from Microsoft
            state: State parameter for verification
            
        Returns:
            dict: Token response from Microsoft
        """
        if not self.is_configured():
            raise ValueError("Microsoft OAuth is not properly configured")
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.scopes)
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = requests.post(
                self.token_url,
                data=data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            token_data = response.json()
            
            if 'error' in token_data:
                raise Exception(f"Token exchange error: {token_data.get('error_description', token_data['error'])}")
            
            return token_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Microsoft token exchange failed: {e}")
            raise Exception(f"Failed to exchange code for token: {str(e)}")
    
    def get_user_info(self, access_token):
        """
        Get user information from Microsoft Graph API
        
        Args:
            access_token: Microsoft access token
            
        Returns:
            dict: User information from Microsoft Graph
        """
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # Get user profile
            response = requests.get(
                f"{self.graph_api_url}/me",
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            user_data = response.json()
            
            # Normalize user data
            return {
                'id': user_data.get('id'),
                'email': user_data.get('mail') or user_data.get('userPrincipalName'),
                'first_name': user_data.get('givenName', ''),
                'last_name': user_data.get('surname', ''),
                'display_name': user_data.get('displayName', ''),
                'job_title': user_data.get('jobTitle', ''),
                'department': user_data.get('department', ''),
                'office_location': user_data.get('officeLocation', ''),
                'mobile_phone': user_data.get('mobilePhone', ''),
                'business_phones': user_data.get('businessPhones', []),
                'preferred_language': user_data.get('preferredLanguage', 'en'),
                'raw_data': user_data
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Microsoft user info request failed: {e}")
            raise Exception(f"Failed to get user info: {str(e)}")
    
    def create_or_update_user(self, microsoft_user_data, ip_address=None):
        """
        Create or update user based on Microsoft user data
        
        Args:
            microsoft_user_data: User data from Microsoft Graph API
            ip_address: User's IP address
            
        Returns:
            tuple: (User object, created boolean)
        """
        email = microsoft_user_data['email']
        microsoft_id = microsoft_user_data['id']
        
        if not email:
            raise ValueError("Email is required from Microsoft account")
        
        # Try to find existing user by Microsoft ID first
        user = User.objects.filter(oauth_id=microsoft_id, oauth_provider='microsoft').first()
        
        if user:
            # Update existing user with latest Microsoft data
            user.first_name = microsoft_user_data.get('first_name', user.first_name)
            user.last_name = microsoft_user_data.get('last_name', user.last_name)
            user.email = email
            user.last_login_ip = ip_address
            user.oauth_linked_at = timezone.now()
            user.save()
            
            logger.info(f"Updated existing Microsoft user: {user.username}")
            return user, False
        
        # Try to find existing user by email
        user = User.objects.filter(email=email).first()
        
        if user:
            # Link existing account to Microsoft
            user.oauth_provider = 'microsoft'
            user.oauth_id = microsoft_id
            user.oauth_linked_at = timezone.now()
            user.last_login_ip = ip_address
            user.save()
            
            logger.info(f"Linked existing user to Microsoft: {user.username}")
            return user, False
        
        # Create new user
        username = self._generate_username(email, microsoft_user_data)
        
        user = User.objects.create(
            username=username,
            email=email,
            first_name=microsoft_user_data.get('first_name', ''),
            last_name=microsoft_user_data.get('last_name', ''),
            oauth_provider='microsoft',
            oauth_id=microsoft_id,
            oauth_linked_at=timezone.now(),
            last_login_ip=ip_address,
            is_active=True,
            role='student'  # Default role for Microsoft users
        )
        
        # Set unusable password since they'll login via Microsoft
        user.set_unusable_password()
        user.save()
        
        logger.info(f"Created new Microsoft user: {user.username}")
        return user, True
    
    def _generate_username(self, email, microsoft_data):
        """Generate unique username from Microsoft data"""
        # Try email prefix first
        base_username = email.split('@')[0]
        
        # Clean username (remove special characters)
        import re
        base_username = re.sub(r'[^a-zA-Z0-9_]', '', base_username)
        
        # Ensure it's not too long
        base_username = base_username[:20]
        
        # Check if username exists
        username = base_username
        counter = 1
        
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
            
            # Prevent infinite loop
            if counter > 1000:
                username = f"msuser_{secrets.token_hex(4)}"
                break
        
        return username


# Singleton instance
microsoft_oauth_service = MicrosoftOAuthService()