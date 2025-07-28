"""
URL configuration for pizzamama project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Step 12: Import per frontend views
from . import views as main_views

@api_view(['GET'])
def api_root(request):
    """API root endpoint con informazioni sistema"""
    return Response({
        'message': 'Benvenuto alle API di PizzaMama Enterprise!',
        'version': '2.0',
        'documentation': {
            'swagger': '/api/docs/swagger/',
            'redoc': '/api/docs/redoc/',
            'schema': '/api/docs/schema/'
        },
        'endpoints': {
            'admin': '/admin/',
            'api-auth': '/api/auth/',
            'accounts': '/api/accounts/',
            'products': '/api/products/',
            'orders': '/api/orders/'
        }
    })

urlpatterns = [
    # ========================================
    # ADMIN INTERFACE
    # ========================================
    path('admin/', admin.site.urls),
   
    # ========================================
    # API DOCUMENTATION - STEP 11
    # ========================================
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   
    # ========================================
    # API ROOT & AUTHENTICATION
    # ========================================
    path('api/', api_root, name='api-root'),
    path('api/auth/', include('rest_framework.urls')),
   
    # ========================================
    # BUSINESS LOGIC APIs - STEP 11
    # ========================================
    path('api/accounts/', include('apps.accounts.api.urls')),
    path('api/products/', include('apps.products.api.urls')),
    path('api/orders/', include('apps.orders.api.urls')),

    # ========================================
    # FRONTEND PAGES - STEP 12
    # ========================================
    # Homepage e pagine principali
    path('', main_views.home, name='home'),
    path('about/', main_views.about, name='about'),
    
    # Product catalog frontend
    path('products/', include('apps.products.urls')),
    
    # Cart e orders frontend
    path('cart/', include('apps.orders.urls')),
    
    # User accounts frontend
    path('accounts/', include('apps.accounts.urls')),
]

# ========================================
# MEDIA FILES SERVING - STEP 12
# ========================================
# Serve media files durante development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files durante development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)