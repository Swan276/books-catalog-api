import stat
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .serializers import BookSerializer
from .handle_internal_error import log_internal_error, return_internal_error_response

class HealthView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "status": "ok",
                "running": True
            }, status=status.HTTP_200_OK
        )

health_view = HealthView.as_view()

class BookView(APIView):
  """Create, Retrieve Books"""
  
  def get(self, request, *args, **kwargs):
    """Get all books"""
    
    try:
      books = Book.objects.all()
      serializer = BookSerializer(books, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)  
    except Exception as e:
      log_internal_error(request, e)
      return return_internal_error_response()
  
  def post(self, request, *args, **kwargs):
    """Insert a book"""
    
    try:
      serializer = BookSerializer(data=request.data)
      if not serializer.is_valid():
        errorResponse = {
          "error": serializer.errors
        }
        return Response(errorResponse, status=status.HTTP_400_BAD_REQUEST)
      
      serializer.save()
      
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
      log_internal_error(request, e)
      return return_internal_error_response()
  
book_view = BookView.as_view()

class BookDetailView(APIView):
  """Retrieve, Update, Delete a Book"""
  
  def get_book(self, id):
    try:
      return Book.objects.get(id=id)
    except Book.DoesNotExist:
      raise Http404
  
  def get(self, request, id, *args, **kwargs):
    try:
      book = self.get_book(id)
      serializer = BookSerializer(book)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Http404:
      return Response({
        "error": "Book not found"
      }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
      log_internal_error(request, e)
      return return_internal_error_response()
  
  def put(self, request, id, *args, **kwargs):
    try:
      book = self.get_book(id)
      serializer = BookSerializer(book, data=request.data)
      
      if not serializer.is_valid():
        errorResponse = {
          "error": serializer.errors
        }
        return Response(errorResponse, status=status.HTTP_400_BAD_REQUEST)
      
      serializer.save()
      
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Http404:
      return Response({
        "error": "Book not found"
      }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
      log_internal_error(request, e)
      return return_internal_error_response()
  
  def patch(self, request, id, *args, **kwargs):
    try:
      book = self.get_book(id)
      serializer = BookSerializer(book, data=request.data, partial=True)
      
      if not serializer.is_valid():
        errorResponse = {
          "error": serializer.errors
        }
        return Response(errorResponse, status=status.HTTP_400_BAD_REQUEST)
      
      serializer.save()
      
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Http404:
      return Response({
        "error": "Book not found"
      }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
      log_internal_error(request, e)
      return return_internal_error_response()

  def delete(self, request, id, *args, **kwargs):
    try:
      book = self.get_book(id)
      book.delete()
      return Response(
        {
          "id": id,
        },
        status=status.HTTP_200_OK
      )
    except Http404:
      return Response({
        "error": "Book not found"
      }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
      log_internal_error(request, e)
      return return_internal_error_response()
  
book_detail_view = BookDetailView.as_view()