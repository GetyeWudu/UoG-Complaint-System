"""
Management command to create test users for all roles
"""
from django.core.management.base import BaseCommand
from accounts.models import CustomUser, Campus, College, Department
from django.db import transaction


class Command(BaseCommand):
    help = 'Create test users for all roles with simple passwords'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test users for all roles...\n')
        
        with transaction.atomic():
            # Create basic structure if not exists
            campus, _ = Campus.objects.get_or_create(name='Main Campus')
            college, _ = College.objects.get_or_create(
                name='College of Informatics',
                defaults={'campus': campus}
            )
            department, _ = Department.objects.get_or_create(
                name='Computer Science',
                defaults={'college': college}
            )
            
            # Test users with simple credentials (username only, no email)
            test_users = [
                {
                    'username': 'student',
                    'email': 'student@uog.edu.et',
                    'password': 'student123',
                    'role': 'student',
                    'first_name': 'Test',
                    'last_name': 'Student',
                    'uog_id': 'UGR/1001/12'
                },
                {
                    'username': 'academic',
                    'email': 'academic@uog.edu.et',
                    'password': 'academic123',
                    'role': 'academic',
                    'first_name': 'Test',
                    'last_name': 'Academic',
                    'uog_id': 'UGR/1002/12'
                },
                {
                    'username': 'nonacademic',
                    'email': 'nonacademic@uog.edu.et',
                    'password': 'nonacademic123',
                    'role': 'non_academic',
                    'first_name': 'Test',
                    'last_name': 'NonAcademic',
                    'uog_id': 'UGR/1003/12'
                },
                {
                    'username': 'proctor',
                    'email': 'proctor@uog.edu.et',
                    'password': 'proctor123',
                    'role': 'proctor',
                    'first_name': 'Test',
                    'last_name': 'Proctor',
                    'uog_id': 'UGR/1004/12'
                },
                {
                    'username': 'depthead',
                    'email': 'depthead@uog.edu.et',
                    'password': 'depthead123',
                    'role': 'dept_head',
                    'first_name': 'Test',
                    'last_name': 'DeptHead',
                    'uog_id': 'UGR/1005/12'
                },
                {
                    'username': 'dean',
                    'email': 'dean@uog.edu.et',
                    'password': 'dean123',
                    'role': 'dean',
                    'first_name': 'Test',
                    'last_name': 'Dean',
                    'uog_id': 'UGR/1006/12'
                },
                {
                    'username': 'maintenance',
                    'email': 'maintenance@uog.edu.et',
                    'password': 'maintenance123',
                    'role': 'maintenance',
                    'first_name': 'Test',
                    'last_name': 'Maintenance',
                    'uog_id': 'UGR/1007/12'
                },
                {
                    'username': 'admin',
                    'email': 'admin@uog.edu.et',
                    'password': 'admin123',
                    'role': 'admin',
                    'first_name': 'Test',
                    'last_name': 'Admin',
                    'uog_id': 'UGR/1008/12'
                },
                {
                    'username': 'superadmin',
                    'email': 'superadmin@uog.edu.et',
                    'password': 'superadmin123',
                    'role': 'super_admin',
                    'first_name': 'Test',
                    'last_name': 'SuperAdmin',
                    'uog_id': 'UGR/1009/12'
                },
                {
                    'username': 'director',
                    'email': 'director@uog.edu.et',
                    'password': 'director123',
                    'role': 'campus_director',
                    'first_name': 'Test',
                    'last_name': 'Director',
                    'uog_id': 'UGR/1010/12'
                },
            ]
            
            created_count = 0
            updated_count = 0
            
            for user_data in test_users:
                username = user_data.pop('username')
                password = user_data.pop('password')
                email = user_data.get('email')
                uog_id = user_data.get('uog_id')
                
                # Try to get existing user by username, email, or uog_id
                user = None
                created = False
                
                try:
                    user = CustomUser.objects.get(username=username)
                except CustomUser.DoesNotExist:
                    try:
                        user = CustomUser.objects.get(email=email)
                    except CustomUser.DoesNotExist:
                        try:
                            user = CustomUser.objects.get(uog_id=uog_id)
                        except CustomUser.DoesNotExist:
                            user = CustomUser.objects.create(username=username, **user_data)
                            created = True
                
                if created:
                    user.set_password(password)
                    user.email_verified = True
                    user.is_active = True
                    # Assign department/campus based on role
                    if user.role == 'dean':
                        # Dean should be associated with college via department
                        user.department = department  # This gives access to college
                    else:
                        user.department = department
                    user.campus = campus
                    user.save()
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Created: {username} (password: {password}) - Role: {user.role}'
                        )
                    )
                else:
                    # Update existing user
                    user.set_password(password)
                    user.email_verified = True
                    user.is_active = True
                    # Assign department/campus based on role
                    if user.role == 'dean':
                        # Dean should be associated with college via department
                        user.department = department  # This gives access to college
                    else:
                        user.department = department
                    user.campus = campus
                    for key, value in user_data.items():
                        setattr(user, key, value)
                    user.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f'↻ Updated: {username} (password: {password}) - Role: {user.role}'
                        )
                    )
            
            self.stdout.write('\n' + '='*60)
            self.stdout.write(self.style.SUCCESS(f'\n✓ Created {created_count} new users'))
            self.stdout.write(self.style.WARNING(f'↻ Updated {updated_count} existing users'))
            self.stdout.write('\n' + '='*60)
            self.stdout.write('\nTEST USER CREDENTIALS (Username / Password):\n')
            self.stdout.write('='*60)
            self.stdout.write('\n1.  Student:          student / student123')
            self.stdout.write('\n2.  Academic Staff:   academic / academic123')
            self.stdout.write('\n3.  Non-Academic:     nonacademic / nonacademic123')
            self.stdout.write('\n4.  Proctor:          proctor / proctor123')
            self.stdout.write('\n5.  Dept Head:        depthead / depthead123')
            self.stdout.write('\n6.  Dean:             dean / dean123')
            self.stdout.write('\n7.  Maintenance:      maintenance / maintenance123')
            self.stdout.write('\n8.  Admin:            admin / admin123')
            self.stdout.write('\n9.  Super Admin:      superadmin / superadmin123')
            self.stdout.write('\n10. Campus Director:  director / director123')
            self.stdout.write('\n' + '='*60 + '\n')
            self.stdout.write('\nNOTE: Login with USERNAME only (not email)\n')
            self.stdout.write('='*60 + '\n')
