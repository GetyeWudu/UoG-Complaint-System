"""
Management command to check SLA breaches and auto-escalate
Run this periodically (e.g., every hour via cron)
"""
from django.core.management.base import BaseCommand
from complaints.sla_service import check_and_update_sla_breaches, auto_escalate_breached_complaints
from complaints.notifications import send_sla_breach_notification
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Check SLA breaches and auto-escalate complaints'

    def add_arguments(self, parser):
        parser.add_argument(
            '--escalate',
            action='store_true',
            help='Auto-escalate breached complaints',
        )
        parser.add_argument(
            '--notify',
            action='store_true',
            help='Send notifications for SLA breaches',
        )

    def handle(self, *args, **options):
        self.stdout.write('Checking SLA breaches...')
        
        # Check for breaches
        breached = check_and_update_sla_breaches()
        
        if breached:
            self.stdout.write(
                self.style.WARNING(f'Found {len(breached)} SLA breaches')
            )
            
            # Send notifications if requested
            if options['notify']:
                for complaint in breached:
                    try:
                        send_sla_breach_notification(complaint)
                        self.stdout.write(f'Sent notification for {complaint.tracking_id}')
                    except Exception as e:
                        logger.error(f'Failed to send notification for {complaint.tracking_id}: {e}')
            
            # Auto-escalate if requested
            if options['escalate']:
                escalated_count = auto_escalate_breached_complaints()
                self.stdout.write(
                    self.style.SUCCESS(f'Auto-escalated {escalated_count} complaints')
                )
        else:
            self.stdout.write(self.style.SUCCESS('No SLA breaches found'))
        
        self.stdout.write(self.style.SUCCESS('SLA check completed'))

