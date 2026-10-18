from django.contrib import admin
from .models import Product, Category, Cart, CartItem, Order, OrderItem
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
class OrderItemInLine(admin.TabularInline):
    model=OrderItem
    extra=0
admin.site.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=["id","user","status","created_at"]
    list_filter=["status","created_at"]
    inlines=[OrderItemInLine]