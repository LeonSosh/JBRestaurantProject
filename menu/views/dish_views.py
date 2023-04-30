from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from menu.models import Dish, Category, Item
from menu.forms import DishForm


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class ManageDishesView(ManagerRequiredMixin, ListView):
    model = Dish
    template_name = 'manage_dishes.html'
    context_object_name = 'dishes'


class CreateDishView(ManagerRequiredMixin, View):
    def get(self, request):
        form = DishForm()
        return render(request, 'create_dish.html', {'form': form})

    def post(self, request):
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_dishes')
        return render(request, 'create_dish.html', {'form': form})


class EditDishView(ManagerRequiredMixin, View):
    def get(self, request, dish_id):
        dish = get_object_or_404(Dish, pk=dish_id)
        form = DishForm(instance=dish)
        return render(request, 'edit_dish.html', {'form': form, 'dish': dish})

    def post(self, request, dish_id):
        dish = get_object_or_404(Dish, pk=dish_id)
        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()
            return redirect('manage_dishes')
        return render(request, 'edit_dish.html', {'form': form, 'dish': dish})


class DeleteDishView(ManagerRequiredMixin, View):
    def get(self, request, dish_id):
        dish = get_object_or_404(Dish, pk=dish_id)
        for item in Item.objects.filter(dish=dish):
            item.dish = None
            item.save()

        dish.delete()
        return redirect('manage_dishes')


class DisplayDishesView(ListView):
    model = Dish
    template_name = 'dishes.html'
    context_object_name = 'dishes'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Dish.objects.filter(category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context
