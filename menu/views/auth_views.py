# Imports required Django modules and forms needed for user registration, login, and details update
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from menu.forms import RegistrationForm, UserLoginForm, UserUpdateForm


# RegisterView handles user registration via GET and POST requests
class RegisterView(View):
    def get(self, request):
        # Redirects authenticated user to the landing page
        if request.user.is_authenticated:
            return redirect("landing_page")
        form = RegistrationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        # Redirects authenticated user to the landing page
        if request.user.is_authenticated:
            return redirect("landing_page")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("landing_page")
        messages.error(request, "There was a problem with your registration.")
        print(form.errors)
        return render(request, "register.html", {"form": form})


# UserLoginView handles user login via GET and POST requests
class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "user_login.html", {"form": form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("landing_page")
            else:
                messages.error(request, "Invalid username or password.")
                return render(request, "user_login.html", {"form": form})


# UpdateDetailsView handles user details update via GET and POST requests; requires user to be logged in
class UpdateDetailsView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, "update_details.html", {"form": form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("landing_page")
        return render(request, "update_details.html", {"form": form})
