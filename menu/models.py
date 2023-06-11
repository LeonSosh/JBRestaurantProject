from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='dishes/')
    is_gluten_free = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart {self.pk} for {self.user}"


class Item(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount = models.IntegerField()
    dish_name = models.CharField(max_length=64, default="Unnamed Dish")
    dish_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.amount} x {self.dish_name}"


class Delivery(models.Model):
    is_delivered = models.BooleanField(default=False)
    address = models.CharField(max_length=64)
    comment = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='delivery')
    delivery_time = models.DateTimeField(default=timezone.now)
    delivery_fee = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)

    def __str__(self):
        return f"Delivery {self.pk} for {self.cart.user}"
