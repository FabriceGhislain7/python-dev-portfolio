from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, AllergenViewSet, IngredientViewSet, PizzaViewSet, PizzaSizeViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'allergens', AllergenViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'pizzas', PizzaViewSet)
router.register(r'sizes', PizzaSizeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]