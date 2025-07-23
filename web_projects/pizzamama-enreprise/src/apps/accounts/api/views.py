from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.accounts.models import CustomUser, Profile, Address
from .serializers import (
    CustomUserSerializer, ProfileSerializer, AddressSerializer,
    LoginSerializer, UserRegistrationSerializer
)

class CustomUserViewSet(viewsets.ModelViewSet):
    """ViewSet per gestione utenti con azioni custom"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_verified', 'preferred_language', 'marketing_consent']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username']
    ordering = ['-date_joined']
    
    def get_permissions(self):
        """Permissions diverse per azioni diverse"""
        if self.action in ['create', 'register']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['me', 'update_profile']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Endpoint per profilo utente corrente"""
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Registrazione nuovo utente"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': CustomUserSerializer(user).data,
                'token': token.key,
                'message': 'Registrazione completata con successo!'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login con token response"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': CustomUserSerializer(user).data,
                'token': token.key,
                'message': 'Login effettuato con successo!'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout con eliminazione token"""
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Logout effettuato con successo!'})
        except:
            return Response({'error': 'Token non trovato.'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet per gestione profili utente"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['loyalty_points']
    ordering_fields = ['loyalty_points', 'total_orders', 'total_spent']
    ordering = ['-loyalty_points']
    
    def get_queryset(self):
        """Utenti vedono solo il proprio profilo"""
        if self.request.user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_loyalty_points(self, request, pk=None):
        """Aggiunge punti loyalty (solo admin)"""
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        profile = self.get_object()
        points = request.data.get('points', 0)
        
        if points > 0:
            profile.loyalty_points += points
            profile.save()
            return Response({
                'message': f'{points} punti aggiunti!',
                'new_total': profile.loyalty_points
            })
        return Response({'error': 'Punti devono essere > 0'}, status=status.HTTP_400_BAD_REQUEST)

class AddressViewSet(viewsets.ModelViewSet):
    """ViewSet per gestione indirizzi di delivery"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_default', 'city', 'country']
    search_fields = ['label', 'street_address', 'city']
    
    def get_queryset(self):
        """Utenti vedono solo i propri indirizzi"""
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Associa indirizzo all'utente corrente"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """Imposta indirizzo come principale"""
        address = self.get_object()
        
        # Reset tutti gli altri indirizzi
        Address.objects.filter(user=request.user).update(is_default=False)
        
        # Imposta questo come default
        address.is_default = True
        address.save()
        
        return Response({
            'message': f'Indirizzo "{address.label}" impostato come principale',
            'address': AddressSerializer(address).data
        })