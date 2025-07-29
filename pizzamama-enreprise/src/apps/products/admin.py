from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Allergen, Ingredient, Pizza, PizzaSize, PizzaIngredient

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'sort_order', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['sort_order', 'name']
    list_editable = ['sort_order', 'is_active']

    fieldsets = (
        ('Informazioni Base', {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        ('Media e Visibilità', {
            'fields': ('image', 'is_active', 'sort_order')
        }),
    )

@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'colored_badge', 'description']
    search_fields = ['name', 'symbol', 'description']
    ordering = ['name']

    def colored_badge(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-weight: bold;">{}</span>',
            obj.color_code, obj.symbol
        )
    colored_badge.short_description = 'Badge'
    colored_badge.admin_order_field = 'symbol'

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price_per_extra',
        'stock_status',
        'is_vegetarian',
        'is_vegan',
        'is_extra',
        'is_active'
    ]
    list_filter = [
        'is_vegetarian',
        'is_vegan',
        'is_extra',
        'is_active',
        'allergens',
        'unit_of_measure'
    ]
    search_fields = ['name', 'description']
    filter_horizontal = ['allergens']
    list_editable = ['price_per_extra', 'is_active']
    ordering = ['name']

    fieldsets = (
        ('Informazioni Base', {
            'fields': ('name', 'description', 'image')
        }),
        ('Pricing', {
            'fields': ('cost_per_unit', 'price_per_extra')
        }),
        ('Stock Management', {
            'fields': ('stock_quantity', 'minimum_stock', 'unit_of_measure')
        }),
        ('Categorizzazione', {
            'fields': ('allergens', 'is_vegetarian', 'is_vegan', 'is_extra')
        }),
        ('Visibilità', {
            'fields': ('is_active',)
        }),
    )

    def stock_status(self, obj):
        if obj.is_low_stock:
            color = 'red'
            status = f'⚠️ Basso ({obj.stock_quantity} {obj.unit_of_measure})'
        else:
            color = 'green'
            status = f'✅ OK ({obj.stock_quantity} {obj.unit_of_measure})'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, status
        )
    stock_status.short_description = 'Status Stock'
    stock_status.admin_order_field = 'stock_quantity'

@admin.register(PizzaSize)
class PizzaSizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'diameter_cm', 'price_multiplier', 'is_active', 'sort_order']
    list_editable = ['price_multiplier', 'is_active', 'sort_order']
    ordering = ['sort_order', 'diameter_cm']

    fieldsets = (
        ('Informazioni Base', {
            'fields': ('name', 'diameter_cm')
        }),
        ('Pricing', {
            'fields': ('price_multiplier',)
        }),
        ('Visibilità', {
            'fields': ('is_active', 'sort_order')
        }),
    )

class PizzaIngredientInline(admin.TabularInline):
    model = PizzaIngredient
    extra = 1
    autocomplete_fields = ['ingredient']

    fields = ['ingredient', 'quantity', 'is_removable', 'is_extra_charge']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ingredient":
            kwargs["queryset"] = Ingredient.objects.filter(is_active=True).order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'base_price',
        'avg_rating',
        'total_reviews',
        'is_featured',
        'is_vegetarian',
        'is_vegan',
        'is_active'
    ]
    list_filter = [
        'category',
        'is_featured',
        'is_active',
        'is_vegetarian',
        'is_vegan',
        'is_spicy',
        'created_at'
    ]
    search_fields = ['name', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = []
    inlines = [PizzaIngredientInline]
    list_editable = ['is_featured', 'is_active']
    ordering = ['-is_featured', '-avg_rating', 'name']

    readonly_fields = ['avg_rating', 'total_reviews', 'popularity_score', 'created_at', 'updated_at']

    fieldsets = (
        ('Informazioni Base', {
            'fields': ('name', 'slug', 'category', 'description', 'short_description')
        }),
        ('Prezzo e Caratteristiche', {
            'fields': ('base_price', 'preparation_time_minutes', 'calories_per_100g')
        }),
        ('Media', {
            'fields': ('image', 'gallery_images')
        }),
        ('Classificazione', {
            'fields': ('is_vegetarian', 'is_vegan', 'is_spicy')
        }),
        ('Visibilità e Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Analytics (Auto-popolato)', {
            'fields': ('popularity_score', 'avg_rating', 'total_reviews'),
            'classes': ('collapse',),
            'description': 'Questi campi sono popolati automaticamente dal sistema.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

    def save_model(self, request, obj, form, change):
        # Auto-populate meta fields if empty
        if not obj.meta_title:
            obj.meta_title = obj.name[:60]
        if not obj.meta_description:
            obj.meta_description = obj.short_description[:160] if obj.short_description else obj.description[:160]
        super().save_model(request, obj, form, change)

# Custom admin site configurations
admin.site.site_header = "PizzaMama Enterprise Admin"
admin.site.site_title = "PizzaMama Admin"
admin.site.index_title = "Gestione E-commerce"

# Register PizzaIngredient separately for direct access if needed
@admin.register(PizzaIngredient)
class PizzaIngredientAdmin(admin.ModelAdmin):
    list_display = ['pizza', 'ingredient', 'quantity', 'is_removable', 'is_extra_charge']
    list_filter = ['is_removable', 'is_extra_charge', 'pizza__category']
    search_fields = ['pizza__name', 'ingredient__name']
    autocomplete_fields = ['pizza', 'ingredient']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('pizza', 'ingredient')