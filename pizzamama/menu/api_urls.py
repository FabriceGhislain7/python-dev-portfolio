from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('GetPizzas', views.api_get_pizzas),
]