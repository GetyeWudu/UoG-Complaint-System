from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from complaints.views import AnonymousComplaintView, TrackComplaintView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints
    path('api/auth/', include('accounts.urls')),
    path('api/complaints/', include('complaints.urls')),
    
    # Public/Anonymous Endpoints
    path('api/public/submit/', AnonymousComplaintView.as_view(), name='anonymous-submit'),
    path('api/public/track/<str:tracking_id>/', TrackComplaintView.as_view(), name='track-complaint'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)