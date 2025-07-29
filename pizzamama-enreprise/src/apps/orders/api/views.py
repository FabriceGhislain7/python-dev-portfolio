from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.utils import timezone
from apps.orders.models import Cart, CartItem, Order, OrderItem, Payment, DeliveryInfo
from .serializers import (
    CartSerializer, CartItemSerializer, OrderListSerializer, 
    OrderDetailSerializer, OrderCreateSerializer, PaymentSerializer
)

class CartViewSet(viewsets.ModelViewSet):
    """ViewSet per gestione carrello"""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Carrello dell'utente corrente"""
        return Cart.objects.filter(user=self.request.user)
    
    def get_object(self):
        """Get or create cart per utente"""
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Aggiungi item al carrello"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart)
            
            # Ritorna carrello aggiornato
            cart_serializer = CartSerializer(cart)
            return Response({
                'message': 'Item aggiunto al carrello',
                'cart': cart_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def update_item(self, request):
        """Aggiorna quantità item carrello"""
        cart = self.get_object()
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity', 1)
        
        try:
            item = cart.items.get(id=item_id)
            if quantity <= 0:
                item.delete()
                message = 'Item rimosso dal carrello'
            else:
                item.quantity = quantity
                item.save()
                message = 'Quantità aggiornata'
            
            cart_serializer = CartSerializer(cart)
            return Response({
                'message': message,
                'cart': cart_serializer.data
            })
        except CartItem.DoesNotExist:
            return Response({'error': 'Item non trovato'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Rimuovi item dal carrello"""
        cart = self.get_object()
        item_id = request.data.get('item_id')
        
        try:
            item = cart.items.get(id=item_id)
            item.delete()
            
            cart_serializer = CartSerializer(cart)
            return Response({
                'message': 'Item rimosso dal carrello',
                'cart': cart_serializer.data
            })
        except CartItem.DoesNotExist:
            return Response({'error': 'Item non trovato'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Svuota carrello"""
        cart = self.get_object()
        cart.items.all().delete()
        
        return Response({'message': 'Carrello svuotato'})

class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet per gestione ordini"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'order_type']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Ordini dell'utente corrente (o tutti per admin)"""
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Serializer diverso per azioni diverse"""
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        else:
            return OrderDetailSerializer
    
    def perform_create(self, serializer):
        """Crea ordine per utente corrente"""
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Annulla ordine se possibile"""
        order = self.get_object()
        
        if not order.can_be_cancelled:
            return Response({
                'error': 'Ordine non può essere annullato in questo stato'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'cancelled'
        order.save()
        
        return Response({
            'message': f'Ordine {order.order_number} annullato',
            'order': OrderDetailSerializer(order).data
        })
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Conferma ordine (solo staff)"""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        order = self.get_object()
        order.status = 'confirmed'
        order.confirmed_at = timezone.now()
        order.save()
        
        return Response({
            'message': f'Ordine {order.order_number} confermato',
            'order': OrderDetailSerializer(order).data
        })
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Aggiorna status ordine (solo staff)"""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Order.ORDER_STATUS_CHOICES):
            return Response({'error': 'Status non valido'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        
        # Aggiorna timestamp specifici
        if new_status == 'confirmed':
            order.confirmed_at = timezone.now()
        elif new_status == 'delivered':
            order.delivered_at = timezone.now()
        
        order.save()
        
        return Response({
            'message': f'Status ordine aggiornato a {order.get_status_display()}',
            'order': OrderDetailSerializer(order).data
        })
    
    @action(detail=True)
    def track(self, request, pk=None):
        """Tracking ordine con info delivery"""
        order = self.get_object()
        
        tracking_info = {
            'order_number': order.order_number,
            'status': order.status,
            'status_display': order.get_status_display(),
            'estimated_delivery': order.estimated_delivery_time,
            'created_at': order.created_at,
            'confirmed_at': order.confirmed_at,
            'delivered_at': order.delivered_at,
        }
        
        # Aggiungi info delivery se disponibili
        if hasattr(order, 'delivery_info'):
            delivery = order.delivery_info
            tracking_info.update({
                'driver_name': delivery.driver_name,
                'driver_phone': delivery.driver_phone,
                'delivery_status': delivery.status,
                'estimated_arrival': delivery.estimated_arrival,
                'current_location': {
                    'latitude': delivery.current_latitude,
                    'longitude': delivery.current_longitude
                } if delivery.current_latitude and delivery.current_longitude else None
            })
        
        return Response(tracking_info)

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet read-only per pagamenti"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'method']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Pagamenti dell'utente corrente"""
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(order__user=self.request.user)