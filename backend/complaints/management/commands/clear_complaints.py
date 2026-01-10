"""
Management command to clear all complaints from the database
"""
from django.core.management.base import BaseCommand
from complaints.models import Complaint, ComplaintFile, ComplaintComment, ComplaintEvent
from django.db import transaction


class Command(BaseCommand):
    help = 'Clear all complaints and related data from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without prompting',
        )

    def handle(self, *args, **kwargs):
        confirm = kwargs.get('confirm')
        
        # Count existing data
        complaint_count = Complaint.objects.count()
        file_count = ComplaintFile.objects.count()
        comment_count = ComplaintComment.objects.count()
        event_count = ComplaintEvent.objects.count()
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write('\nCURRENT DATABASE STATUS:')
        self.stdout.write('\n' + '='*60)
        self.stdout.write(f'\nComplaints: {complaint_count}')
        self.stdout.write(f'\nFiles: {file_count}')
        self.stdout.write(f'\nComments: {comment_count}')
        self.stdout.write(f'\nEvents: {event_count}')
        self.stdout.write('\n' + '='*60 + '\n')
        
        if complaint_count == 0:
            self.stdout.write(self.style.SUCCESS('\n✓ Database is already clean!\n'))
            return
        
        if not confirm:
            response = input('\nAre you sure you want to DELETE ALL complaints? (yes/no): ')
            if response.lower() != 'yes':
                self.stdout.write(self.style.WARNING('\nOperation cancelled.\n'))
                return
        
        self.stdout.write('\nDeleting all complaints...')
        
        with transaction.atomic():
            # Delete in order (related objects first)
            ComplaintFile.objects.all().delete()
            ComplaintComment.objects.all().delete()
            ComplaintEvent.objects.all().delete()
            Complaint.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('\n✓ All complaints deleted successfully!\n'))
        self.stdout.write(f'Deleted: {complaint_count} complaints, {file_count} files, ')
        self.stdout.write(f'{comment_count} comments, {event_count} events\n')
