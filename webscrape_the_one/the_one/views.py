from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from django.core import serializers

from .models import ProductDetails
from .main import main
from .serializers import ProductDetailsSerializer


class Requests(APIView):

    def get(self, request):
        products = ProductDetails.objects.all()
        updated_products = []
        for product in products:
            updated_product = ProductDetails.objects.get(id=product.id)
            names, prices, rating = main(product=updated_product.product_url)
            if prices[0] != updated_product.product_price:
                updated_product.product_price = prices[0]
            if float(prices[0]) <= float(updated_product.all_time_low):
                updated_product.all_time_low = prices[0]
            updated_product.save()
            updated_products.append(updated_product)
        print(updated_products[5].product_name)
        data = ProductDetailsSerializer(updated_products, many=True)
        return JsonResponse(data.data, safe=False)

    def post(self, request):
        jsonBody = json.loads(request.body)
        product = jsonBody['product']
        names, price, rating = main(product=product)

        # names = product_details[0]
        # price = product_details[1]
        # rating = product_details[2]

        data = {'product_name': names[0], 'price': price[0], 'rating': rating[0]}

        new_product = ProductDetails(product_name=data['product_name'], product_url=product, product_price=data['price']
                                     , all_time_low=data['price'])

        new_product.save()
        data = ProductDetailsSerializer(new_product, many=False)

        return JsonResponse(data.data, safe=False)
