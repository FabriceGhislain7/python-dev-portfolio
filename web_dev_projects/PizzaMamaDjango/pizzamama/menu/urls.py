# 7. Paste what you copy here:
from django.urls import path
from . import views   # 8. We import the view moduls

app_name = 'menu'
urlpatterns = [
    path('', views.index, name="index"), # 9. We remove the sub address 'admin/' and substitute by : path('', views.index, name="index"),
]
# 10. Go to the pizzamama/urls
