from rest_framework import serializers
from menu.models import Category, Dish


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "image"]


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = [
            "id",
            "name",
            "price",
            "description",
            "image",
            "is_gluten_free",
            "is_vegetarian",
            "category",
        ]
