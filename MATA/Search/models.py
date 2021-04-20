from django.db import models

# Create your models here.
class item(models.Model) :
    asin = models.CharField(max_length=100,default="")
    reviewText=models.TextField(max_length=5000,default="")
    description = models.TextField(max_length=500, default="")
    title = models.TextField(max_length=500, default="")
    image = models.TextField(max_length=500, default="")

