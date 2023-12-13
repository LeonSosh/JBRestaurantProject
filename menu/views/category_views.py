from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, TemplateView

from menu.forms import CategoryForm
from menu.models import Category
from menu.views.delivery_views import ManagerRequiredMixin


# Landing page view for a template-based website.
class landing_pageView(TemplateView):
    # The template to be rendered is 'landing_page.html'.
    template_name = "landing_page.html"

    # Get context data to be displayed on the website.
    def get_context_data(self, **kwargs):
        # Get context from the base class.
        context = super().get_context_data(**kwargs)
        # Populate context with all available categories.
        context["categories"] = Category.objects.all()
        # Return the context with categories added.
        return context


# Management panel view which requires the user to be a manager.
class ManagementPanelView(ManagerRequiredMixin, View):
    # Handle the GET request.
    def get(self, request):
        # Fetch all categories from the Category model.
        categories = Category.objects.all()
        # Render the management panel template with the available categories.
        return render(request, "management_panel.html", {"categories": categories})


# Display categories view which inherits from Django's ListView.
class DisplayCategoriesView(ListView):
    # Specify the model to be used for fetching categories.
    model = Category
    # Specify the template to be rendered.
    template_name = "categories.html"
    # Define context object name for categories to be used in the template.
    context_object_name = "categories"


# This is a Django view class for creating a new category
class CreateCategoryView(View):
    # This method handles GET requests and displays an empty CategoryForm
    def get(self, request):
        form = CategoryForm()
        return render(request, "create_category.html", {"form": form})

    # This method handles POST requests and saves a new category if the form is valid
    def post(self, request):
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("management_panel")
        return render(request, "create_category.html", {"form": form})


# This is a Django view class for editing an existing category
class EditCategoryView(View):
    # This method handles GET requests and displays a CategoryForm with the existing category data
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(instance=category)
        return render(request, "edit_category.html", {"form": form, "category": category})

    # This method handles POST requests and updates the category if the form is valid
    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect("management_panel")
        return render(request, "edit_category.html", {"form": form, "category": category})


# This is a Django view class for deleting an existing category
class DeleteCategoryView(View):
    # This method handles GET requests and deletes the specified category
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return redirect("management_panel")
