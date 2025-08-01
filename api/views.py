from email import errors
import stat
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render

from .models import Book
from .serializers import BookSerializer

class HealthView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "status": "ok",
                "running": True
            }
        )

health_view = HealthView.as_view()

class BookView(APIView):
  """Create, Retrieve Books"""
  
  def get(self, request, *args, **kwargs):
    """Get all books""" 
    
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    """Insert a book"""
    
    serializer = BookSerializer(data=request.data)
    if not serializer.is_valid():
      errorResponse = {
        "errors": serializer.errors
      }
      return Response(errorResponse, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
book_view = BookView.as_view()

class BookDetailView(APIView):
  """Retrieve, Update, Delete a Book"""
  
  def get_book(self, id):
    try:
      return Book.objects.get(id=id)
    except Book.DoesNotExist:
      raise Http404
  
  def get(self, request, id, *args, **kwargs):
    book = self.get_book(id)
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def put(self, request, id, *args, **kwargs):
    book = self.get_book(id)
    serializer = BookSerializer(book, data=request.data)
    
    if not serializer.is_valid():
      errorResponse = {
        "errors": serializer.errors
      }
      return Response(errorResponse, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def patch(self, request, id, *args, **kwargs):
    book = self.get_book(id)
    serializer = BookSerializer(book, data=request.data, partial=True)
    
    if not serializer.is_valid():
      errorResponse = {
        "errors": serializer.errors
      }
      return Response(errorResponse, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    
    return Response(serializer.data, status=status.HTTP_200_OK)

  def delete(self, request, id, *args, **kwargs):
    book = self.get_book(id)
    book.delete()
    return Response(
      {
        "id": id,
      },
      status=status.HTTP_200_OK
    )
  
book_detail_view = BookDetailView.as_view()