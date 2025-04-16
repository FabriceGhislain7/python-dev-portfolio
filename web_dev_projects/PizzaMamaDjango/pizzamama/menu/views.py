from django.shortcuts import render
from django.http import HttpResponse # 1. Import this librairy necessary to visualize the menu in html
from .models import Pizza   # 15 We import the pizza model to get our base model and visualize directly in html page.
# Create your views here.

# 20. Create a template for visualize the data the html
# 21. Go to app "menu", create the folder "templates" exactly like this, because it is a keyword
# 22. Inside "templates" folder, created exactly the name "menu", like the father name. like this menu/templates/menu
# 23. inside "menu", generate "index.html" file, then we have :menu/templates/menu/index.html
# 24. Go to menu/templates/menu/index.html you have create.

# 2. manage the index to visualize the menu by this function. (http://127.0.0.1:8000/admin/menu/pizza/)
def index(request):
    """
    pizzas = Pizza.objects.all()  # 16 We collect the pizzas objects and , using for and join methods.(3lines of ccode)
    pizzas_names = [pizza.name + ": " + str(pizza.price) +  " €" for pizza in pizzas]
    pizzas_names_str = ", ".join(pizzas_names) 
    return HttpResponse("The Pizzas: " + pizzas_names_str)   # 17 join add the return "return HttpResponse("The Pizzas" + pizzas_names_str)"
    return render(request, 'menu/index.html')
    """
    pizzas = Pizza.objects.all().order_by('price')
    return render(request, 'menu/index.html', {'pizzas': pizzas})

# 3. in menu(folder) we create a file urls.py
# 4. Go to pizzamama/urls.py
# 18. How to use the debug on this kind of projects?: on the top- Add configurations/ Templates/Python/Script path(click on the folder)/ select the manage.py inside the django projects and click small ok, not the big one under/
# 19 We are still on the same page. The parameter to add is "runserver"/ click "Apply" / You can nominate the play bottom "Django".
# 28. We comment the block inside def index() function and al contrary to return this: HttpResponse("The Pizzas: " + pizzas_names_str)
# 29. we return the name of our templates: return render(request, 'menu/index.html')
# 30. We go to index.html file to insert the block for each pizzas
# 33. the function became like this inside to return render(request, 'menu/index.html'), it will return
# def index(request):
#     pizzas = Pizza.objects.all()
#     return render(request, 'menu/index', {'pizzas': pizzas})
# 34 Go to index.html file to modified the price of the pizzas.