"""
Utility functions for accounts app
"""
from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context
from django.conf import settings
from complaints.models import EmailTemplate
import logging

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """
    Extract client IP address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_email(template_type, recipient, context, subject=None):
    """
    Send email using template
    
    Args:
        template_type: Type of email template (e.g., 'welcome', 'password_reset')
        recipient: Email address of recipient
        context: Dictionary of template variables
        subject: Optional subject override
    """
    try:
        # Try to get template from database
        try:
            email_template = EmailTemplate.objects.get(
                template_type=template_type,
                is_active=True
            )
            
            # Render subject
            subject_template = Template(email_template.subject)
            email_subject = subject_template.render(Context(context))
            
            # Render HTML content
            html_template = Template(email_template.html_content)
            html_content = html_template.render(Context(context))
            
            # Render text content
            text_template = Template(email_template.text_content)
            text_content = text_template.render(Context(context))
            
        except EmailTemplate.DoesNotExist:
            # Fallback to default templates
            email_subject, html_content, text_content = get_default_template(template_type, context)
        
        # Override subject if provided
        if subject:
            email_subject = subject
        
        # Create email
        email = EmailMultiAlternatives(
            subject=email_subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient]
        )
        
        # Attach HTML version
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        email.send(fail_silently=False)
        
        logger.info(f"Email sent successfully to {recipient} (type: {template_type})")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {recipient}: {str(e)}")
        return False


def get_default_template(template_type, context):
    """
    Get default email template if database template doesn't exist
    """
    templates = {
        'welcome': {
            'subject': 'Welcome to UoG Complaint Management System',
            'html': '''
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #003366;">Welcome to UoG Complaint Management System</h2>
                        <p>Dear {user_name},</p>
                        <p>Your account has been successfully created!</p>
                        <p><strong>Username:</strong> {username}</p>
                        <p>You can now login and submit complaints or track existing ones.</p>
                        <p><a href="{frontend_url}" style="background-color: #003366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Login Now</a></p>
                        <p>Thank you,<br>University of Gondar<br>Complaint Management Team</p>
                    </div>
                </body>
                </html>
            ''',
            'text': '''
                Welcome to UoG Complaint Management System
                
                Dear {user_name},
                
                Your account has been successfully created!
                
                Username: {username}
                
                You can now login and submit complaints or track existing ones.
                
                Login at: {frontend_url}
                
                Thank you,
                University of Gondar
                Complaint Management Team
            '''
        },
        'password_reset': {
            'subject': 'Password Reset Request - UoG Complaint System',
            'html': '''
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #003366;">Password Reset Request</h2>
                        <p>Dear {user_name},</p>
                        <p>We received a request to reset your password. Click the button below to reset it:</p>
                        <p><a href="{reset_url}" style="background-color: #003366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Reset Password</a></p>
                        <p>Or copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; color: #666;">{reset_url}</p>
                        <p><strong>This link will expire in {expires_in}.</strong></p>
                        <p>If you didn't request this, please ignore this email.</p>
                        <p>Thank you,<br>University of Gondar<br>Complaint Management Team</p>
                    </div>
                </body>
                </html>
            ''',
            'text': '''
                Password Reset Request - UoG Complaint System
                
                Dear {user_name},
                
                We received a request to reset your password.
                
                Click this link to reset your password:
                {reset_url}
                
                This link will expire in {expires_in}.
                
                If you didn't request this, please ignore this email.
                
                Thank you,
                University of Gondar
                Complaint Management Team
            '''
        },
    }
    
    template = templates.get(template_type, templates['welcome'])
    
    # Format templates with context
    subject = template['subject'].format(**context)
    html_content = template['html'].format(**context)
    text_content = template['text'].format(**context)
    
    return subject, html_content, text_content


def validate_password_strength(password):
    """
    Additional password strength validation
    Returns tuple: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter"
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(char in special_chars for char in password):
        return False, "Password must contain at least one special character"
    
    return True, ""
