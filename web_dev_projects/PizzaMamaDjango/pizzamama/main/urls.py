# 7. Paste what you copy here:
from django.urls import path
from . import views   # 8. We import the view moduls

app_name = 'main'
urlpatterns = [
    path('', views.index, name="index"), # 9. We remove the sub address 'admin/' and substitute by : path('', views.index, name="index"),
]
# 10. Go to the pizzamama/urls
# 44. We have exactly the same things like in "menu/urls.py"
# 45. Go to "pizzamama/urls.py"