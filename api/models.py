from django.db import models

class Book(models.Model):
  isbn = models.CharField(max_length=17, primary_key=True) # isbn has 13 digits and 4 hyphens
  title = models.CharField(max_length=255)
  description = models.TextField(default="")
  author = models.CharField(max_length=255)
  publishedDate = models.DateField() # no validation for future date as there can be pre-orders