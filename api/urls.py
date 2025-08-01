from django.urls import path, re_path
from .views import book_view, book_detail_view, health_view

app_name = "api"

urlpatterns = [
    path("", health_view, name="health"),
    re_path(r"^books/$", book_view, name="books"),
    re_path(r"^books/(?P<id>[0-9]+)/$", book_detail_view, name="book_detail"),
]