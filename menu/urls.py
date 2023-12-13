from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordChangeView
from django.urls import include, path

from menu.views import auth_views, cart_views, category_views, delivery_views, dish_views

urlpatterns = [
    path("api/", include("menu.api.urls")),
    path("", category_views.landing_pageView.as_view(), name="landing_page"),
    path("user_login/", auth_views.UserLoginView.as_view(), name="user_login"),
    path("logout/", LogoutView.as_view(next_page="landing_page"), name="logout"),
    path("register/", auth_views.RegisterView.as_view(), name="register"),
    path("update_details/", auth_views.UpdateDetailsView.as_view(), name="update_details"),
    path(
        "password_change/",
        PasswordChangeView.as_view(template_name="password_change.html"),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(template_name="password_change_done.html"),
        name="password_change_done",
    ),
    path(
        "management_panel/", category_views.ManagementPanelView.as_view(), name="management_panel"
    ),
    path("create_category/", category_views.CreateCategoryView.as_view(), name="create_category"),
    path(
        "edit_category/<int:category_id>/",
        category_views.EditCategoryView.as_view(),
        name="edit_category",
    ),
    path(
        "delete_category/<int:category_id>/",
        category_views.DeleteCategoryView.as_view(),
        name="delete_category",
    ),
    path("categories/", category_views.DisplayCategoriesView.as_view(), name="categories"),
    path("dishes/<int:category_id>/", dish_views.DisplayDishesView.as_view(), name="dishes"),
    path("manage_dishes/", dish_views.ManageDishesView.as_view(), name="manage_dishes"),
    path("create_dish/", dish_views.CreateDishView.as_view(), name="create_dish"),
    path("edit_dish/<int:dish_id>/", dish_views.EditDishView.as_view(), name="edit_dish"),
    path("delete_dish/<int:dish_id>/", dish_views.DeleteDishView.as_view(), name="delete_dish"),
    path("add_to_cart/<int:dish_id>/", cart_views.AddToCartView.as_view(), name="add_to_cart"),
    path("cart/", cart_views.CartView.as_view(), name="cart"),
    path("place_order/", cart_views.PlaceOrderView.as_view(), name="place_order"),
    path(
        "order_confirmed/<int:delivery_id>/",
        cart_views.OrderconfirmedView.as_view(),
        name="order_confirmed",
    ),
    path(
        "cart/increment/<int:item_id>/",
        cart_views.IncrementCartItemView.as_view(),
        name="increment_cart_item",
    ),
    path(
        "cart/decrement/<int:item_id>/",
        cart_views.DecrementCartItemView.as_view(),
        name="decrement_cart_item",
    ),
    path(
        "cart/remove/<int:item_id>/",
        cart_views.RemoveCartItemView.as_view(),
        name="remove_cart_item",
    ),
    path("order_history/", delivery_views.ViewOrderHistoryView.as_view(), name="order_history"),
    path(
        "manage_deliveries/",
        delivery_views.ManageDeliveriesView.as_view(),
        name="manage_deliveries",
    ),
    path(
        "mark_as_delivered/<int:delivery_id>/",
        delivery_views.MarkAsDeliveredView.as_view(),
        name="mark_as_delivered",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
