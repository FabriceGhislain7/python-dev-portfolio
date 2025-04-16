"""
URL configuration for pizzamama project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include  # 11. add thee module "include"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', include('menu.urls')),  # 12. Add this path !! path('menu', include('menu.urls')), || and save
    path('', include('main.urls')),  # 46. do this path and remove the index for an instant path('', include('main.urls')),
]
# 13 Run the server and on the address add   "/menu" to get the html version of the pizzamama project.
# 14. Go the the "menu/views" folders
# 47. Go to app "main" and create main/static/main/images/(upload the files.py for welcome page we will use)
# 48. Copy the menu/style.css in main/static/main/style.css
"""
# 5. Copy this part that is one models we can directly use
----------------------------------------
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
----------------------------------------
# 6. Turn to menu/urls.py to paste it 
"""
