"""
Management command to seed comprehensive categories and subcategories
"""
from django.core.management.base import BaseCommand
from complaints.models import Category, SubCategory


class Command(BaseCommand):
    help = 'Seed comprehensive categories and subcategories for UoG complaint system'

    def handle(self, *args, **options):
        self.stdout.write('Seeding categories and subcategories...')
        
        categories_data = {
            'Academic': [
                'Grade Dispute',
                'Exam Irregularity',
                'Instructor Conduct',
                'Course Content',
                'Syllabus Issue',
                'Academic Calendar',
                'Course Registration',
                'Transcript Request'
            ],
            'Facilities / Infrastructure': [
                'Electricity',
                'Water',
                'Classroom Furniture',
                'Restroom',
                'HVAC',
                'Projector/AV',
                'Building Maintenance',
                'Lighting',
                'Doors/Windows',
                'Roof/Leakage'
            ],
            'Administrative': [
                'Registration',
                'Transcript',
                'ID Card',
                'Scheduling',
                'Bursar/Fees',
                'Document Request',
                'Administrative Process'
            ],
            'Housing / Accommodation': [
                'Room Allocation',
                'Maintenance',
                'Safety',
                'Roommate Conflict',
                'Housing Application',
                'Dormitory Facilities'
            ],
            'Security / Safety': [
                'Theft',
                'Harassment',
                'Assault',
                'Campus Lighting',
                'Emergency Response',
                'Security Personnel',
                'Access Control'
            ],
            'IT / Network': [
                'WiFi',
                'LMS Access',
                'Email',
                'Computer Lab Hardware',
                'Service Outage',
                'Software Issues',
                'Network Connectivity',
                'Account Access'
            ],
            'Health / Medical': [
                'Clinic Services',
                'Medical Referral',
                'Mental Health Support',
                'Health Insurance',
                'Emergency Medical'
            ],
            'Transport': [
                'Shuttle Service',
                'Drivers',
                'Timetable Complaints',
                'Vehicle Maintenance',
                'Route Issues'
            ],
            'HR / Staff Conduct': [
                'Unprofessional Behavior',
                'Discrimination',
                'Harassment',
                'Staff Performance',
                'Workplace Issues'
            ],
            'Library': [
                'Borrowing',
                'Access',
                'Noise',
                'Resource Availability',
                'Library Services',
                'Study Space'
            ],
            'Other': [
                'Miscellaneous',
                'Suggestions',
                'General Inquiry',
                'Feedback'
            ]
        }
        
        created_count = 0
        subcategory_count = 0
        
        for category_name, subcategories in categories_data.items():
            # Create or get category
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'description': f'{category_name} related complaints'}
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'Created category: {category_name}')
            else:
                self.stdout.write(f'Category already exists: {category_name}')
            
            # Create subcategories
            for subcat_name in subcategories:
                subcat, created = SubCategory.objects.get_or_create(
                    category=category,
                    name=subcat_name,
                    defaults={'description': f'{subcat_name} under {category_name}'}
                )
                if created:
                    subcategory_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded {created_count} categories and {subcategory_count} subcategories'
            )
        )

