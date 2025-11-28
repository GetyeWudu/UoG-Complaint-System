"""
Notification system for complaint status changes
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template import Template, Context
from .models import EmailTemplate
import logging

logger = logging.getLogger(__name__)


def send_complaint_notification(complaint, event_type, additional_context=None):
    """
    Send notification email when complaint status changes
    
    Args:
        complaint: Complaint object
        event_type: Type of event (reviewed, assigned, in_progress, resolved, rejected, closed)
        additional_context: Additional context for email template
    """
    if not complaint.submitter or not complaint.submitter.email:
        return
    
    # Don't send to anonymous complaints without email
    if complaint.is_anonymous and not complaint.anonymous_email:
        return
    
    recipient_email = complaint.anonymous_email if complaint.is_anonymous else complaint.submitter.email
    recipient_name = 'User' if complaint.is_anonymous else (complaint.submitter.get_full_name() or complaint.submitter.username)
    
    # Email templates for different events
    templates = {
        'reviewed': {
            'subject': 'Your Complaint Has Been Reviewed - {tracking_id}',
            'message': '''
Dear {recipient_name},

Your complaint has been reviewed by our team.

Complaint Details:
- Tracking ID: {tracking_id}
- Title: {title}
- Status: {status}
- Priority: {priority}

{additional_message}

You can track your complaint status at any time using your tracking ID.

Best regards,
UoG Complaint Management Team
            '''
        },
        'assigned': {
            'subject': 'Your Complaint Has Been Assigned - {tracking_id}',
            'message': '''
Dear {recipient_name},

Your complaint has been assigned to a staff member for resolution.

Complaint Details:
- Tracking ID: {tracking_id}
- Title: {title}
- Assigned to: {assigned_to}
- Status: Assigned

We will keep you updated on the progress.

Best regards,
UoG Complaint Management Team
            '''
        },
        'in_progress': {
            'subject': 'Your Complaint is Being Processed - {tracking_id}',
            'message': '''
Dear {recipient_name},

Your complaint is now being actively worked on.

Complaint Details:
- Tracking ID: {tracking_id}
- Title: {title}
- Status: In Progress
- Assigned to: {assigned_to}

We are working to resolve your issue as quickly as possible.

Best regards,
UoG Complaint Management Team
            '''
        },
        'resolved': {
            'subject': 'Your Complaint Has Been Resolved - {tracking_id}',
            'message': '''
Dear {recipient_name},

Great news! Your complaint has been resolved.

Complaint Details:
- Tracking ID: {tracking_id}
- Title: {title}
- Status: Resolved
- Resolution Notes: {resolution_notes}

If you are satisfied with the resolution, no further action is needed.
If you have any concerns, please contact us.

Best regards,
UoG Complaint Management Team
            '''
        },
        'rejected': {
            'subject': 'Complaint Status Update - {tracking_id}',
            'message': '''
Dear {recipient_name},

We have reviewed your complaint and unfortunately cannot proceed with it at this time.

Complaint Details:
- Tracking ID: {tracking_id}
- Title: {title}
- Status: Rejected
- Reason: {rejection_reason}

If you have questions about this decision, please contact our support team.

Best regards,
UoG Complaint Management Team
            '''
        },
        'closed': {
            'subject': 'Your Complaint Has Been Closed - {tracking_id}',
            'message': '''
Dear {recipient_name},

Your complaint has been closed.

Complaint Details:
- Tracking ID: {tracking_id}
- Title: {title}
- Status: Closed
- Final Resolution: {resolution_notes}

Thank you for using the UoG Complaint Management System.

Best regards,
UoG Complaint Management Team
            '''
        }
    }
    
    if event_type not in templates:
        logger.warning(f"Unknown notification event type: {event_type}")
        return
    
    template = templates[event_type]
    
    # Build context
    context = {
        'recipient_name': recipient_name,
        'tracking_id': complaint.tracking_id,
        'title': complaint.title,
        'status': complaint.get_status_display(),
        'priority': complaint.get_urgency_display() if complaint.urgency else 'Not set',
        'assigned_to': complaint.assigned_to.get_full_name() if complaint.assigned_to else 'Not assigned',
        'resolution_notes': complaint.resolution_notes or 'No notes provided',
        'rejection_reason': complaint.rejection_reason or 'No reason provided',
        'additional_message': ''
    }
    
    # Add additional context if provided
    if additional_context:
        context.update(additional_context)
    
    # Format subject and message
    subject = template['subject'].format(**context)
    message = template['message'].format(**context)
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        logger.info(f"Notification sent to {recipient_email} for complaint {complaint.tracking_id}")
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")


def notify_complaint_reviewed(complaint):
    """Send notification when admin reviews a complaint"""
    send_complaint_notification(
        complaint, 
        'reviewed',
        {'additional_message': 'Our team has reviewed your complaint and will take appropriate action.'}
    )


def notify_complaint_assigned(complaint):
    """Send notification when complaint is assigned"""
    send_complaint_notification(complaint, 'assigned')


def notify_complaint_in_progress(complaint):
    """Send notification when complaint status changes to in progress"""
    send_complaint_notification(complaint, 'in_progress')


def notify_complaint_resolved(complaint):
    """Send notification when complaint is resolved"""
    send_complaint_notification(complaint, 'resolved')


def notify_complaint_rejected(complaint):
    """Send notification when complaint is rejected"""
    send_complaint_notification(complaint, 'rejected')


def notify_complaint_closed(complaint):
    """Send notification when complaint is closed"""
    send_complaint_notification(complaint, 'closed')
