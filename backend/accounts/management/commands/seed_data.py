"""
Management command to seed the database with test data
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Campus, College, Department
from complaints.models import Category, SubCategory, EmailTemplate, RoutingRule
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with test data for UoG Complaint System'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))
        
        # Create Campuses
        self.stdout.write('Creating campuses...')
        tewodros = Campus.objects.get_or_create(name='Tewodros Campus')[0]
        maraki = Campus.objects.get_or_create(name='Maraki Campus')[0]
        cmhs = Campus.objects.get_or_create(name='CMHS Campus')[0]
        
        # Create Colleges
        self.stdout.write('Creating colleges...')
        coi = College.objects.get_or_create(
            name='College of Informatics',
            defaults={'campus': tewodros}
        )[0]
        
        cncs = College.objects.get_or_create(
            name='College of Natural and Computational Sciences',
            defaults={'campus': tewodros}
        )[0]
        
        # Create Departments
        self.stdout.write('Creating departments...')
        cs_dept = Department.objects.get_or_create(
            name='Computer Science',
            defaults={'college': coi}
        )[0]
        
        it_dept = Department.objects.get_or_create(
            name='Information Technology',
            defaults={'college': coi}
        )[0]
        
        bio_dept = Department.objects.get_or_create(
            name='Biology',
            defaults={'college': cncs}
        )[0]
        
        maintenance_dept = Department.objects.get_or_create(
            name='Campus Maintenance',
            defaults={'college': coi}
        )[0]
        
        # Create Test Users
        self.stdout.write('Creating test users...')
        
        users_data = [
            {
                'username': 'student@example.com',
                'email': 'student@example.com',
                'password': 'Student123!',
                'role': 'student',
                'first_name': 'Test',
                'last_name': 'Student',
                'department': cs_dept,
                'campus': tewodros,
                'uog_id': 'UGR/1234/12',
            },
            {
                'username': 'staff@example.com',
                'email': 'staff@example.com',
                'password': 'Staff123!',
                'role': 'academic',
                'first_name': 'Academic',
                'last_name': 'Staff',
                'department': cs_dept,
                'campus': tewodros,
            },
            {
                'username': 'nonstaff@example.com',
                'email': 'nonstaff@example.com',
                'password': 'NonStaff123!',
                'role': 'non_academic',
                'first_name': 'Non-Academic',
                'last_name': 'Staff',
                'department': maintenance_dept,
                'campus': tewodros,
            },
            {
                'username': 'maint@example.com',
                'email': 'maint@example.com',
                'password': 'Maint123!',
                'role': 'maintenance',
                'first_name': 'Maintenance',
                'last_name': 'Worker',
                'department': maintenance_dept,
                'campus': tewodros,
            },
            {
                'username': 'depthead@example.com',
                'email': 'depthead@example.com',
                'password': 'DeptHead123!',
                'role': 'dept_head',
                'first_name': 'Department',
                'last_name': 'Head',
                'department': cs_dept,
                'campus': tewodros,
            },
            {
                'username': 'admin@example.com',
                'email': 'admin@example.com',
                'password': 'Admin123!',
                'role': 'admin',
                'first_name': 'System',
                'last_name': 'Admin',
                'campus': tewodros,
            },
            {
                'username': 'super@example.com',
                'email': 'super@example.com',
                'password': 'Super123!',
                'role': 'super_admin',
                'first_name': 'Super',
                'last_name': 'Admin',
                'is_superuser': True,
                'is_staff': True,
            },
        ]
        
        created_users = {}
        for user_data in users_data:
            password = user_data.pop('password')
            username = user_data['username']
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults=user_data
            )
            
            if created:
                user.set_password(password)
                user.email_verified = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created user: {username}'))
            else:
                self.stdout.write(f'  - User already exists: {username}')
            
            created_users[user_data['role']] = user
        
        # Update department heads
        cs_dept.head = created_users.get('dept_head')
        cs_dept.save()
        
        # Create Categories
        self.stdout.write('Creating categories...')
        categories_data = [
            {
                'name': 'Academic',
                'description': 'Academic-related complaints (grades, courses, teaching)',
                'subcategories': ['Grading Issues', 'Course Content', 'Teaching Quality', 'Exam Scheduling']
            },
            {
                'name': 'Facility',
                'description': 'Facility and infrastructure complaints',
                'subcategories': ['Classroom Maintenance', 'Restroom Issues', 'Lighting', 'Furniture']
            },
            {
                'name': 'IT Services',
                'description': 'IT and technology-related complaints',
                'subcategories': ['Internet/WiFi', 'Computer Lab', 'Portal Access', 'Email Issues']
            },
            {
                'name': 'Library',
                'description': 'Library services and resources',
                'subcategories': ['Book Availability', 'Study Space', 'Library Hours', 'Staff Service']
            },
            {
                'name': 'Administrative',
                'description': 'Administrative and bureaucratic issues',
                'subcategories': ['Registration', 'Transcript', 'ID Card', 'Payment Issues']
            },
        ]
        
        for cat_data in categories_data:
            subcats = cat_data.pop('subcategories')
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created category: {category.name}'))
            
            # Create subcategories
            for subcat_name in subcats:
                SubCategory.objects.get_or_create(
                    category=category,
                    name=subcat_name
                )
        
        # Create Email Templates
        self.stdout.write('Creating email templates...')
        templates_data = [
            {
                'name': 'Complaint Submission Confirmation',
                'template_type': 'submission_confirmation',
                'subject': 'Complaint Submitted - {{tracking_id}}',
                'html_content': '''
                <h2>Complaint Submitted Successfully</h2>
                <p>Dear {{submitter_name}},</p>
                <p>Your complaint has been successfully submitted to the University of Gondar Complaint Management System.</p>
                <p><strong>Tracking ID:</strong> {{tracking_id}}</p>
                <p><strong>Title:</strong> {{title}}</p>
                <p><strong>Status:</strong> {{status}}</p>
                <p>You can track your complaint status using the tracking ID above.</p>
                <p>Thank you,<br>UoG Complaint Management Team</p>
                ''',
                'text_content': '''
                Complaint Submitted Successfully
                
                Dear {{submitter_name}},
                
                Your complaint has been successfully submitted.
                
                Tracking ID: {{tracking_id}}
                Title: {{title}}
                Status: {{status}}
                
                Thank you,
                UoG Complaint Management Team
                ''',
            },
            {
                'name': 'Assignment Notification',
                'template_type': 'assignment_notification',
                'subject': 'Complaint Assigned - {{tracking_id}}',
                'html_content': '''
                <h2>Complaint Assigned to You</h2>
                <p>Dear {{assignee_name}},</p>
                <p>A complaint has been assigned to you.</p>
                <p><strong>Tracking ID:</strong> {{tracking_id}}</p>
                <p><strong>Title:</strong> {{title}}</p>
                <p><strong>Priority:</strong> {{priority}}</p>
                <p>Please review and take appropriate action.</p>
                <p><a href="{{complaint_url}}">View Complaint</a></p>
                ''',
                'text_content': '''
                Complaint Assigned to You
                
                Dear {{assignee_name}},
                
                Tracking ID: {{tracking_id}}
                Title: {{title}}
                Priority: {{priority}}
                
                Please review and take appropriate action.
                ''',
            },
            {
                'name': 'Status Change Notification',
                'template_type': 'status_change',
                'subject': 'Complaint Status Updated - {{tracking_id}}',
                'html_content': '''
                <h2>Complaint Status Updated</h2>
                <p>Dear {{submitter_name}},</p>
                <p>The status of your complaint has been updated.</p>
                <p><strong>Tracking ID:</strong> {{tracking_id}}</p>
                <p><strong>Title:</strong> {{title}}</p>
                <p><strong>Previous Status:</strong> {{old_status}}</p>
                <p><strong>New Status:</strong> {{new_status}}</p>
                <p><strong>Notes:</strong> {{notes}}</p>
                <p><a href="{{complaint_url}}">View Complaint</a></p>
                <p>Thank you,<br>UoG Complaint Management Team</p>
                ''',
                'text_content': '''
                Complaint Status Updated
                
                Dear {{submitter_name}},
                
                Tracking ID: {{tracking_id}}
                Title: {{title}}
                Previous Status: {{old_status}}
                New Status: {{new_status}}
                Notes: {{notes}}
                
                Thank you,
                UoG Complaint Management Team
                ''',
            },
            {
                'name': 'Resolution Notification',
                'template_type': 'resolution_notification',
                'subject': 'Complaint Resolved - {{tracking_id}}',
                'html_content': '''
                <h2>Complaint Resolved</h2>
                <p>Dear {{submitter_name}},</p>
                <p>Your complaint has been resolved.</p>
                <p><strong>Tracking ID:</strong> {{tracking_id}}</p>
                <p><strong>Title:</strong> {{title}}</p>
                <p><strong>Resolution Notes:</strong> {{resolution_notes}}</p>
                <p>We would appreciate your feedback on how we handled your complaint.</p>
                <p><a href="{{complaint_url}}">Rate Our Service</a></p>
                <p>Thank you,<br>UoG Complaint Management Team</p>
                ''',
                'text_content': '''
                Complaint Resolved
                
                Dear {{submitter_name}},
                
                Tracking ID: {{tracking_id}}
                Title: {{title}}
                Resolution Notes: {{resolution_notes}}
                
                Please rate our service at: {{complaint_url}}
                
                Thank you,
                UoG Complaint Management Team
                ''',
            },
        ]
        
        for template_data in templates_data:
            template, created = EmailTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created template: {template.name}'))
        
        # Create Routing Rules
        self.stdout.write('Creating routing rules...')
        
        # Get categories
        academic_cat = Category.objects.filter(name='Academic').first()
        facility_cat = Category.objects.filter(name='Facility').first()
        it_cat = Category.objects.filter(name='IT Services').first()
        
        if academic_cat:
            RoutingRule.objects.get_or_create(
                name='Academic Complaints to CS Department',
                defaults={
                    'description': 'Route academic complaints to CS department head',
                    'category': academic_cat,
                    'campus': tewodros,
                    'assign_to_department': cs_dept,
                    'assign_to_user': created_users.get('dept_head'),
                    'priority': 10,
                }
            )
        
        if facility_cat:
            RoutingRule.objects.get_or_create(
                name='Facility Complaints to Maintenance',
                defaults={
                    'description': 'Route facility complaints to maintenance department',
                    'category': facility_cat,
                    'assign_to_department': maintenance_dept,
                    'assign_to_user': created_users.get('maint'),
                    'set_priority': 'high',
                    'priority': 20,
                }
            )
        
        self.stdout.write(self.style.SUCCESS('\n✅ Database seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS('\nTest Accounts Created:'))
        self.stdout.write('  student@example.com / Student123!')
        self.stdout.write('  staff@example.com / Staff123!')
        self.stdout.write('  nonstaff@example.com / NonStaff123!')
        self.stdout.write('  maint@example.com / Maint123!')
        self.stdout.write('  depthead@example.com / DeptHead123!')
        self.stdout.write('  admin@example.com / Admin123!')
        self.stdout.write('  super@example.com / Super123!')
