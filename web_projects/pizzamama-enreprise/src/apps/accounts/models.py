from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    """
    Custom User model esteso per PizzaMama
    """
    # Contact info
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Personal info
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Preferences
    preferred_language = models.CharField(
        max_length=5, 
        choices=[('it', 'Italiano'), ('en', 'English')], 
        default='it'
    )
    
    # Privacy & Marketing
    marketing_consent = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'
    
    def __str__(self):
        return f"{self.username} - {self.get_full_name()}"

class Address(models.Model):
    """
    Indirizzi di consegna multipli per utente
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=50, help_text="es. Casa, Ufficio, Altro")
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    province = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default='Italia')
    
    # Coordinate per delivery (opzionale)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'accounts_address'
        verbose_name = 'Indirizzo'
        verbose_name_plural = 'Indirizzi'
        unique_together = [['user', 'label']]
    
    def __str__(self):
        return f"{self.user.username} - {self.label}"

class Profile(models.Model):
    """
    Profilo utente esteso con preferenze e loyalty
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # Loyalty system
    loyalty_points = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Preferences JSON field per dietary restrictions, favorite pizzas, etc.
    preferences = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_profile'
        verbose_name = 'Profilo'
        verbose_name_plural = 'Profili'
    
    def __str__(self):
        return f"Profilo di {self.user.username}"