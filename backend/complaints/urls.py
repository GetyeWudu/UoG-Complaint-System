from django.urls import path
from . import views
from .ai_admin_views import ValidateComplaintView, ComplaintStatsView
from .dashboard_views import (
    StudentDashboardView, DeanDashboardView, ProctorDashboardView,
    AdminDashboardView, DepartmentHeadDashboardView, MaintenanceWorkerDashboardView,
    CampusDirectorDashboardView, SuperAdminDashboardView
)
from .approval_views import ApprovalWorkflowViewSet
from .reporting_views import ReportingViewSet
from .chatbot_views import chat_message, suggested_questions
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# Register dashboard viewsets
router.register(r'dashboards/student', StudentDashboardView, basename='student-dashboard')
router.register(r'dashboards/dean', DeanDashboardView, basename='dean-dashboard')
router.register(r'dashboards/proctor', ProctorDashboardView, basename='proctor-dashboard')
router.register(r'dashboards/admin', AdminDashboardView, basename='admin-dashboard')
router.register(r'dashboards/dept-head', DepartmentHeadDashboardView, basename='dept-head-dashboard')
router.register(r'dashboards/maintenance', MaintenanceWorkerDashboardView, basename='maintenance-dashboard')
router.register(r'dashboards/campus-director', CampusDirectorDashboardView, basename='campus-director-dashboard')
router.register(r'dashboards/super-admin', SuperAdminDashboardView, basename='super-admin-dashboard')

# Register approval workflow
router.register(r'approvals', ApprovalWorkflowViewSet, basename='approval-workflow')

# Register reporting
router.register(r'reports', ReportingViewSet, basename='reporting')

urlpatterns = [
    # Complaint CRUD
    path('', views.ComplaintListCreateView.as_view(), name='complaint-list-create'),
    path('<int:pk>/', views.ComplaintDetailView.as_view(), name='complaint-detail'),
    
    # AI Validation
    path('validate/', ValidateComplaintView.as_view(), name='complaint-validate'),
    path('ai-stats/', ComplaintStatsView.as_view(), name='complaint-ai-stats'),
    
    # Complaint Actions
    path('<int:complaint_id>/assign/', views.ComplaintAssignView.as_view(), name='complaint-assign'),
    path('<int:complaint_id>/status/', views.ComplaintStatusUpdateView.as_view(), name='complaint-status'),
    path('<int:pk>/feedback/', views.ComplaintFeedbackView.as_view(), name='complaint-feedback'),
    
    # File Management
    path('<int:complaint_id>/files/', views.ComplaintFileUploadView.as_view(), name='complaint-file-upload'),
    path('files/<int:file_id>/download/', views.ComplaintFileDownloadView.as_view(), name='complaint-file-download'),
    path('files/<int:file_id>/', views.ComplaintFileDeleteView.as_view(), name='complaint-file-delete'),
    
    # Comments
    path('<int:complaint_id>/comments/', views.ComplaintCommentListCreateView.as_view(), name='complaint-comments'),
    
    # Staff List
    path('staff/', views.StaffListView.as_view(), name='staff-list'),
    
    # Chatbot
    path('chatbot/message/', chat_message, name='chatbot-message'),
    path('chatbot/suggestions/', suggested_questions, name='chatbot-suggestions'),
]

urlpatterns += router.urls