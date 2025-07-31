from django.db import models

class Book(models.Model):
  id = models.AutoField(primary_key=True)  
  isbn = models.CharField(max_length=17, unique=True) # isbn has 13 digits and 4 hyphens
  title = models.CharField(max_length=255)
  description = models.TextField(default="") # default to empty if not provided
  author = models.CharField(max_length=255)
  published_date = models.DateField() # no validation for future date as there can be pre-orders
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)