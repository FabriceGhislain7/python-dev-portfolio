from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Cart, CartItem, Order, OrderItem, Payment, DeliveryInfo

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ['pizza', 'size', 'quantity', 'unit_price', 'extra_cost', 'subtotal']
    readonly_fields = ['subtotal']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_display', 'total_items', 'total_price', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'session_key']
    inlines = [CartItemInline]
    
    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        return f"Anonimo ({obj.session_key})"
    user_display.short_description = 'Utente'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['pizza', 'size', 'quantity', 'unit_price', 'extra_cost', 'subtotal', 'preparation_status']
    readonly_fields = ['subtotal']

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ['amount', 'method', 'status', 'transaction_id', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'customer_name', 'status_colored', 'order_type', 
        'total_amount', 'total_items', 'created_at'
    ]
    list_filter = ['status', 'order_type', 'created_at', 'confirmed_at']
    search_fields = ['order_number', 'customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['id', 'order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline, PaymentInline]
    
    fieldsets = (
        ('Identificazione', {
            'fields': ('id', 'order_number', 'status')
        }),
        ('Cliente', {
            'fields': ('user', 'customer_name', 'customer_email', 'customer_phone')
        }),
        ('Consegna', {
            'fields': ('order_type', 'delivery_address', 'delivery_address_text', 'special_instructions')
        }),
        ('Prezzi', {
            'fields': ('subtotal', 'delivery_fee', 'tax_amount', 'discount_amount', 'total_amount')
        }),
        ('Timing', {
            'fields': ('estimated_delivery_time', 'actual_delivery_time', 'confirmed_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def status_colored(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#17a2b8',
            'preparing': '#fd7e14',
            'ready': '#20c997',
            'out_for_delivery': '#6f42c1',
            'delivered': '#28a745',
            'cancelled': '#dc3545',
            'refunded': '#6c757d',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'
    
    actions = ['mark_as_confirmed', 'mark_as_preparing', 'mark_as_ready']
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='confirmed',
            confirmed_at=timezone.now()
        )
        self.message_user(request, f'{updated} ordini confermati.')
    mark_as_confirmed.short_description = 'Conferma ordini selezionati'
    
    def mark_as_preparing(self, request, queryset):
        updated = queryset.filter(status='confirmed').update(status='preparing')
        self.message_user(request, f'{updated} ordini in preparazione.')
    mark_as_preparing.short_description = 'Segna come "in preparazione"'
    
    def mark_as_ready(self, request, queryset):
        updated = queryset.filter(status='preparing').update(status='ready')
        self.message_user(request, f'{updated} ordini pronti.')
    mark_as_ready.short_description = 'Segna come "pronti"'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'amount', 'method', 'status_colored', 'transaction_id', 'created_at']
    list_filter = ['status', 'method', 'created_at']
    search_fields = ['order__order_number', 'transaction_id']
    readonly_fields = ['id', 'created_at', 'processed_at']
    
    def status_colored(self, obj):
        colors = {
            'pending': '#ffc107',
            'processing': '#17a2b8',
            'completed': '#28a745',
            'failed': '#dc3545',
            'cancelled': '#6c757d',
            'refunded': '#fd7e14',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'

@admin.register(DeliveryInfo)
class DeliveryInfoAdmin(admin.ModelAdmin):
    list_display = ['order', 'driver_name', 'status_colored', 'estimated_arrival', 'customer_rating']
    list_filter = ['status', 'created_at', 'customer_rating']
    search_fields = ['order__order_number', 'driver_name', 'driver_phone']
    
    fieldsets = (
        ('Ordine', {
            'fields': ('order', 'status')
        }),
        ('Driver', {
            'fields': ('driver_name', 'driver_phone', 'vehicle_info')
        }),
        ('Tracking', {
            'fields': ('estimated_arrival', 'actual_arrival', 'current_latitude', 'current_longitude')
        }),
        ('Feedback', {
            'fields': ('delivery_notes', 'customer_rating')
        })
    )
    
    def status_colored(self, obj):
        colors = {
            'assigned': '#ffc107',
            'picked_up': '#17a2b8',
            'in_transit': '#fd7e14',
            'arrived': '#20c997',
            'delivered': '#28a745',
            'failed': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'