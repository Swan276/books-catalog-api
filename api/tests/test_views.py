from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Book

class BookViewTest(APITestCase):
  def test_get_books(self):
    book = Book.objects.create(
      isbn="11-111-111-111-11",
      title="Test Book",
      author="Test Author",
      published_date="2025-07-31"
    )
    
    url = reverse('api:books')
    response = self.client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert isinstance(body, list)
    returned_book = body[0]
    assert returned_book["title"] == book.title
    assert returned_book["description"] == book.description
    assert returned_book["author"] == book.author
    assert returned_book["published_date"] == book.published_date
    
  def test_post_books(self):
    book = {
      "isbn": "11-111-111-111-11",
      "title": "Test Book",
      "author": "Test Author",
      "published_date": "2025-07-31"
    }
    
    url = reverse('api:books')
    response = self.client.post(url, data=book, headers={ "Content-Type": "application/json" }, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    returned_book = response.json()
    assert returned_book["title"] == book["title"]
    assert returned_book["description"] == ""
    assert returned_book["author"] == book["author"]
    assert returned_book["published_date"] == book["published_date"]
    assert returned_book["created_at"]
    assert returned_book["updated_at"]
    