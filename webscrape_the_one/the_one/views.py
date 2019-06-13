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

from .parallel_fetch import concurrent_map, call_main


class Requests(APIView):

    def get(self, request):
        products = ProductDetails.objects.all()
        products_list = []
        product_urls = []

        for product in list(products):
            updated_product = ProductDetails.objects.get(id=product.id)
            products_list.append(updated_product)
            product_urls.append(updated_product.product_url)

        return_values = concurrent_map(call_main, product_urls)
        names, prices, rating, image_urls = [], [], [], []
        for i in range(len(return_values)):
            prices.append(return_values[i][1][0])

        print(prices[0])

        for i in range(len(products_list)):
            if prices[i] != products_list[i].product_price:
                products_list[i].product_price = prices[i]
            if float(prices[i]) <= float(products_list[i].all_time_low):
                products_list[i].all_time_low = prices[i]
            products_list[i].save()
        # print(updated_products[5].product_name)
        data = ProductDetailsSerializer(products_list, many=True)

        # send_notifications()

        return JsonResponse(data.data, safe=False)

    def post(self, request):
        jsonBody = json.loads(request.body)
        product = jsonBody['product']
        url = findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]| [! * \(\),] | (?: %[0-9a-fA-F][0-9a-fA-F]))+', product)
        product_url = url[0]
        names, price, rating, image_urls = main(product=product_url)

        # names = product_details[0]
        # price = product_details[1]
        # rating = product_details[2]

        new_product = ProductDetails(product_name=names[0], product_url=product_url,
                                     product_price=price[0],
                                     all_time_low=price[0],
                                     image_url=image_urls[0])

        new_product.save()
        print(product_url)
        data = ProductDetailsSerializer(new_product, many=False)

        return JsonResponse(data.data, safe=False)
