from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from menu.models import Delivery, Item


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class ManageDeliveriesView(ManagerRequiredMixin, ListView):
    model = Delivery
    template_name = 'manage_deliveries.html'
    context_object_name = 'deliveries'

    def get_queryset(self):
        return Delivery.objects.order_by('-pk')


class MarkAsDeliveredView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        delivery_id = self.kwargs['delivery_id']
        delivery = get_object_or_404(Delivery, pk=delivery_id)
        delivery.is_delivered = True
        delivery.save()
        return redirect('manage_deliveries')


class ViewOrderHistoryView(LoginRequiredMixin, ListView):
    model = Delivery
    template_name = 'order_history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Delivery.objects.filter(cart__user=self.request.user).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = context['orders']
        for order in orders:
            items = Item.objects.filter(cart=order.cart)
            order.subtotal = sum(Decimal(item.dish.price) * item.amount for item in items)
            order.total = order.subtotal + order.delivery_fee
            order.cart.items = items
        return context
