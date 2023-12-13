from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, View

from menu.forms import PlaceOrderForm
from menu.models import Cart, Delivery, Dish, Item


# The CartView class is a subclass of LoginRequiredMixin and ListView classes.
# It requires the user to be logged in and displays a list of items.
class CartView(LoginRequiredMixin, ListView):
    # Specify the HTML template for the view.
    template_name = "cart.html"
    # Define the name of the context object used in the template.
    context_object_name = "items"

    # Get the queryset of items in the cart for the logged in user.
    def get_queryset(self):
        # Get or create an active cart for the user.
        cart, _ = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        # Return the items in the cart.
        return Item.objects.filter(cart=cart)

    # Provide additional context data to the template.
    def get_context_data(self, **kwargs):
        # Get base context data from the parent class.
        context = super().get_context_data(**kwargs)
        # Add the total_amount attribute to the context.
        context["total_amount"] = sum(item.dish.price * item.amount for item in context["items"])
        # Return the updated context.
        return context


# The AddToCartView class is a subclass of LoginRequiredMixin and View classes.
# It requires the user to be logged in and lets users add items to their cart.
class AddToCartView(LoginRequiredMixin, View):
    # Process a GET request.
    def get(self, request, dish_id):
        # Get the dish by its primary key.
        dish = Dish.objects.get(pk=dish_id)
        # Get or create an active cart for the user.
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        # Get or create an item with the specified dish and cart, and set some default values.
        item, created = Item.objects.get_or_create(
            dish=dish,
            cart=cart,
            defaults={"amount": 1, "dish_name": dish.name, "dish_price": dish.price},
        )
        # If the item already existed, increment the amount and save the item.
        if not created:
            item.amount += 1
            item.save()
        # Redirect to the dishes view with the specified category_id.
        return redirect("dishes", category_id=dish.category_id)


class IncrementCartItemView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        item = Item.objects.get(pk=item_id)
        item.amount += 1
        item.save()
        return redirect("cart")


class DecrementCartItemView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        item = Item.objects.get(pk=item_id)
        item.amount -= 1
        if item.amount <= 0:
            item.delete()
        else:
            item.save()
        return redirect("cart")


class RemoveCartItemView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        item = Item.objects.get(pk=item_id)
        item.delete()
        return redirect("cart")


# This class represents a view for placing an order.
class PlaceOrderView(LoginRequiredMixin, TemplateView):
    # The HTML template used for the view.
    template_name = "place_order.html"

    # This method retrieves context data for the view.
    def get_context_data(self, **kwargs):
        # Get the base context data.
        context = super().get_context_data(**kwargs)
        # Add a PlaceOrderForm instance to the context.
        context["form"] = PlaceOrderForm()
        # Attempt to get the active cart for the current user.
        try:
            cart = Cart.objects.get(user=self.request.user, is_active=True)
            # Get the items in the cart.
            items = Item.objects.filter(cart=cart)
            # Calculate the total amount for the items in the cart.
            total_amount = sum(item.dish.price * item.amount for item in items)
        # If there's no active cart, set cart, items, and total_amount to None/0.
        except Cart.DoesNotExist:
            cart = None
            items = None
            total_amount = 0
        # Set the delivery fee.
        delivery_fee = Decimal(5.00)
        # Calculate the correct total amount with delivery fee added.
        correct_total_amount = total_amount + delivery_fee
        # Update the context with the cart details.
        context.update(
            {
                "items": items,
                "total_amount": total_amount,
                "delivery_fee": delivery_fee,
                "correct_total_amount": correct_total_amount,
            }
        )
        return context

    # This method handles POST requests to the view.
    def post(self, request, *args, **kwargs):
        # Get the action from the POST data.
        action = request.POST.get("action")
        # If the action is to confirm the order, handle it accordingly.
        if action == "confirm_order":
            return self.handle_confirm_order(request)
        # If the action is to cancel the order, handle it accordingly.
        elif action == "cancel_order":
            return self.handle_cancel_order(request)
        # If no action is provided, redirect to the landing page.
        else:
            return redirect("landing_page")


# This method handles the process of confirming a user's order
def handle_confirm_order(self, request):
    # Create an instance of PlaceOrderForm with the POST data
    form = PlaceOrderForm(request.POST)
    # Check if the form data is valid
    if form.is_valid():
        # Get the user's active cart
        cart = Cart.objects.get(user=request.user, is_active=True)
        # Check if the cart is empty
        if Item.objects.filter(cart=cart).count() == 0:
            # Display a warning message and redirect to the categories page
            messages.warning(
                request, "Your cart is empty. Please add some dishes before placing an order."
            )
            return redirect("categories")
        # Create a delivery object associated with the user's cart
        delivery = Delivery.objects.create(
            cart=cart,
            address=form.cleaned_data["address"],
            comment=form.cleaned_data["comment"],
        )
        # Mark the cart as inactive and save its state
        cart.is_active = False
        cart.save()
        # Create a new active cart for the user
        Cart.objects.create(user=request.user, is_active=True)
        # Display a success message and redirect to the order confirmation page
        messages.success(request, "Order placed successfully.")
        return redirect("order_confirmed", delivery_id=delivery.pk)
    # Render the form again if the form data is not valid
    return self.render_to_response(self.get_context_data(form=form))


# This method handles the process of canceling a user's order and emptying the cart
def handle_cancel_order(self, request):
    # Get the user's active cart
    cart = Cart.objects.get(user=request.user, is_active=True)
    # Delete all items in the cart
    cart.item_set.all().delete()
    # Display an info message and redirect to the landing page
    messages.info(request, "Order canceled and cart emptied.")
    return redirect("landing_page")


# This class provides a view for order confirmation page.
# It inherits from LoginRequiredMixin and TemplateView.
class OrderConfirmedView(LoginRequiredMixin, TemplateView):
    # The HTML template to be rendered for this view
    template_name = "order_confirmed.html"

    # Method used to collect and return the context data
    # to be used when rendering the template.
    def get_context_data(self, **kwargs):
        # Call the parent class method to get the base context data
        context = super().get_context_data(**kwargs)

        # Get the delivery ID from the URL parameters
        delivery_id = self.kwargs["delivery_id"]

        # Fetch the delivery object or 404 if not found
        delivery = get_object_or_404(Delivery, pk=delivery_id)

        # Check if the user making the request is the same as the cart's user
        if delivery.cart.user != self.request.user:
            # If not, redirect to the landing page
            return redirect("landing_page")

        # Fetch all items related to the cart in the delivery
        items = Item.objects.filter(cart=delivery.cart)

        # Calculate the total amount for all items in the cart
        total_amount = sum(item.dish.price * item.amount for item in items)

        # Calculate the correct total amount including the delivery fee
        correct_total_amount = total_amount + delivery.delivery_fee

        # Update the context with additional data
        context.update(
            {
                "delivery": delivery,
                "items": items,
                "total_amount": total_amount,
                "delivery_fee": delivery.delivery_fee,
                "correct_total_amount": correct_total_amount,
            }
        )

        # Return the updated context
        return context
