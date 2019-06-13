from rest_framework import serializers
from .models import ProductDetails


class ProductDetailsSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=255)
    product_url = serializers.CharField()
    product_price = serializers.CharField(max_length=255)
    all_time_low = serializers.CharField(max_length=255)
    image_url = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return ProductDetails.objects.create(**validated_data)
