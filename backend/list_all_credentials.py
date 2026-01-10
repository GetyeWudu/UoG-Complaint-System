import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

print("=" * 80)
print("ALL USER CREDENTIALS")
print("=" * 80)

# Common test passwords by role
role_passwords = {
    'student': 'student123',
    'academic': 'academic123',
    'non_academic': 'nonacademic123',
    'maintenance': 'maintenance123',
    'proctor': 'proctor123',
    'dept_head': 'dept123',
    'dean': 'dean123',
    'campus_director': 'director123',
    'admin': 'admin123',
    'super_admin': 'superadmin123'
}

users = CustomUser.objects.all().order_by('role', 'username')

current_role = None
for user in users:
    if user.role != current_role:
        current_role = user.role
        print(f"\n{'='*80}")
        print(f"ROLE: {user.role.upper().replace('_', ' ')}")
        print(f"{'='*80}")
    
    print(f"\nUsername: {user.username}")
    print(f"Email: {user.email or '(no email)'}")
    
    # Try to guess password
    likely_password = role_passwords.get(user.role, '???')
    password_works = user.check_password(likely_password)
    
    if password_works:
        print(f"Password: {likely_password} ✓")
    else:
        # Try some other common patterns
        other_passwords = [
            user.username + '123',
            user.role + '123',
            'password123',
            'test123'
        ]
        found = False
        for pwd in other_passwords:
            if user.check_password(pwd):
                print(f"Password: {pwd} ✓")
                found = True
                break
        if not found:
            print(f"Password: (unknown - try {likely_password} or {user.username}123)")

print("\n" + "=" * 80)
print("QUICK REFERENCE - MAIN TEST ACCOUNTS")
print("=" * 80)
print("\nStudent:")
print("  Username: student@example.com  |  Email: student@test.com  |  Password: student123")
print("\nAdmin:")
print("  Username: getye  |  Email: admin@uog.edu.et  |  Password: admin123")
print("\nDean:")
print("  Username: dean_info  |  Email: dean@uog.edu.et  |  Password: dean123")
print("\nDepartment Head:")
print("  Username: head_cs  |  Email: head@uog.edu.et  |  Password: dept123")
print("\n" + "=" * 80)
