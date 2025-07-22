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
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

def home_view(request):
    return HttpResponse("""
    <h1>🍕 PizzaMama Enterprise</h1>
    <p><a href="/admin/">Admin Panel</a></p>
    <p><a href="/api/">API Root</a></p>
    <p><a href="/api/auth/login/">API Login</a></p>
    """)

@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Benvenuto alle API di PizzaMama!',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'api-auth': '/api/auth/login/',
        }
    })

urlpatterns = [
    path('', home_view, name='home'),                  # ← AGGIUNGI QUESTA
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/auth/', include('rest_framework.urls')),
]