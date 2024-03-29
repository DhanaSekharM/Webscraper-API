from django.db import models


# Create your models here.
class ProductDetails(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_url = models.TextField()
    product_price = models.CharField(max_length=255)
    all_time_low = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255, null=True, default=None)
