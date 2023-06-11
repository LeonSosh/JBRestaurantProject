from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, TemplateView

from menu.forms import CategoryForm
from menu.models import Category
from menu.views.delivery_views import ManagerRequiredMixin


class landing_pageView(TemplateView):
    template_name = 'landing_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ManagementPanelView(ManagerRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'management_panel.html', {'categories': categories})


class DisplayCategoriesView(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'


class CreateCategoryView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'create_category.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('management_panel')
        return render(request, 'create_category.html', {'form': form})


class EditCategoryView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(instance=category)
        return render(request, 'edit_category.html', {'form': form, 'category': category})

    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('management_panel')
        return render(request, 'edit_category.html', {'form': form, 'category': category})


class DeleteCategoryView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return redirect('management_panel')
