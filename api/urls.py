from django.urls import re_path
from rest_framework.urls import app_name
from .views import book_view

app_name = "api"

urlpatterns = [
    re_path(r"^books/", book_view, name="books")
]