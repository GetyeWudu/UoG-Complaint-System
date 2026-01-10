import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser
from django.db.models import Count

print("=" * 60)
print("FINDING DUPLICATE EMAILS")
print("=" * 60)

# Find duplicate emails
duplicates = CustomUser.objects.values('email').annotate(
    count=Count('email')
).filter(count__gt=1)

for dup in duplicates:
    email = dup['email']
    count = dup['count']
    print(f"\n⚠️  Email '{email}' appears {count} times:")
    users = CustomUser.objects.filter(email=email)
    for u in users:
        print(f"   - ID: {u.id}, Username: {u.username}, Role: {u.role}, Active: {u.is_active}")

# Find users with empty emails
empty_emails = CustomUser.objects.filter(email='')
if empty_emails.exists():
    print(f"\n⚠️  Found {empty_emails.count()} users with empty email:")
    for u in empty_emails:
        print(f"   - ID: {u.id}, Username: {u.username}, Role: {u.role}")

print("\n" + "=" * 60)
print("SOLUTION")
print("=" * 60)
print("The login is failing because when you try to login with an email")
print("that has duplicates, Django can't determine which user to authenticate.")
print("\nYou need to either:")
print("1. Delete duplicate users")
print("2. Update duplicate emails to be unique")
print("3. Login using username instead of email")
