from django.db import models
from django.conf import settings

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def items_count(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Panier de {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalogue.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Prix au moment de l'ajout (snapshot)")
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('PAID', 'Payé'),
        ('CONFIRMED', 'Confirmé'),
        ('SHIPPED', 'Expédié'),
        ('DELIVERED', 'Livré'),
        ('CANCELLED', 'Annulé'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('MVOLA', 'MVola'),
        ('ORANGE_MONEY', 'Orange Money'),
        ('STRIPE', 'Stripe'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('ESCROWED', 'Bloqué (Escrow)'),
        ('RELEASED', 'Libéré'),
        ('REFUNDED', 'Remboursé'),
    ]

    order_number = models.CharField(max_length=50, unique=True, help_text="e.g., CMD-2024-0001")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    buyer_name = models.CharField(max_length=255)
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    
    delivery_name = models.CharField(max_length=255)
    delivery_phone = models.CharField(max_length=50)
    delivery_address = models.TextField()
    delivery_city = models.CharField(max_length=100)
    delivery_region = models.CharField(max_length=100)
    delivery_notes = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number

    def decrease_stock(self):
        """Réduit le stock des produits commandés"""
        # On évite de déduire deux fois le stock (ex: double clic ou retry)
        if hasattr(self, '_stock_decreased') and self._stock_decreased:
            return
            
        for item in self.items.all():
            if item.product:
                item.product.stock -= item.quantity
                item.product.save()
        
        self._stock_decreased = True

class OrderItem(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmé'),
        ('PREPARING', 'En préparation'),
        ('SHIPPED', 'Expédié'),
        ('DELIVERED', 'Livré'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalogue.Product', on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='order_items_sold')
    
    seller_name = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    product_image = models.URLField(max_length=500, null=True, blank=True)
    
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Prix unitaire au moment de la commande (snapshot)")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.quantity} x {self.product_name} (Commande: {self.order.order_number})"

class Review(models.Model):
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
