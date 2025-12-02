"""
Management command to add tracking IDs to complaints that don't have them
"""
from django.core.management.base import BaseCommand
from complaints.models import Complaint
import uuid


class Command(BaseCommand):
    help = 'Add tracking IDs to complaints that are missing them'

    def handle(self, *args, **kwargs):
        self.stdout.write('Checking for complaints without tracking IDs...\n')
        
        complaints_without_tracking = Complaint.objects.filter(tracking_id__isnull=True) | Complaint.objects.filter(tracking_id='')
        count = complaints_without_tracking.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('✓ All complaints have tracking IDs!'))
            return
        
        self.stdout.write(f'Found {count} complaints without tracking IDs. Fixing...\n')
        
        fixed = 0
        for complaint in complaints_without_tracking:
            track_id = f"CMP-{str(uuid.uuid4())[:8].upper()}"
            complaint.tracking_id = track_id
            complaint.save()
            self.stdout.write(f'  ✓ Fixed complaint #{complaint.id}: {track_id}')
            fixed += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Fixed {fixed} complaints!'))
