from rest_framework import serializers
from apps.products.models import Category, Allergen, Ingredient, Pizza, PizzaSize, PizzaIngredient

class AllergenSerializer(serializers.ModelSerializer):
    """Serializer per allergeni con badge colorato"""
    
    class Meta:
        model = Allergen
        fields = ['id', 'name', 'symbol', 'description', 'color_code', 'regulation_code', 'is_major_allergen']

class CategorySerializer(serializers.ModelSerializer):
    """Serializer per categorie con gerarchia"""
    children = serializers.SerializerMethodField()
    pizza_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'image', 'parent', 'children',
            'is_active', 'sort_order', 'pizza_count', 'view_count'
        ]
        read_only_fields = ['view_count']
    
    def get_children(self, obj):
        """Sottocategorie annidate"""
        if obj.children.exists():
            return CategorySerializer(obj.children.filter(is_active=True), many=True).data
        return []
    
    def get_pizza_count(self, obj):
        """Numero pizze in categoria"""
        return obj.pizzas.filter(is_active=True).count()

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer per ingredienti con info stock"""
    allergens = AllergenSerializer(many=True, read_only=True)
    stock_status = serializers.CharField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Ingredient
        fields = [
            'id', 'name', 'slug', 'description', 'image', 'price_per_extra',
            'stock_quantity', 'minimum_stock', 'unit_of_measure', 'stock_status',
            'is_low_stock', 'allergens', 'is_vegetarian', 'is_vegan', 'is_gluten_free',
            'is_active', 'supplier', 'usage_count'
        ]
        read_only_fields = ['usage_count', 'stock_status', 'is_low_stock']

class PizzaSizeSerializer(serializers.ModelSerializer):
    """Serializer per taglie pizza"""
    
    class Meta:
        model = PizzaSize
        fields = ['id', 'name', 'diameter_cm', 'price_multiplier', 'is_active', 'sort_order']

class PizzaIngredientSerializer(serializers.ModelSerializer):
    """Serializer per ingredienti pizza con quantità"""
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = PizzaIngredient
        fields = ['ingredient', 'ingredient_id', 'quantity', 'is_removable', 'extra_cost']

class PizzaListSerializer(serializers.ModelSerializer):
    """Serializer leggero per lista pizze"""
    category = CategorySerializer(read_only=True)
    avg_rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    price_range = serializers.SerializerMethodField()
    
    class Meta:
        model = Pizza
        fields = [
            'id', 'name', 'slug', 'short_description', 'base_price', 'price_range',
            'image', 'category', 'is_vegetarian', 'is_vegan', 'is_spicy',
            'avg_rating', 'review_count', 'preparation_time', 'is_featured'
        ]
    
    def get_price_range(self, obj):
        """Calcola range prezzi per tutte le taglie"""
        sizes = PizzaSize.objects.filter(is_active=True)
        if sizes.exists():
            prices = [obj.base_price * size.price_multiplier for size in sizes]
            return {
                'min_price': min(prices),
                'max_price': max(prices)
            }
        return {'min_price': obj.base_price, 'max_price': obj.base_price}

class PizzaDetailSerializer(serializers.ModelSerializer):
    """Serializer completo per dettaglio pizza"""
    category = CategorySerializer(read_only=True)
    ingredients = PizzaIngredientSerializer(source='pizzaingredient_set', many=True, read_only=True)
    available_sizes = PizzaSizeSerializer(many=True, read_only=True, source='pizzasize_set')
    popularity_score = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Pizza
        fields = [
            'id', 'name', 'slug', 'description', 'short_description', 'base_price',
            'category', 'ingredients', 'available_sizes', 'image', 'gallery',
            'is_vegetarian', 'is_vegan', 'is_spicy', 'is_featured', 'is_active',
            'avg_rating', 'review_count', 'view_count', 'order_count',
            'popularity_score', 'calories_per_100g', 'preparation_time',
            'meta_title', 'meta_description', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'view_count', 'order_count', 'avg_rating', 'review_count',
            'popularity_score', 'created_at', 'updated_at'
        ]

class PizzaCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer per creazione/modifica pizze"""
    ingredients = PizzaIngredientSerializer(many=True, required=False)
    
    class Meta:
        model = Pizza
        fields = [
            'name', 'description', 'short_description', 'base_price', 'category',
            'image', 'gallery', 'is_vegetarian', 'is_vegan', 'is_spicy',
            'is_featured', 'is_active', 'calories_per_100g', 'preparation_time',
            'meta_title', 'meta_description', 'ingredients'
        ]
    
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        pizza = Pizza.objects.create(**validated_data)
        
        for ingredient_data in ingredients_data:
            PizzaIngredient.objects.create(pizza=pizza, **ingredient_data)
        
        return pizza
    
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        
        # Update pizza fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update ingredients if provided
        if ingredients_data is not None:
            instance.pizzaingredient_set.all().delete()
            for ingredient_data in ingredients_data:
                PizzaIngredient.objects.create(pizza=instance, **ingredient_data)
        
        return instance