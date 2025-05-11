from django.contrib import admin
from .models import Pizza  # Import the Pizza model from current directory

# Custom admin interface configuration for Pizza model
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'ingredients', 'vegetarian', 'price') # Define which fields to display in the admin list view
    search_fields = ["name"]      # Enable search functionality by pizza name

admin.site.register(Pizza, PizzaAdmin) # Register Pizza model with the custom admin interface