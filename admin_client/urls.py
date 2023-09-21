from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name='registration'),
    path("", views.home_view, name="home"),
    path('logout/', LogoutView.as_view(), name='logout'),
]