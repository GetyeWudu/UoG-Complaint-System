import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

# Check test user
try:
    u = CustomUser.objects.get(email='student@test.com')
    print(f'Username: {u.username}')
    print(f'Email: {u.email}')
    print(f'Password check: {u.check_password("student123")}')
    print(f'Is active: {u.is_active}')
except CustomUser.DoesNotExist:
    print('User not found!')
