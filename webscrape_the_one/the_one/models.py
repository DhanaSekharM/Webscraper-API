from django.db import models


# Create your models here.
class ProductDetails(models.Model):
    product_name = models.CharField(max_length=255)
    product_url = models.TextField()
    product_price = models.CharField(max_length=255)
    all_time_low = models.CharField(max_length=255)