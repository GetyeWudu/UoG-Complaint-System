import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

print("=" * 60)
print("FIXING DUPLICATE EMAILS")
print("=" * 60)

# Fix admin@uog.edu.et duplicates
print("\n1. Fixing admin@uog.edu.et duplicates...")
admin_users = CustomUser.objects.filter(email='admin@uog.edu.et').order_by('id')
if admin_users.count() > 1:
    # Keep the first one (getye), update the second
    for i, user in enumerate(admin_users):
        if i == 0:
            print(f"   ✓ Keeping: {user.username} (ID: {user.id}) with email: {user.email}")
        else:
            new_email = f"{user.username}@uog.edu.et"
            print(f"   → Updating: {user.username} (ID: {user.id})")
            print(f"     Old email: {user.email}")
            print(f"     New email: {new_email}")
            user.email = new_email
            user.save()

# Fix dean@uog.edu.et duplicates
print("\n2. Fixing dean@uog.edu.et duplicates...")
dean_users = CustomUser.objects.filter(email='dean@uog.edu.et').order_by('id')
if dean_users.count() > 1:
    # Keep the first one (dean_info), update the second
    for i, user in enumerate(dean_users):
        if i == 0:
            print(f"   ✓ Keeping: {user.username} (ID: {user.id}) with email: {user.email}")
        else:
            new_email = f"{user.username}_dean@uog.edu.et"
            print(f"   → Updating: {user.username} (ID: {user.id})")
            print(f"     Old email: {user.email}")
            print(f"     New email: {new_email}")
            user.email = new_email
            user.save()

# Fix empty email
print("\n3. Fixing empty email...")
empty_email_users = CustomUser.objects.filter(email='')
for user in empty_email_users:
    new_email = f"{user.username.lower()}@uog.edu.et"
    print(f"   → Updating: {user.username} (ID: {user.id})")
    print(f"     New email: {new_email}")
    user.email = new_email
    user.save()

print("\n" + "=" * 60)
print("✓ DUPLICATE EMAILS FIXED!")
print("=" * 60)
print("\nYou can now login with:")
print("  - Username: getye")
print("  - Email: admin@uog.edu.et")
print("  - Or use any username directly")
print("\nThe duplicate 'admin' user now has email: admin@uog.edu.et")
print("The duplicate 'dean' user now has email: dean_dean@uog.edu.et")
