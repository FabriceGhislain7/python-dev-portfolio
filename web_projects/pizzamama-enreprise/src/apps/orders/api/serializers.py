from rest_framework import serializers
from decimal import Decimal
from apps.orders.models import Cart, CartItem, Order, OrderItem, Payment, DeliveryInfo
from apps.products.api.serializers import PizzaListSerializer, PizzaSizeSerializer, IngredientSerializer
from apps.accounts.api.serializers import AddressSerializer

class CartItemSerializer(serializers.ModelSerializer):
    """Serializer per elementi carrello con dettagli prodotto"""
    pizza = PizzaListSerializer(read_only=True)
    pizza_id = serializers.IntegerField(write_only=True)
    size = PizzaSizeSerializer(read_only=True)
    size_id = serializers.IntegerField(write_only=True)
    extra_ingredients = IngredientSerializer(many=True, read_only=True)
    extra_ingredients_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    removed_ingredients = IngredientSerializer(many=True, read_only=True)
    removed_ingredients_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    subtotal = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'pizza', 'pizza_id', 'size', 'size_id', 'quantity',
            'extra_ingredients', 'extra_ingredients_ids', 'removed_ingredients', 
            'removed_ingredients_ids', 'special_instructions', 'unit_price', 
            'extra_cost', 'subtotal', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'unit_price', 'extra_cost', 'subtotal', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        extra_ingredients_ids = validated_data.pop('extra_ingredients_ids', [])
        removed_ingredients_ids = validated_data.pop('removed_ingredients_ids', [])
        
        # Calcola prezzo con taglia
        pizza_id = validated_data['pizza_id']
        size_id = validated_data['size_id']
        pizza = validated_data['pizza_id']
        size = validated_data['size_id']
        
        from apps.products.models import Pizza, PizzaSize
        pizza_obj = Pizza.objects.get(id=pizza_id)
        size_obj = PizzaSize.objects.get(id=size_id)
        
        unit_price = pizza_obj.base_price * size_obj.price_multiplier
        
        # Calcola costo extra ingredienti
        extra_cost = Decimal('0.00')
        if extra_ingredients_ids:
            from apps.products.models import Ingredient
            extra_ingredients = Ingredient.objects.filter(id__in=extra_ingredients_ids)
            extra_cost = sum(ing.price_per_extra for ing in extra_ingredients)
        
        validated_data['unit_price'] = unit_price
        validated_data['extra_cost'] = extra_cost
        
        cart_item = CartItem.objects.create(**validated_data)
        
        # Associa ingredienti extra e rimossi
        if extra_ingredients_ids:
            cart_item.extra_ingredients.set(extra_ingredients_ids)
        if removed_ingredients_ids:
            cart_item.removed_ingredients.set(removed_ingredients_ids)
        
        return cart_item

class CartSerializer(serializers.ModelSerializer):
    """Serializer per carrello con totali"""
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer per elementi ordine con snapshot"""
    pizza_name = serializers.CharField(source='pizza.name', read_only=True)
    size_name = serializers.CharField(source='size.name', read_only=True)
    subtotal = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'pizza_name', 'size_name', 'quantity', 'unit_price', 'extra_cost',
            'subtotal', 'extra_ingredients_snapshot', 'removed_ingredients_snapshot',
            'special_instructions', 'preparation_status'
        ]
        read_only_fields = ['id', 'subtotal']

class PaymentSerializer(serializers.ModelSerializer):
    """Serializer per pagamenti"""
    is_successful = serializers.BooleanField(read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'amount', 'method', 'status', 'transaction_id', 'gateway_response',
            'refund_amount', 'refund_reason', 'is_successful', 'remaining_amount',
            'created_at', 'processed_at'
        ]
        read_only_fields = ['id', 'gateway_response', 'created_at', 'processed_at']

class DeliveryInfoSerializer(serializers.ModelSerializer):
    """Serializer per info delivery"""
    
    class Meta:
        model = DeliveryInfo
        fields = [
            'driver_name', 'driver_phone', 'vehicle_info', 'status',
            'estimated_arrival', 'actual_arrival', 'current_latitude',
            'current_longitude', 'delivery_notes', 'customer_rating'
        ]

class OrderListSerializer(serializers.ModelSerializer):
    """Serializer leggero per lista ordini"""
    customer_name = serializers.CharField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer_name', 'status', 'status_display',
            'order_type', 'total_amount', 'total_items', 'created_at'
        ]

class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer completo per dettaglio ordine"""
    items = OrderItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    delivery_info = DeliveryInfoSerializer(read_only=True)
    delivery_address_details = AddressSerializer(source='delivery_address', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    order_type_display = serializers.CharField(source='get_order_type_display', read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    is_delivered = serializers.BooleanField(read_only=True)
    can_be_cancelled = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer_name', 'customer_email', 'customer_phone',
            'status', 'status_display', 'order_type', 'order_type_display',
            'delivery_address_details', 'delivery_address_text', 'special_instructions',
            'subtotal', 'delivery_fee', 'tax_amount', 'discount_amount', 'total_amount',
            'items', 'payments', 'delivery_info', 'total_items', 'is_delivered',
            'can_be_cancelled', 'estimated_delivery_time', 'actual_delivery_time',
            'created_at', 'confirmed_at', 'delivered_at'
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer per creazione ordini da carrello"""
    delivery_address_id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Order
        fields = [
            'order_type', 'delivery_address_id', 'special_instructions'
        ]
    
    def validate(self, data):
        """Validazione ordine"""
        if data.get('order_type') == 'delivery' and not data.get('delivery_address_id'):
            raise serializers.ValidationError('Delivery address required for delivery orders')
        return data
    
    def create(self, validated_data):
        """Crea ordine da carrello utente"""
        user = self.context['request'].user
        
        # Trova carrello utente
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError('Carrello vuoto')
        
        if not cart.items.exists():
            raise serializers.ValidationError('Carrello vuoto')
        
        # Calcola totali
        subtotal = cart.total_price
        delivery_fee = Decimal('3.00') if validated_data.get('order_type') == 'delivery' else Decimal('0.00')
        tax_amount = subtotal * Decimal('0.22')  # IVA 22%
        total_amount = subtotal + delivery_fee + tax_amount
        
        # Crea ordine
        order_data = {
            'user': user,
            'customer_name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'customer_email': user.email,
            'customer_phone': user.phone or '',
            'subtotal': subtotal,
            'delivery_fee': delivery_fee,
            'tax_amount': tax_amount,
            'total_amount': total_amount,
            **validated_data
        }
        
        # Gestisci indirizzo delivery
        if validated_data.get('delivery_address_id'):
            from apps.accounts.models import Address
            try:
                address = Address.objects.get(id=validated_data['delivery_address_id'], user=user)
                order_data['delivery_address'] = address
                order_data['delivery_address_text'] = f"{address.street_address}, {address.city}, {address.postal_code}"
            except Address.DoesNotExist:
                raise serializers.ValidationError('Indirizzo delivery non valido')
        
        order = Order.objects.create(**order_data)
        
        # Crea order items da cart items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                pizza=cart_item.pizza,
                size=cart_item.size,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                extra_cost=cart_item.extra_cost,
                extra_ingredients_snapshot=[ing.name for ing in cart_item.extra_ingredients.all()],
                removed_ingredients_snapshot=[ing.name for ing in cart_item.removed_ingredients.all()],
                special_instructions=cart_item.special_instructions
            )
        
        # Svuota carrello
        cart.items.all().delete()
        
        return order