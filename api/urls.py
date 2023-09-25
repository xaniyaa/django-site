from django.urls import include, path


urlpatterns = [
    path("files/", include(("files.urls", "files"))),
    ]