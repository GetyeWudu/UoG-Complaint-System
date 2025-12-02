"""
Management command to create old complaints for SLA testing
"""
from django.core.management.base import BaseCommand
from complaints.models import Complaint
from accounts.models import CustomUser, Department
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Create old complaints to test SLA breaches'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating old complaints for SLA testing...\n')
        
        # Get student and department
        student = CustomUser.objects.filter(role='student').first()
        department = Department.objects.first()
        
        if not student or not department:
            self.stdout.write(self.style.ERROR('Need at least one student and department'))
            return
        
        # Create complaints with different ages
        test_complaints = [
            {
                'title': 'SLA Test: 5 days old - BREACHED',
                'description': 'This complaint is 5 days old and unresolved. SLA should be breached.',
                'days_old': 5,
                'priority': 'medium',  # Medium = 3 days resolution SLA
                'status': 'new'
            },
            {
                'title': 'SLA Test: 2 days old - HIGH priority BREACHED',
                'description': 'High priority complaint from 2 days ago. Should breach 24-hour SLA.',
                'days_old': 2,
                'priority': 'high',  # High = 1 day resolution SLA
                'status': 'assigned'
            },
            {
                'title': 'SLA Test: 10 hours old - CRITICAL BREACHED',
                'description': 'Critical complaint from 10 hours ago. Should breach 4-hour SLA.',
                'hours_old': 10,
                'priority': 'critical',  # Critical = 4 hours resolution SLA
                'status': 'in_progress'
            },
            {
                'title': 'SLA Test: 1 day old - Within SLA',
                'description': 'Low priority complaint. Still within 7-day SLA.',
                'days_old': 1,
                'priority': 'low',  # Low = 7 days resolution SLA
                'status': 'new'
            }
        ]
        
        created_count = 0
        for data in test_complaints:
            # Calculate creation time
            if 'days_old' in data:
                created_at = timezone.now() - timedelta(days=data['days_old'])
            else:
                created_at = timezone.now() - timedelta(hours=data['hours_old'])
            
            # Create complaint
            complaint = Complaint.objects.create(
                title=data['title'],
                description=data['description'],
                location='Test Location',
                status=data['status'],
                priority=data['priority'],
                urgency=data['priority'],
                submitter=student,
                department=department,
                tracking_id=f"SLA-{timezone.now().strftime('%H%M%S')}-{created_count+1}"
            )
            
            # Manually set created_at (bypass auto_now_add)
            Complaint.objects.filter(id=complaint.id).update(created_at=created_at)
            
            # Apply SLA
            from complaints.sla_service import apply_sla_to_complaint
            complaint.refresh_from_db()
            apply_sla_to_complaint(complaint)
            
            # Check if breached (will be done by the periodic task, but we can trigger manually)
            complaint.refresh_from_db()
            
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Created: {complaint.tracking_id} - {data["priority"].upper()} - '
                    f'{"BREACHED" if complaint.sla_resolution_breached else "OK"}'
                )
            )
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'\n✓ Created {created_count} test complaints'))
        self.stdout.write('\n' + '='*60)
        self.stdout.write('\nNow you can test SLA tracking:')
        self.stdout.write('\n1. Login as admin/depthead/director')
        self.stdout.write('\n2. Check dashboard for "SLA Breaches" count')
        self.stdout.write('\n3. Open complaints with "SLA Test" in title')
        self.stdout.write('\n4. Look for red SLA warnings')
        self.stdout.write('\n' + '='*60 + '\n')
