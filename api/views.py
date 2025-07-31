from email import errors
import stat
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render

from .models import Book
from .serializers import BookSerializer

class BookView(APIView):
  """CRUD Books"""
  
  def get(self, request, *args, **kwargs):
    """Get all books"""
    
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    """Insert a book"""
    
    serializer = BookSerializer(data=request.data)
    if not serializer.is_valid():
      print("Not Valid")
      errorResponse = {
        "errors": serializer.errors
      }
      print(errorResponse)
      return Response(errorResponse, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
book_view = BookView.as_view()