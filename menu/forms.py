from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Dish


# CategoryForm is a class based on ModelForm for creating a form based on the Category model
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "image"]


# DishForm is a class based on ModelForm for creating a form based on the Dish model
class DishForm(forms.ModelForm):
    class Meta:
        def __init__(self, *args, **kwargs):
            super(DishForm, self).__init__(*args, **kwargs)
            # Update the image field's widget attributes with a class "file-input"
            self.fields["image"].widget.attrs.update({"class": "file-input"})

        model = Dish
        fields = [
            "name",
            "price",
            "description",
            "image",
            "is_gluten_free",
            "is_vegetarian",
            "category",
        ]


# PlaceOrderForm is a class based on Form for creating a form to place an order
class PlaceOrderForm(forms.Form):
    address = forms.CharField(
        max_length=64, widget=forms.TextInput(attrs={"placeholder": "Delivery Address"})
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Notes"}), required=False
    )


# RegistrationForm is a class extending UserCreationForm for creating a user registration form
class RegistrationForm(UserCreationForm):
    # Add an email field with a help text
    email = forms.EmailField(max_length=64, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "first_name", "last_name")


# UserLoginForm is a class based on Form for creating a user login form
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# UserUpdateForm is a class based on ModelForm for creating a form to update the User model
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
