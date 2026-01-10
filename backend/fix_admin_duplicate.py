import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

print("=" * 60)
print("FIXING ADMIN DUPLICATE")
print("=" * 60)

# Get both admin users
admin_users = CustomUser.objects.filter(email='admin@uog.edu.et').order_by('id')

print(f"\nFound {admin_users.count()} users with admin@uog.edu.et:")
for user in admin_users:
    print(f"  - ID: {user.id}, Username: {user.username}, Email: {user.email}")

# Update the second one (admin) to have a different email
if admin_users.count() > 1:
    user_to_update = admin_users[1]  # The 'admin' user
    new_email = "admin_user@uog.edu.et"
    
    print(f"\nUpdating user '{user_to_update.username}' (ID: {user_to_update.id}):")
    print(f"  Old email: {user_to_update.email}")
    print(f"  New email: {new_email}")
    
    user_to_update.email = new_email
    user_to_update.save()
    
    print("\n✓ Fixed!")

# Verify
print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)
admin_users_after = CustomUser.objects.filter(email='admin@uog.edu.et')
print(f"Users with admin@uog.edu.et: {admin_users_after.count()}")
for user in admin_users_after:
    print(f"  - {user.username} (ID: {user.id})")

print("\nAll admin-related users:")
admin_related = CustomUser.objects.filter(username__icontains='admin') | CustomUser.objects.filter(email__icontains='admin')
for user in admin_related:
    print(f"  - Username: {user.username}, Email: {user.email}")
