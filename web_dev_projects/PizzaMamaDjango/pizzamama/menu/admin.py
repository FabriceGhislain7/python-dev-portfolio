from django.contrib import admin
from .models import Pizza  # Import the Pizza model from current directory

# Admin credentials reminder:Username: my_user, Password: access7, Email: my_user@gmail.com

# Custom admin interface configuration for Pizza model
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'ingredients', 'vegetarian', 'price') # Define which fields to display in the admin list view
    search_fields = ["name"]      # Enable search functionality by pizza name

admin.site.register(Pizza, PizzaAdmin) # Register Pizza model with the custom admin interface


# After making changes to admin.py:
# 1. Run migrations: python manage.py makemigrations
# 2. Apply migrations: python manage.py migrate
# 3. Access admin at: http://127.0.0.1:8000/admin