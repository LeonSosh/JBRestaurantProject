from rest_framework import generics

from menu.models import Category, Dish

from .serializers import CategorySerializer, DishSerializer


# CategoryList view class
class CategoryList(generics.ListAPIView):
    # Retrieve all Category objects from the database
    queryset = Category.objects.all()
    # Specify the serializer to use for Category objects
    serializer_class = CategorySerializer


# DishList view class
class DishList(generics.ListAPIView):
    # Specify the serializer to use for Dish objects
    serializer_class = DishSerializer

    # Override get_queryset method to customize retrieval of Dish objects
    def get_queryset(self):
        # Obtain the 'category_id' parameter from the request's query parameters
        category = self.request.query_params.get("category_id", None)
        # If 'category_id' is specified, return Dish objects related to that category
        if category is not None:
            return Dish.objects.filter(category_id=category)
        # If 'category_id' is not specified, return all Dish objects
        return Dish.objects.all()
