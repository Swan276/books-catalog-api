from datetime import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Book

class HealthViewTest(APITestCase):
  def test_get(self):
    url = reverse('api:health')
    response = self.client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["status"] == "ok"

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
    assert returned_book["isbn"] == book.isbn
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
    assert returned_book["isbn"] == book["isbn"]
    assert returned_book["title"] == book["title"]
    assert returned_book["description"] == ""
    assert returned_book["author"] == book["author"]
    assert returned_book["published_date"] == book["published_date"]
    assert returned_book["created_at"]
    assert returned_book["updated_at"]
    
class BookDetailViewTest(APITestCase):
  def test_get_book_by_id(self):
    book = Book.objects.create(
      isbn="11-111-111-111-11",
      title="Test Book",
      author="Test Author",
      published_date="2025-07-31"
    )
    
    url = reverse('api:books')
    response = self.client.get(url + f"{book.id}/", format='json')
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["isbn"] == book.isbn
    assert body["title"] == book.title
    assert body["description"] == book.description
    assert body["author"] == book.author
    assert body["published_date"] == book.published_date
    
  def test_put_book_by_id(self):
    book = Book.objects.create(
      isbn="11-111-111-111-11",
      title="Test Book",
      author="Test Author",
      published_date="2025-07-31"
    )
    
    updated_book = {
      "isbn": "11-111-111-111-11",
      "title": "Updated Book",
      "description": "Updated Description",
      "author": "Updated Author",
      "published_date": "2025-08-31"
    }
    
    url = reverse('api:books')
    response = self.client.put(url + f"{book.id}/", data=updated_book, headers={ "Content-Type": "application/json" }, format='json')
    assert response.status_code == status.HTTP_200_OK
    returned_book = response.json()
    assert returned_book["title"] == updated_book["title"]
    assert returned_book["description"] == updated_book["description"]
    assert returned_book["author"] == updated_book["author"]
    assert returned_book["published_date"] == updated_book["published_date"]
    assert datetime.fromisoformat(returned_book["created_at"]) == book.created_at
    assert datetime.fromisoformat(returned_book["updated_at"]) != book.updated_at
    
  def test_patch_book_by_id(self):
    book = Book.objects.create(
      isbn="11-111-111-111-11",
      title="Test Book",
      author="Test Author",
      published_date="2025-07-31"
    )
    
    updated_book = {
      "description": "Updated Description"
    }
    
    url = reverse('api:books')
    response = self.client.patch(url + f"{book.id}/", data=updated_book, headers={ "Content-Type": "application/json" }, format='json')
    assert response.status_code == status.HTTP_200_OK
    returned_book = response.json()
    assert returned_book["title"] == book.title
    assert returned_book["description"] == updated_book["description"]
    assert returned_book["author"] == book.author
    assert returned_book["published_date"] == str(book.published_date)
    assert datetime.fromisoformat(returned_book["created_at"]) == book.created_at
    assert datetime.fromisoformat(returned_book["updated_at"]) != book.updated_at
    
  def test_delete_book_by_id(self):
    book = Book.objects.create(
      isbn="11-111-111-111-11",
      title="Test Book",
      author="Test Author",
      published_date="2025-07-31"
    )
    
    url = reverse('api:books')
    response = self.client.delete(url + f"{book.id}/", format='json')
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["id"] == str(book.id)
    assert book.DoesNotExist()