from django.shortcuts import render
# from django.http import HttpResponse   # 52. We don't need again     return HttpResponse("Main principal page."), we take directly the render function

# Create your views here.

def index(request):
    return render (request, 'main/index.html') # 53. Go to pizzamama/settings to add 'main.apps.MenuConfig' in the LIST INSTALLED_APPS