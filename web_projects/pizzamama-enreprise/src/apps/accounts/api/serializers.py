from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.accounts.models import CustomUser, Profile, Address

class AddressSerializer(serializers.ModelSerializer):
    """Serializer per indirizzi di delivery"""
    
    class Meta:
        model = Address
        fields = [
            'id', 'label', 'street_address', 'city', 'postal_code', 
            'province', 'country', 'latitude', 'longitude', 'is_default', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        """Validazione business logic"""
        user = self.context['request'].user
        
        # Solo un indirizzo default per utente
        if data.get('is_default') and Address.objects.filter(user=user, is_default=True).exists():
            if not self.instance or not self.instance.is_default:
                raise serializers.ValidationError("Hai già un indirizzo principale. Disattiva quello attuale prima.")
        
        return data

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer per profilo utente con loyalty system"""
    addresses = AddressSerializer(many=True, read_only=True, source='user.addresses')
    loyalty_tier = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'avatar', 'bio', 'loyalty_points', 'total_orders', 'total_spent',
            'preferences', 'loyalty_tier', 'addresses', 'created_at', 'updated_at'
        ]
        read_only_fields = ['loyalty_points', 'total_orders', 'total_spent', 'created_at', 'updated_at']
    
    def get_loyalty_tier(self, obj):
        """Calcola tier loyalty in base ai punti"""
        points = obj.loyalty_points
        if points >= 1000:
            return {'name': 'Gold', 'icon': '🥇', 'benefits': 'Free delivery + 15% discount'}
        elif points >= 500:
            return {'name': 'Silver', 'icon': '🥈', 'benefits': 'Free delivery + 10% discount'}
        elif points >= 100:
            return {'name': 'Bronze', 'icon': '🥉', 'benefits': '5% discount'}
        else:
            return {'name': 'Basic', 'icon': '👤', 'benefits': 'Earn points on orders'}

class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer per CustomUser con profilo integrato"""
    profile = ProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'phone',
            'date_of_birth', 'preferred_language', 'marketing_consent', 
            'is_verified', 'profile', 'password', 'date_joined'
        ]
        read_only_fields = ['id', 'is_verified', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }
    
    def create(self, validated_data):
        """Crea utente con password hashata e profilo"""
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Crea profilo automaticamente
        Profile.objects.create(user=user)
        
        return user
    
    def update(self, instance, validated_data):
        """Update con gestione password"""
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    """Serializer per login con token response"""
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Credenziali non valide.')
            if not user.is_active:
                raise serializers.ValidationError('Account disattivato.')
            data['user'] = user
        else:
            raise serializers.ValidationError('Username e password richiesti.')
        
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer per registrazione nuovi utenti"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name', 'last_name', 'phone',
            'password', 'password_confirm', 'marketing_consent', 'preferred_language'
        ]
    
    def validate(self, data):
        """Validazione password match"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Le password non corrispondono.")
        return data
    
    def create(self, validated_data):
        """Crea utente con profilo"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Crea profilo automaticamente
        Profile.objects.create(user=user)
        
        return user