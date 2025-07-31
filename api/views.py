from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render

class BookView(APIView):
  """CRUD Books"""
  
  def get(self, request, *args, **kwargs):
    return Response({
      "status": "ok"
    })

book_view = BookView.as_view()