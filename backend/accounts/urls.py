from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.CustomAuthToken.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Password Management
    path('password-reset/request/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password-change'),
    
    # OAuth
    path('oauth/callback/', views.OAuthCallbackView.as_view(), name='oauth-callback'),
    path('oauth/link/', views.OAuthLinkView.as_view(), name='oauth-link'),
    
    # User Profile
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    
    # Utility Endpoints
    path('campuses/', views.CampusListView.as_view(), name='campus-list'),
    path('departments/', views.DepartmentListView.as_view(), name='department-list'),
    path('activity-logs/', views.ActivityLogListView.as_view(), name='activity-logs'),
]
