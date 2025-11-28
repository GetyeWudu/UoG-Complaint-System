from django.urls import path
from . import views

urlpatterns = [
    # Complaint CRUD
    path('', views.ComplaintListCreateView.as_view(), name='complaint-list-create'),
    path('<int:pk>/', views.ComplaintDetailView.as_view(), name='complaint-detail'),
    
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
]