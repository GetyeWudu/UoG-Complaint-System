import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

# Check specific users
test_users = [
    ('getye', ['admin123', 'getye123', 'password', 'test123', '123456']),
    ('dean_info', ['dean123', 'dean_info123', 'password', 'test123']),
    ('head_cs', ['dept123', 'head_cs123', 'password', 'test123']),
    ('abebe', ['student123', 'abebe123', 'password', 'test123']),
    ('gech', ['student123', 'gech123', 'password', 'test123']),
]

print("=" * 60)
print("CHECKING MAIN USER PASSWORDS")
print("=" * 60)

for username, passwords in test_users:
    try:
        user = CustomUser.objects.get(username=username)
        print(f"\nUsername: {username}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
        
        found = False
        for pwd in passwords:
            if user.check_password(pwd):
                print(f"✓ Password: {pwd}")
                found = True
                break
        
        if not found:
            print(f"✗ None of the tested passwords work")
            print(f"  Tried: {', '.join(passwords)}")
    except CustomUser.DoesNotExist:
        print(f"\n✗ User '{username}' not found")

print("\n" + "=" * 60)
