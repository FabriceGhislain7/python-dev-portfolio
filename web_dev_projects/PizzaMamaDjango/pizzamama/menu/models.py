from django.db import models

# Create your models here.
# The Pizza class inherits from Django's models class

class Pizza(models.Model):
    name = models.CharField(max_length=200)          # Pizza name
    ingredients = models.CharField(max_length=400)   # Main ingredients
    price = models.FloatField(default=0)            # Price in euros
    vegetarian = models.BooleanField(default=False)  # Vegetarian option

    def __str__(self):
        return self.name                            # Admin display