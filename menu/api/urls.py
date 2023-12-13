# Import 'path' from Django's URL handling module
from django.urls import path

# Import views for handling API requests related to categories and dishes
from .api_views import CategoryList, DishList

# Define URL patterns for the API endpoints
urlpatterns = [
    # Route for the 'category-list' view: Lists all categories
    path("categories/", CategoryList.as_view(), name="category-list"),
    # Route for the 'dish-list' view: Lists all dishes
    path("dishes/", DishList.as_view(), name="dish-list"),
]
