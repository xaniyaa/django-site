from django.urls.conf import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    ]