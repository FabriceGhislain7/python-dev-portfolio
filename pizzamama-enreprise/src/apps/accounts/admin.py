from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Address

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    fields = ['label', 'street_address', 'city', 'postal_code', 'is_default']

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username', 'email', 'get_full_name', 'phone', 
        'is_verified', 'marketing_consent', 'is_active', 'date_joined'
    ]
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'is_verified', 
        'marketing_consent', 'preferred_language', 'date_joined'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['-date_joined']
    filter_horizontal = ['groups', 'user_permissions']
    inlines = [AddressInline]  # ← SPOSTATO QUI (era in ProfileAdmin)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informazioni Aggiuntive', {
            'fields': ('phone', 'date_of_birth', 'preferred_language')
        }),
        ('Privacy & Marketing', {
            'fields': ('marketing_consent', 'is_verified'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'date_joined', 'last_login']
    
    actions = ['verify_users', 'unverify_users', 'enable_marketing']
    
    def verify_users(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} utenti verificati.')
    verify_users.short_description = 'Verifica utenti selezionati'
    
    def unverify_users(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} utenti non verificati.')
    unverify_users.short_description = 'Rimuovi verifica utenti'
    
    def enable_marketing(self, request, queryset):
        updated = queryset.update(marketing_consent=True)
        self.message_user(request, f'{updated} utenti hanno acconsentito al marketing.')
    enable_marketing.short_description = 'Abilita consenso marketing'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'loyalty_points', 'total_orders', 'total_spent', 
        'loyalty_tier', 'has_avatar', 'created_at'
    ]
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'bio']
    readonly_fields = ['created_at', 'updated_at']
    # inlines = [AddressInline]  ← RIMOSSO DA QUI
    
    fieldsets = (
        ('Utente', {
            'fields': ('user', 'avatar', 'bio')
        }),
        ('Loyalty System', {
            'fields': ('loyalty_points', 'total_orders', 'total_spent')
        }),
        ('Preferenze', {
            'fields': ('preferences',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def loyalty_tier(self, obj):
        if obj.loyalty_points >= 1000:
            return format_html(
                '<span style="color: gold; font-weight: bold;">🥇 Gold</span>'
            )
        elif obj.loyalty_points >= 500:
            return format_html(
                '<span style="color: silver; font-weight: bold;">🥈 Silver</span>'
            )
        elif obj.loyalty_points >= 100:
            return format_html(
                '<span style="color: #cd7f32; font-weight: bold;">🥉 Bronze</span>'
            )
        else:
            return format_html(
                '<span style="color: gray;">👤 Basic</span>'
            )
    loyalty_tier.short_description = 'Tier'
    
    def has_avatar(self, obj):
        if obj.avatar:
            return format_html(
                '<span style="color: green;">✅ Sì</span>'
            )
        return format_html(
            '<span style="color: red;">❌ No</span>'
        )
    has_avatar.short_description = 'Avatar'
    has_avatar.boolean = True

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'label', 'city', 'postal_code', 
        'country', 'is_default', 'has_coordinates'
    ]
    list_filter = ['is_default', 'country', 'province', 'created_at']
    search_fields = [
        'user__username', 'label', 'street_address', 
        'city', 'postal_code'
    ]
    ordering = ['user__username', '-is_default', 'label']
    
    fieldsets = (
        ('Utente', {
            'fields': ('user', 'label', 'is_default')
        }),
        ('Indirizzo', {
            'fields': ('street_address', 'city', 'postal_code', 'province', 'country')
        }),
        ('Coordinate GPS', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',),
            'description': 'Coordinate per ottimizzazione delivery'
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']
    
    def has_coordinates(self, obj):
        if obj.latitude and obj.longitude:
            return format_html(
                '<span style="color: green;">📍 Sì</span>'
            )
        return format_html(
            '<span style="color: orange;">📍 No</span>'
        )
    has_coordinates.short_description = 'GPS'
    has_coordinates.boolean = True
    
    actions = ['set_as_default', 'add_gps_coordinates']
    
    def set_as_default(self, request, queryset):
        for address in queryset:
            # Reset all other addresses for this user
            Address.objects.filter(user=address.user).update(is_default=False)
            # Set selected as default
            address.is_default = True
            address.save()
        self.message_user(request, f'{queryset.count()} indirizzi impostati come default.')
    set_as_default.short_description = 'Imposta come indirizzo principale'
    
    def add_gps_coordinates(self, request, queryset):
        # Placeholder per integrazione futura con geocoding API
        self.message_user(request, 'Funzione geocoding in sviluppo.')
    add_gps_coordinates.short_description = 'Aggiungi coordinate GPS'

# Personalizzazione admin site
admin.site.site_header = "PizzaMama Enterprise Admin"
admin.site.site_title = "PizzaMama Admin" 
admin.site.index_title = "Gestione Accounts & Profili"