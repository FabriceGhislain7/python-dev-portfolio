from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class Category(models.Model):
    """
    Categorie pizze gerarchiche (es. Classiche, Gourmet, Vegane)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)

    # Gerarchia categorie (categoria parent opzionale)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    # SEO e visibilità
    image = models.ImageField(upload_to='categories/', blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products_category'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorie'
        ordering = ['sort_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})

class Allergen(models.Model):
    """
    Allergeni per compliance alimentare
    """
    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=10, help_text="Simbolo standard (es. G per glutine)")
    description = models.TextField(help_text="Descrizione dettagliata allergene")
    color_code = models.CharField(max_length=7, default="#FF0000", help_text="Codice colore hex per UI")

    class Meta:
        db_table = 'products_allergen'
        verbose_name = 'Allergene'
        verbose_name_plural = 'Allergeni'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class Ingredient(models.Model):
    """
    Ingredienti con pricing e gestione stock
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    # Pricing
    cost_per_unit = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Costo per unità (€)"
    )
    price_per_extra = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        help_text="Prezzo extra per cliente (€)"
    )

    # Stock management
    stock_quantity = models.PositiveIntegerField(default=0)
    minimum_stock = models.PositiveIntegerField(default=10)
    unit_of_measure = models.CharField(
        max_length=20,
        choices=[
            ('g', 'Grammi'),
            ('ml', 'Millilitri'),
            ('piece', 'Pezzo'),
            ('slice', 'Fetta'),
        ],
        default='g'
    )

    # Categorizzazione
    allergens = models.ManyToManyField(Allergen, blank=True)
    is_vegetarian = models.BooleanField(default=True)
    is_vegan = models.BooleanField(default=False)
    is_extra = models.BooleanField(default=False, help_text="Disponibile come extra a pagamento")

    # Visibilità
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='ingredients/', blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products_ingredient'
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredienti'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.minimum_stock

class PizzaSize(models.Model):
    """
    Taglie pizza con pricing differenziato
    """
    name = models.CharField(max_length=20, unique=True)  # Small, Medium, Large, Family
    diameter_cm = models.PositiveIntegerField(help_text="Diametro in centimetri")
    price_multiplier = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1.0,
        help_text="Moltiplicatore prezzo base (1.0 = prezzo base)"
    )
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'products_pizza_size'
        verbose_name = 'Taglia Pizza'
        verbose_name_plural = 'Taglie Pizza'
        ordering = ['sort_order', 'diameter_cm']

    def __str__(self):
        return f"{self.name} ({self.diameter_cm}cm)"

class Pizza(models.Model):
    """
    Modello principale pizza
    """
    # Basic info
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200, blank=True)

    # Categorizzazione
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='pizzas'
    )

    # Ingredienti
    ingredients = models.ManyToManyField(
        Ingredient,
        through='PizzaIngredient',
        related_name='pizzas'
    )

    # Pricing
    base_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Prezzo base per taglia media"
    )

    # Nutritional info
    calories_per_100g = models.PositiveIntegerField(null=True, blank=True)
    preparation_time_minutes = models.PositiveIntegerField(default=15)

    # Media
    image = models.ImageField(upload_to='pizzas/')
    gallery_images = models.JSONField(default=list, blank=True, help_text="Array di URL immagini aggiuntive")

    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Status e visibilità
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)

    # Analytics fields (popolati da ML)
    popularity_score = models.FloatField(default=0.0)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products_pizza'
        verbose_name = 'Pizza'
        verbose_name_plural = 'Pizze'
        ordering = ['-is_featured', '-popularity_score', 'name']
        indexes = [
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['avg_rating']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pizza-detail', kwargs={'slug': self.slug})

    def get_price_for_size(self, size):
        """Calcola prezzo per una specifica taglia"""
        if isinstance(size, str):
            size = PizzaSize.objects.get(name=size)
        return self.base_price * size.price_multiplier

    @property
    def allergens(self):
        """Restituisce tutti gli allergeni della pizza"""
        return Allergen.objects.filter(
            ingredient__pizzaingredient__pizza=self
        ).distinct()

class PizzaIngredient(models.Model):
    """
    Tabella intermedia per ingredienti pizza con quantità
    """
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Quantità ingrediente per pizza media"
    )
    is_removable = models.BooleanField(
        default=True,
        help_text="Cliente può rimuovere questo ingrediente"
    )
    is_extra_charge = models.BooleanField(
        default=False,
        help_text="Ingrediente premium con costo extra"
    )

    class Meta:
        db_table = 'products_pizza_ingredient'
        unique_together = [['pizza', 'ingredient']]
        verbose_name = 'Ingrediente Pizza'
        verbose_name_plural = 'Ingredienti Pizza'

    def __str__(self):
        return f"{self.pizza.name} - {self.ingredient.name} ({self.quantity}{self.ingredient.unit_of_measure})"