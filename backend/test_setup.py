"""
Quick test script to verify Django setup
Run with: python test_setup.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_imports():
    """Test that all models can be imported"""
    print("Testing imports...")
    try:
        from accounts.models import CustomUser, Campus, Department, PasswordResetToken, ActivityLog
        from complaints.models import (
            Category, SubCategory, Complaint, ComplaintEvent,
            ComplaintComment, ComplaintFile, RoutingRule, EmailTemplate
        )
        print("✓ All models imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False


def test_settings():
    """Test that settings are configured correctly"""
    print("\nTesting settings...")
    from django.conf import settings
    
    checks = [
        ('SECRET_KEY', settings.SECRET_KEY),
        ('DEBUG', settings.DEBUG),
        ('AUTH_USER_MODEL', settings.AUTH_USER_MODEL),
        ('MEDIA_ROOT', settings.MEDIA_ROOT),
        ('MEDIA_URL', settings.MEDIA_URL),
    ]
    
    all_ok = True
    for name, value in checks:
        if value:
            print(f"✓ {name}: {value}")
        else:
            print(f"✗ {name}: Not set")
            all_ok = False
    
    return all_ok


def test_database():
    """Test database connection"""
    print("\nTesting database connection...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False


def test_models():
    """Test that models are registered"""
    print("\nTesting model registration...")
    from django.apps import apps
    
    expected_models = [
        ('accounts', 'CustomUser'),
        ('accounts', 'Campus'),
        ('accounts', 'Department'),
        ('accounts', 'PasswordResetToken'),
        ('accounts', 'ActivityLog'),
        ('complaints', 'Category'),
        ('complaints', 'SubCategory'),
        ('complaints', 'Complaint'),
        ('complaints', 'ComplaintEvent'),
        ('complaints', 'ComplaintComment'),
        ('complaints', 'ComplaintFile'),
        ('complaints', 'RoutingRule'),
        ('complaints', 'EmailTemplate'),
    ]
    
    all_ok = True
    for app_label, model_name in expected_models:
        try:
            model = apps.get_model(app_label, model_name)
            print(f"✓ {app_label}.{model_name}")
        except Exception as e:
            print(f"✗ {app_label}.{model_name}: {e}")
            all_ok = False
    
    return all_ok


def main():
    print("=" * 60)
    print("UoG Complaint Management System - Setup Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Settings", test_settings()))
    results.append(("Database", test_database()))
    results.append(("Models", test_models()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate")
        print("3. Run: python manage.py seed_data")
        print("4. Run: python manage.py runserver")
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
