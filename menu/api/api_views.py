from rest_framework import generics
from menu.models import Category, Dish
from .serializers import CategorySerializer, DishSerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DishList(generics.ListAPIView):
    serializer_class = DishSerializer

    def get_queryset(self):
        category = self.request.query_params.get("category_id", None)
        if category is not None:
            return Dish.objects.filter(category_id=category)
        return Dish.objects.all()
