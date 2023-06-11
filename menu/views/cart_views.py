from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, View

from menu.forms import PlaceOrderForm
from menu.models import Cart, Delivery, Dish, Item


class CartView(LoginRequiredMixin, ListView):
    template_name = 'cart.html'
    context_object_name = 'items'

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        return Item.objects.filter(cart=cart)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_amount'] = sum(item.dish.price * item.amount for item in context['items'])
        return context


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, dish_id):
        dish = Dish.objects.get(pk=dish_id)
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        item, created = Item.objects.get_or_create(dish=dish, cart=cart, defaults={
                                                   'amount': 1, 'dish_name': dish.name, 'dish_price': dish.price})
        if not created:
            item.amount += 1
            item.save()
        return redirect('dishes', category_id=dish.category_id)


class IncrementCartItemView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        item = Item.objects.get(pk=item_id)
        item.amount += 1
        item.save()
        return redirect('cart')


class DecrementCartItemView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        item = Item.objects.get(pk=item_id)
        item.amount -= 1
        if item.amount <= 0:
            item.delete()
        else:
            item.save()
        return redirect('cart')


class RemoveCartItemView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        item = Item.objects.get(pk=item_id)
        item.delete()
        return redirect('cart')


class PlaceOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'place_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PlaceOrderForm()
        try:
            cart = Cart.objects.get(user=self.request.user, is_active=True)
            items = Item.objects.filter(cart=cart)
            total_amount = sum(item.dish.price * item.amount for item in items)
        except Cart.DoesNotExist:
            cart = None
            items = None
            total_amount = 0
        delivery_fee = Decimal(5.00)
        correct_total_amount = total_amount + delivery_fee
        context.update({
            'items': items,
            'total_amount': total_amount,
            'delivery_fee': delivery_fee,
            'correct_total_amount': correct_total_amount,
        })
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'confirm_order':
            return self.handle_confirm_order(request)
        elif action == 'cancel_order':
            return self.handle_cancel_order(request)
        else:
            return redirect('landing_page')

    def handle_confirm_order(self, request):
        form = PlaceOrderForm(request.POST)
        if form.is_valid():
            cart = Cart.objects.get(user=request.user, is_active=True)
            if Item.objects.filter(cart=cart).count() == 0:
                messages.warning(
                    request, 'Your cart is empty. Please add some dishes before placing an order.')
                return redirect('categories')
            delivery = Delivery.objects.create(
                cart=cart,
                address=form.cleaned_data['address'],
                comment=form.cleaned_data['comment'],
            )
            cart.is_active = False
            cart.save()
            Cart.objects.create(user=request.user, is_active=True)
            messages.success(request, 'Order placed successfully.')
            return redirect('order_confirmed', delivery_id=delivery.pk)
        return self.render_to_response(self.get_context_data(form=form))

    def handle_cancel_order(self, request):
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart.item_set.all().delete()
        messages.info(request, 'Order canceled and cart emptied.')
        return redirect('landing_page')


class OrderconfirmedView(LoginRequiredMixin, TemplateView):
    template_name = 'order_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delivery_id = self.kwargs['delivery_id']
        delivery = get_object_or_404(Delivery, pk=delivery_id)
        if delivery.cart.user != self.request.user:
            return redirect('landing_page')
        items = Item.objects.filter(cart=delivery.cart)
        total_amount = sum(item.dish.price * item.amount for item in items)
        correct_total_amount = total_amount + delivery.delivery_fee
        context.update({
            'delivery': delivery,
            'items': items,
            'total_amount': total_amount,
            'delivery_fee': delivery.delivery_fee,
            'correct_total_amount': correct_total_amount,
        })
        return context
