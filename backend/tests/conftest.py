"""
Pytest configuration and fixtures
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from accounts.models import Campus, College, Department
from complaints.models import Category, SubCategory

User = get_user_model()


@pytest.fixture
def api_client():
    """Return API client"""
    return APIClient()


@pytest.fixture
def create_user(db):
    """Factory fixture for creating users"""
    def make_user(**kwargs):
        defaults = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'student',
        }
        defaults.update(kwargs)
        
        password = defaults.pop('password', 'TestPass123!')
        user = User.objects.create(**defaults)
        user.set_password(password)
        user.save()
        return user
    
    return make_user


@pytest.fixture
def student_user(create_user):
    """Create a student user"""
    return create_user(
        username='student@example.com',
        email='student@example.com',
        role='student'
    )


@pytest.fixture
def staff_user(create_user):
    """Create a staff user"""
    return create_user(
        username='staff@example.com',
        email='staff@example.com',
        role='academic'
    )


@pytest.fixture
def admin_user(create_user):
    """Create an admin user"""
    return create_user(
        username='admin@example.com',
        email='admin@example.com',
        role='admin'
    )


@pytest.fixture
def dept_head_user(create_user, department):
    """Create a department head user"""
    return create_user(
        username='depthead@example.com',
        email='depthead@example.com',
        role='dept_head',
        department=department
    )


@pytest.fixture
def campus(db):
    """Create a campus"""
    return Campus.objects.create(name='Test Campus')


@pytest.fixture
def college(db, campus):
    """Create a college"""
    return College.objects.create(
        name='Test College',
        campus=campus
    )


@pytest.fixture
def department(db, college):
    """Create a department"""
    return Department.objects.create(
        name='Test Department',
        college=college
    )


@pytest.fixture
def category(db):
    """Create a category"""
    return Category.objects.create(
        name='Test Category',
        description='Test category description'
    )


@pytest.fixture
def sub_category(db, category):
    """Create a subcategory"""
    return SubCategory.objects.create(
        name='Test SubCategory',
        category=category
    )


@pytest.fixture
def authenticated_client(api_client, student_user):
    """Return authenticated API client"""
    from rest_framework.authtoken.models import Token
    token = Token.objects.create(user=student_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    api_client.user = student_user
    return api_client
