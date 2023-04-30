from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, Dish


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']


class DishForm(forms.ModelForm):
    class Meta:
        def __init__(self, *args, **kwargs):
            super(DishForm, self).__init__(*args, **kwargs)
            self.fields['image'].widget.attrs.update({'class': 'file-input'})
        model = Dish
        fields = ['name', 'price', 'description', 'image',
                  'is_gluten_free', 'is_vegetarian', 'category']


class PlaceOrderForm(forms.Form):
    address = forms.CharField(max_length=64, widget=forms.TextInput(
        attrs={'placeholder': 'Delivery Address'}))
    comment = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Notes'}), required=False)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=64, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1',
                  'password2', 'first_name', 'last_name')


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
