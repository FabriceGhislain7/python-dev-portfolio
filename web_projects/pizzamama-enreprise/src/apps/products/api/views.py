from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, F
from apps.products.models import Category, Allergen, Ingredient, Pizza, PizzaSize
from .serializers import (
    CategorySerializer, AllergenSerializer, IngredientSerializer,
    PizzaListSerializer, PizzaDetailSerializer, PizzaCreateUpdateSerializer,
    PizzaSizeSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet per categorie con gerarchia"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['sort_order', 'name', 'view_count']
    ordering = ['sort_order', 'name']
    lookup_field = 'slug'
    
    @action(detail=False)
    def hierarchy(self, request):
        """Ritorna gerarchia completa categorie"""
        root_categories = Category.objects.filter(parent=None, is_active=True)
        serializer = CategorySerializer(root_categories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increment_view(self, request, slug=None):
        """Incrementa contatore visualizzazioni"""
        category = self.get_object()
        category.view_count = F('view_count') + 1
        category.save()
        return Response({'message': 'View count updated'})

class AllergenViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet read-only per allergeni"""
    queryset = Allergen.objects.all()
    serializer_class = AllergenSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'symbol']

class IngredientViewSet(viewsets.ModelViewSet):
    """ViewSet per ingredienti con gestione stock"""
    queryset = Ingredient.objects.filter(is_active=True)
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_vegetarian', 'is_vegan', 'is_gluten_free', 'allergens']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price_per_extra', 'stock_quantity']
    ordering = ['name']
    lookup_field = 'slug'
    
    def get_permissions(self):
        """Read-only per non-staff"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=False)
    def low_stock(self, request):
        """Ingredienti con scorte basse"""
        low_stock_ingredients = Ingredient.objects.filter(
            stock_quantity__lte=F('minimum_stock'),
            is_active=True
        )
        serializer = self.get_serializer(low_stock_ingredients, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def dietary(self, request):
        """Filtra per esigenze dietetiche"""
        dietary_type = request.query_params.get('type', 'vegetarian')
        
        if dietary_type == 'vegetarian':
            queryset = self.get_queryset().filter(is_vegetarian=True)
        elif dietary_type == 'vegan':
            queryset = self.get_queryset().filter(is_vegan=True)
        elif dietary_type == 'gluten_free':
            queryset = self.get_queryset().filter(is_gluten_free=True)
        else:
            queryset = self.get_queryset()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PizzaSizeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet read-only per taglie pizza"""
    queryset = PizzaSize.objects.filter(is_active=True)
    serializer_class = PizzaSizeSerializer
    permission_classes = [permissions.AllowAny]
    ordering = ['sort_order', 'diameter_cm']

class PizzaViewSet(viewsets.ModelViewSet):
    """ViewSet per pizze con filtering avanzato"""
    queryset = Pizza.objects.filter(is_active=True)
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_vegetarian', 'is_vegan', 'is_spicy', 'is_featured']
    search_fields = ['name', 'description', 'short_description']
    ordering_fields = ['name', 'base_price', 'avg_rating', 'popularity_score', 'created_at']
    ordering = ['-is_featured', '-popularity_score', 'name']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        """Serializer diverso per lista e dettaglio"""
        if self.action == 'list':
            return PizzaListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PizzaCreateUpdateSerializer
        else:
            return PizzaDetailSerializer
    
    def get_permissions(self):
        """Read-only per non-staff"""
        if self.action in ['list', 'retrieve', 'popular', 'featured', 'search_advanced']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, *args, **kwargs):
        """Incrementa view count quando si visualizza dettaglio"""
        instance = self.get_object()
        instance.view_count = F('view_count') + 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False)
    def featured(self, request):
        """Pizze in evidenza"""
        featured_pizzas = self.get_queryset().filter(is_featured=True)
        serializer = PizzaListSerializer(featured_pizzas, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def popular(self, request):
        """Pizze più popolari"""
        popular_pizzas = self.get_queryset().order_by('-popularity_score')[:10]
        serializer = PizzaListSerializer(popular_pizzas, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def by_category(self, request):
        """Pizze per categoria"""
        category_slug = request.query_params.get('category')
        if category_slug:
            pizzas = self.get_queryset().filter(category__slug=category_slug)
            serializer = PizzaListSerializer(pizzas, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category parameter required'}, status=400)
    
    @action(detail=False, methods=['post'])
    def search_advanced(self, request):
        """Ricerca avanzata con filtri multipli"""
        filters = Q()
        
        # Filtri dalla request
        price_min = request.data.get('price_min')
        price_max = request.data.get('price_max')
        vegetarian = request.data.get('vegetarian')
        vegan = request.data.get('vegan')
        spicy = request.data.get('spicy')
        preparation_time_max = request.data.get('preparation_time_max')
        excluded_allergens = request.data.get('excluded_allergens', [])
        
        if price_min:
            filters &= Q(base_price__gte=price_min)
        if price_max:
            filters &= Q(base_price__lte=price_max)
        if vegetarian:
            filters &= Q(is_vegetarian=True)
        if vegan:
            filters &= Q(is_vegan=True)
        if spicy is not None:
            filters &= Q(is_spicy=spicy)
        if preparation_time_max:
            filters &= Q(preparation_time__lte=preparation_time_max)
        
        pizzas = self.get_queryset().filter(filters)
        
        # Escludi pizze con allergeni specificati
        if excluded_allergens:
            for allergen_id in excluded_allergens:
                pizzas = pizzas.exclude(
                    pizzaingredient__ingredient__allergens__id=allergen_id
                )
        
        pizzas = pizzas.distinct()
        serializer = PizzaListSerializer(pizzas, many=True)
        return Response({
            'results': serializer.data,
            'count': pizzas.count(),
            'filters_applied': request.data
        })