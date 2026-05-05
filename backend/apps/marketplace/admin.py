from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'price', 'stock', 'source_type', 'is_active')
    list_filter = ('source_type', 'is_active', 'category')
    search_fields = ('name', 'seller__username')

admin.site.register(Cart)
admin.site.register(CartItem)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'buyer', 'total', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method')
    search_fields = ('order_number', 'buyer__username', 'buyer_name')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'seller_name', 'quantity', 'subtotal', 'status')
    list_filter = ('status',)

admin.site.register(Review)
