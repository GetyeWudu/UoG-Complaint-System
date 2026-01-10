import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

print("=" * 60)
print("RESETTING PASSWORDS FOR MAIN ACCOUNTS")
print("=" * 60)

# Reset passwords for main accounts
accounts_to_reset = [
    ('getye', 'admin123', 'admin'),
    ('dean_info', 'dean123', 'dean'),
    ('head_cs', 'dept123', 'dept_head'),
    ('abebe', 'student123', 'student'),
    ('gech', 'student123', 'student'),
    ('proctor_1', 'proctor123', 'proctor'),
]

for username, new_password, role in accounts_to_reset:
    try:
        user = CustomUser.objects.get(username=username)
        user.set_password(new_password)
        user.failed_login_attempts = 0
        user.account_locked_until = None
        user.save()
        
        print(f"\n✓ Reset password for: {username}")
        print(f"  Email: {user.email}")
        print(f"  Role: {user.role}")
        print(f"  New Password: {new_password}")
    except CustomUser.DoesNotExist:
        print(f"\n✗ User '{username}' not found")

print("\n" + "=" * 60)
print("PASSWORD RESET COMPLETE!")
print("=" * 60)
print("\nYou can now login with these credentials:")
print("\n1. Admin Account:")
print("   Username: getye")
print("   Email: admin@uog.edu.et")
print("   Password: admin123")
print("\n2. Dean Account:")
print("   Username: dean_info")
print("   Email: dean@uog.edu.et")
print("   Password: dean123")
print("\n3. Department Head:")
print("   Username: head_cs")
print("   Email: head@uog.edu.et")
print("   Password: dept123")
print("\n4. Student Accounts:")
print("   Username: abebe  |  Password: student123")
print("   Username: gech   |  Password: student123")
print("\n5. Proctor:")
print("   Username: proctor_1  |  Password: proctor123")
print("\n" + "=" * 60)
