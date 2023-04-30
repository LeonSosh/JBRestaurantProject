from django.contrib import admin
from .models import Category, Dish, Cart, Item, Delivery

admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Cart)
admin.site.register(Item)
admin.site.register(Delivery)
