from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from complaints.views import AnonymousComplaintView, TrackComplaintView

def health_check(request):
    """Health check endpoint for Render"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'UoG Complaints System',
        'version': '1.0.0'
    })

urlpatterns = [
    # Health check for Render
    path('', health_check, name='health-check'),
    path('api/', health_check, name='api-health-check'),
    
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