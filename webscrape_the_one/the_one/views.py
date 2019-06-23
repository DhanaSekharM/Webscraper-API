import time

from django.http import JsonResponse

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.views import status

from .models import ProductDetails
from .main import main
from .serializers import ProductDetailsSerializer
from re import findall

from .parallel_fetch import concurrent_map, call_main
from .multiprocess_fetch import parallel_map, call_main as call

class Requests(APIView):

    def get(self, request):
        products = ProductDetails.objects.all()
        products_list = []
        product_urls = []
        # send_notifications(title='Title', message='Message')
        # scrape_periodically.delay()
        for product in list(products):
            updated_product = ProductDetails.objects.get(product_id=product.product_id)
            products_list.append(updated_product)
            product_urls.append(updated_product.product_url)
        start_time = time.time()
        return_values = parallel_map(call, product_urls)
        endtime = time.time() - start_time
        names, prices, rating, image_urls = [], [], [], []
        # print(return_values)
        for i in range(len(return_values)):
            prices.append(return_values[i][1][0])

        print(prices[0])

        for i in range(len(products_list)):
            if prices[i] != products_list[i].product_price:
                products_list[i].product_price = prices[i]
            if float(prices[i]) <= float(products_list[i].all_time_low):
                products_list[i].all_time_low = prices[i]
            products_list[i].save()
        data = ProductDetailsSerializer(products_list, many=True)

        return JsonResponse(data.data, safe=False)

    def post(self, request):
        jsonBody = json.loads(request.body)
        product = jsonBody['product']
        url = findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]| [! * \(\),] | (?: %[0-9a-fA-F][0-9a-fA-F]))+', product)
        product_url = url[0]
        names, price, rating, image_urls = main(product=product_url)

        new_product = ProductDetails(product_name=names[0], product_url=product_url,
                                     product_price=price[0],
                                     all_time_low=price[0],
                                     image_url=image_urls[0])

        new_product.save()
        print(product_url)
        data = ProductDetailsSerializer(new_product, many=False)

        return JsonResponse(data.data, safe=False)


class ProductDeleteView(generics.RetrieveUpdateDestroyAPIView):

    def delete(self, request, *args, **kwargs):
        product = ProductDetails.objects.get(product_id=kwargs["pk"])
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
