# Import the required module from Django REST framework
from rest_framework import serializers

# Import the necessary models from the menu app
from menu.models import Category, Dish


# Create a CategorySerializer class inheriting from serializers.ModelSerializer
class CategorySerializer(serializers.ModelSerializer):
    # Define the metadata for the serializer
    class Meta:
        model = Category  # The model the serializer represents
        fields = ["id", "name", "image"]  # The fields to include in the serialized output


# Create a DishSerializer class inheriting from serializers.ModelSerializer
class DishSerializer(serializers.ModelSerializer):
    # Define the metadata for the serializer
    class Meta:
        model = Dish  # The model the serializer represents
        fields = [
            "id",
            "name",
            "price",
            "description",
            "image",
            "is_gluten_free",
            "is_vegetarian",
            "category",
        ]  # The fields to include in the serialized output
