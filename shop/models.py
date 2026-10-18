from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    available = models.BooleanField(default=True)
    rate = models.FloatField(default=0)
    description = models.TextField(default="")
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/",blank=True,null=True)

    def __str__(self):
        return self.name
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    def __str__(self):
        return f"Cart: {self.user.username}"
class CartItem(models.Model): 
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product= models.ForeignKey(
        Product,
        on_delete=models.CASCADE        
    )
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    @property
    def total_price(self):
        return self.product.price*self.quantity
    
class Order(models.Model):
    STATUS_CHOICES=[
        ("new","нове"),
        ("cooking","готується"),
        ("delivering","доставляється"),
        ("done","виконано"),
        ("cancelled","скасовано")
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="new")
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Замовлення №{self.id}  ({self.user.username})"
    @property
    def total_price(self):
        return sum(
            item.total_price for item in self.items.all()
        )
class OrderItem(models.Model):
    order=models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product=models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    product_name=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField()
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    @property
    def total_price(self):
        return self.price * self.quantity

    