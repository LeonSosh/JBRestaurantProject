from django.urls import path

from .api_views import CategoryList, DishList

urlpatterns = [
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("dishes/", DishList.as_view(), name="dish-list"),
]
