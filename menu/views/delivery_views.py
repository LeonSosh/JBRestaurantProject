from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from menu.models import Delivery, Item


# ManagerRequiredMixin is a mixin to ensure that only users in the 'manager' group can access the views it's included in.
class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="manager").exists()


# ManageDeliveriesView displays a list of all deliveries for managers to manage.
class ManageDeliveriesView(ManagerRequiredMixin, ListView):
    model = Delivery
    template_name = "manage_deliveries.html"
    context_object_name = "deliveries"

    # Orders the queryset by delivery primary key in descending order.
    def get_queryset(self):
        return Delivery.objects.order_by("-pk")


# MarkAsDeliveredView allows marking a delivery as delivered, updating the Delivery instance.
class MarkAsDeliveredView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        delivery_id = self.kwargs["delivery_id"]
        delivery = get_object_or_404(Delivery, pk=delivery_id)
        delivery.is_delivered = True
        delivery.save()
        return redirect("manage_deliveries")


# ViewOrderHistoryView displays a list of deliveries associated with the logged-in user's order history.
class ViewOrderHistoryView(LoginRequiredMixin, ListView):
    model = Delivery
    template_name = "order_history.html"
    context_object_name = "orders"

    # Filters the queryset by the logged-in user in descending order of creation.
    def get_queryset(self):
        return Delivery.objects.filter(cart__user=self.request.user).order_by("-created")

    # Augments context data with subtotal, total, and items for each order.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = context["orders"]
        for order in orders:
            items = Item.objects.filter(cart=order.cart)
            order.subtotal = sum(Decimal(item.dish.price) * item.amount for item in items)
            order.total = order.subtotal + order.delivery_fee
            order.cart.items = items
        return context
