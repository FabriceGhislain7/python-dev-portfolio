from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    # return HttpResponse("ciao")
    return render(request, 'myblog/home.html')

def contacts(request):
    # return HttpResponse("Site official")
    return render(request, 'myblog/contacts.html')

def articles(request):
    return render(request, "myblog/articles.html")
    
    