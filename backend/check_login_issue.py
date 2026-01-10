import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser
from django.utils import timezone

# Check all users and their login status
print("=" * 60)
print("USER ACCOUNT STATUS CHECK")
print("=" * 60)

users = CustomUser.objects.all()
for u in users:
    print(f"\nUsername: {u.username}")
    print(f"Email: {u.email}")
    print(f"Role: {u.role}")
    print(f"Is active: {u.is_active}")
    print(f"Failed login attempts: {u.failed_login_attempts}")
    print(f"Account locked until: {u.account_locked_until}")
    
    # Check if account is currently locked
    if u.account_locked_until and u.account_locked_until > timezone.now():
        print(f"⚠️  ACCOUNT IS LOCKED! Locked until: {u.account_locked_until}")
        print(f"   Time remaining: {u.account_locked_until - timezone.now()}")
    
    # Test password for common test accounts
    test_passwords = {
        'student@test.com': 'student123',
        'admin@test.com': 'admin123',
        'dean@test.com': 'dean123',
        'dept_head@test.com': 'dept123'
    }
    
    if u.email in test_passwords:
        password_valid = u.check_password(test_passwords[u.email])
        print(f"Password check ({test_passwords[u.email]}): {password_valid}")
        if not password_valid:
            print(f"❌ PASSWORD MISMATCH!")
    
    print("-" * 60)

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
locked_users = CustomUser.objects.filter(account_locked_until__gt=timezone.now())
print(f"Total users: {users.count()}")
print(f"Locked accounts: {locked_users.count()}")
print(f"Active accounts: {CustomUser.objects.filter(is_active=True).count()}")
