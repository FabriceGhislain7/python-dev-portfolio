from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from apps.products.models import Pizza, PizzaSize, Ingredient
from apps.accounts.models import Address
import uuid

class Cart(models.Model):
    """
    Carrello temporaneo per utenti (sessione o persistente)
    """
    # Utente (null per carrelli anonimi)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, null=True, blank=True, help_text="Session ID per utenti anonimi")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders_cart'
        verbose_name = 'Carrello'
        verbose_name_plural = 'Carrelli'
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())
    
    def __str__(self):
        if self.user:
            return f"Carrello di {self.user.username}"
        return f"Carrello anonimo {self.session_key}"

class CartItem(models.Model):
    """
    Elementi nel carrello con customization pizza
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.ForeignKey(PizzaSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    # Customization
    extra_ingredients = models.ManyToManyField(Ingredient, blank=True, help_text="Ingredienti extra")
    removed_ingredients = models.ManyToManyField(Ingredient, blank=True, related_name='removed_from_carts')
    special_instructions = models.TextField(blank=True, max_length=500)
    
    # Pricing snapshot
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Prezzo unitario al momento aggiunta")
    extra_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders_cart_item'
        verbose_name = 'Elemento Carrello'
        verbose_name_plural = 'Elementi Carrello'
    
    @property
    def subtotal(self):
        return (self.unit_price + self.extra_cost) * self.quantity
    
    def __str__(self):
        return f"{self.pizza.name} ({self.size.name}) x{self.quantity}"

class Order(models.Model):
    """
    Ordine principale con state machine e tracking
    """
    ORDER_STATUS_CHOICES = [
        ('pending', 'In Attesa'),
        ('confirmed', 'Confermato'),
        ('preparing', 'In Preparazione'),
        ('ready', 'Pronto'),
        ('out_for_delivery', 'In Consegna'),
        ('delivered', 'Consegnato'),
        ('cancelled', 'Annullato'),
        ('refunded', 'Rimborsato'),
    ]
    
    ORDER_TYPE_CHOICES = [
        ('delivery', 'Consegna a Domicilio'),
        ('pickup', 'Ritiro in Negozio'),
        ('dine_in', 'Consumo sul Posto'),
    ]
    
    # Identificazione
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, help_text="Numero ordine pubblico")
    
    # Customer info
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    
    # Contact details (snapshot al momento ordine)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=17)
    
    # Delivery/Pickup
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='delivery')
    delivery_address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL)
    
    # Address snapshot (in caso address viene cancellato)
    delivery_address_text = models.TextField(blank=True)
    
    # Order details
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    special_instructions = models.TextField(blank=True, max_length=1000)
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timing
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    actual_delivery_time = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'orders_order'
        verbose_name = 'Ordine'
        verbose_name_plural = 'Ordini'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Genera numero ordine sequenziale
            last_order = Order.objects.order_by('-created_at').first()
            if last_order and last_order.order_number:
                last_number = int(last_order.order_number.split('-')[-1])
                self.order_number = f"PME-{last_number + 1:06d}"
            else:
                self.order_number = "PME-000001"
        super().save(*args, **kwargs)
    
    @property
    def is_delivered(self):
        return self.status == 'delivered'
    
    @property
    def can_be_cancelled(self):
        return self.status in ['pending', 'confirmed']
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    def __str__(self):
        return f"Ordine {self.order_number} - {self.customer_name}"

class OrderItem(models.Model):
    """
    Righe ordine con snapshot pricing e customization
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.ForeignKey(PizzaSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    
    # Pricing snapshot (importante per storico prezzi)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    extra_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Customization snapshot
    extra_ingredients_snapshot = models.JSONField(default=list, help_text="Lista ingredienti extra al momento ordine")
    removed_ingredients_snapshot = models.JSONField(default=list, help_text="Lista ingredienti rimossi")
    special_instructions = models.TextField(blank=True, max_length=500)
    
    # Status per item specifico
    preparation_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'In Attesa'),
            ('preparing', 'In Preparazione'),
            ('ready', 'Pronto'),
        ],
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'orders_order_item'
        verbose_name = 'Elemento Ordine'
        verbose_name_plural = 'Elementi Ordine'
    
    @property
    def subtotal(self):
        return (self.unit_price + self.extra_cost) * self.quantity
    
    def __str__(self):
        return f"{self.order.order_number} - {self.pizza.name} x{self.quantity}"

class Payment(models.Model):
    """
    Tracking pagamenti con support multiple payment methods
    """
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'In Attesa'),
        ('processing', 'In Elaborazione'),
        ('completed', 'Completato'),
        ('failed', 'Fallito'),
        ('cancelled', 'Annullato'),
        ('refunded', 'Rimborsato'),
        ('partially_refunded', 'Parzialmente Rimborsato'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Carta di Credito'),
        ('paypal', 'PayPal'),
        ('cash', 'Contanti'),
        ('bank_transfer', 'Bonifico'),
        ('voucher', 'Buono'),
    ]
    
    # Identificazione
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # External payment gateway info
    transaction_id = models.CharField(max_length=100, blank=True, help_text="ID transazione gateway")
    gateway_response = models.JSONField(default=dict, blank=True, help_text="Response completa gateway")
    
    # Refund support
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    refund_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'orders_payment'
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamenti'
        ordering = ['-created_at']
    
    @property
    def is_successful(self):
        return self.status == 'completed'
    
    @property
    def remaining_amount(self):
        return self.amount - self.refund_amount
    
    def __str__(self):
        return f"Pagamento {self.order.order_number} - €{self.amount}"

class DeliveryInfo(models.Model):
    """
    Informazioni consegna con tracking GPS e driver assignment
    """
    DELIVERY_STATUS_CHOICES = [
        ('assigned', 'Assegnato'),
        ('picked_up', 'Ritirato'),
        ('in_transit', 'In Transito'),
        ('arrived', 'Arrivato'),
        ('delivered', 'Consegnato'),
        ('failed', 'Consegna Fallita'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery_info')
    
    # Driver assignment
    driver_name = models.CharField(max_length=100, blank=True)
    driver_phone = models.CharField(max_length=17, blank=True)
    vehicle_info = models.CharField(max_length=100, blank=True, help_text="Tipo veicolo, targa")
    
    # Tracking
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='assigned')
    estimated_arrival = models.DateTimeField(null=True, blank=True)
    actual_arrival = models.DateTimeField(null=True, blank=True)
    
    # GPS tracking
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Delivery notes
    delivery_notes = models.TextField(blank=True)
    customer_rating = models.PositiveIntegerField(
        null=True, blank=True, 
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders_delivery_info'
        verbose_name = 'Info Consegna'
        verbose_name_plural = 'Info Consegne'
    
    def __str__(self):
        return f"Consegna {self.order.order_number} - {self.status}"