# apps/products/urls.py - Step 12 Frontend URLs
from django.urls import path
from . import views

app_name = 'products'

# Temporary basic URLs - implementeremo le views nei prossimi files
urlpatterns = [
    # Placeholder per ora - implementeremo dopo
    # path('', views.catalog, name='catalog'),
    # path('category/<slug:slug>/', views.category, name='category'),
    # path('<slug:slug>/', views.product_detail, name='detail'),
]