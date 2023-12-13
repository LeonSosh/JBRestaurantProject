from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Define a Category model which inherits from the models.Model class
class Category(models.Model):
    # Define the name and image fields with their respective field types
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to="categories/")

    # Custom string representation for the Category model
    def __str__(self):
        return self.name


# Define a Dish model which inherits from the models.Model class
class Dish(models.Model):
    # Define the name, price, description, image, gluten-free, vegetarian, and category fields with their respective field types
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="dishes/")
    is_gluten_free = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # Custom string representation for the Dish model
    def __str__(self):
        return self.name


# Define a Cart model which inherits from the models.Model class
class Cart(models.Model):
    # Define the user and is_active fields with their respective field types
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    # Custom string representation for the Cart model
    def __str__(self):
        return f"Cart {self.pk} for {self.user}"


# Define an Item model which inherits from the models.Model class
class Item(models.Model):
    # Define the dish, cart, amount, dish_name, and dish_price fields with their respective field types
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount = models.IntegerField()
    dish_name = models.CharField(max_length=64, default="Unnamed Dish")
    dish_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Custom string representation for the Item model
    def __str__(self):
        return f"{self.amount} x {self.dish_name}"


# Define a Delivery model which inherits from the models.Model class
class Delivery(models.Model):
    # Define the is_delivered, address, comment, created, cart, delivery_time, and delivery_fee fields with their respective field types
    is_delivered = models.BooleanField(default=False)
    address = models.CharField(max_length=64)
    comment = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name="delivery")
    delivery_time = models.DateTimeField(default=timezone.now)
    delivery_fee = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)

    # Custom string representation for the Delivery model
    def __str__(self):
        return f"Delivery {self.pk} for {self.cart.user}"
