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
from .Notifications import send_notifications
from re import findall


class Requests(APIView):

    def get(self, request):
        products1 = ProductDetails.objects.get(id=11)
        products = []
        products.append(products1)
        updated_products = []
        for product in list(products):
            updated_product = ProductDetails.objects.get(id=product.id)
            names, prices, rating = main(product=updated_product.product_url)
            if prices[0] != updated_product.product_price:
                updated_product.product_price = prices[0]
            if float(prices[0]) <= float(updated_product.all_time_low):
                updated_product.all_time_low = prices[0]
            updated_product.save()
            updated_products.append(updated_product)
        # print(updated_products[5].product_name)
        data = ProductDetailsSerializer(updated_products, many=True)

        send_notifications()

        return JsonResponse(data.data, safe=False)

    def post(self, request):
        jsonBody = json.loads(request.body)
        product = jsonBody['product']
        url = findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]| [! * \(\),] | (?: %[0-9a-fA-F][0-9a-fA-F]))+', product)
        product_url = url[0]
        names, price, rating = main(product=product_url)

        # names = product_details[0]
        # price = product_details[1]
        # rating = product_details[2]

        data = {'product_name': names[0], 'price': price[0], 'rating': rating[0]}

        new_product = ProductDetails(product_name=data['product_name'], product_url=product_url,
                                     product_price=data['price']
                                     , all_time_low=data['price'])

        # new_product.save()
        print(product_url)
        data = ProductDetailsSerializer(new_product, many=False)

        return JsonResponse(data.data, safe=False)
