from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .models import CustomUser
from .forms import LoginForm, RegistrationForm


# Create your views here.
def register_view(request):
    user = request.user
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {"form": form,
                                                 "user": user})


def login_view(request):
    user = request.user
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            print(f"{email} {password}")
            user = authenticate(request, username=email, password=password)
            login(request, user)
            return redirect("home")
    else:
        form = LoginForm()
    return render(request, 'login.html',  {"form": form,
                                           "user": user})


def home_view(request):
    user = request.user
    return render(request, 'home.html', {"user": user})


