from django.urls import path, re_path
from .views import book_view, health_view

app_name = "api"

urlpatterns = [
    path("", health_view, name="health"),
    re_path(r"^books/", book_view, name="books")
]