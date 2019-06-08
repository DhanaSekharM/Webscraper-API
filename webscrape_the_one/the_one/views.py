from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from .main import main


class Requests(APIView):

    def get(self, request):
        return Response({"hello": str(request)})

    def post(self, request):
        jsonBody = json.loads(request.body)
        product = jsonBody['product']
        names, price, rating = main(product=product)

        # names = product_details[0]
        # price = product_details[1]
        # rating = product_details[2]

        data = {'product_name': names[0], 'price': price[0], 'rating': rating[0]}

        jsonResponse = json.dumps(data)

        if True:
            return JsonResponse(data, safe=False)

        # return Response({'first': names[0]})
