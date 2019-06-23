from __future__ import absolute_import, unicode_literals

from celery import shared_task
# from webscrape_the_one.webscrape_the_one.celery import app
from .main import main
from .Notifications import send_notifications

from celery import task

from .models import ProductDetails
from .parallel_fetch import concurrent_map, call_main
from .serializers import ProductDetailsSerializer


@task()
def scrape_periodically(name='scrape_periodically'):
    print('here')
    products = list(ProductDetails.objects.all())
    product_urls = []
    names, prices, rating, image_urls = [], [], [], []
    for product in products:
        product_urls.append(product.product_url)

    return_values = concurrent_map(call_main, product_urls)
    # send_notifications(title='Title', message='Message')

    for i in range(len(return_values)):
        prices.append(return_values[i][1][0])

    for i in range(len(products)):
        temp = float(products[i].product_price)
        print(temp, prices[i])
        if float(prices[i]) != float(products[i].product_price):
            products[i].product_price = prices[i]
        if float(prices[i]) <= float(products[i].all_time_low):
            products[i].all_time_low = prices[i]
            message = products[i].product_name + ' is at an all low of ' + prices[i]
            send_notifications(title='Product is at an all time low!', message=message)
            products[i].save()
            continue
        if float(prices[i]) < temp:
            print(type(products[i].product_name), type(prices[i]))
            message = products[i].product_name + ' has reduced to ' + str(prices[i]) + ' from ' + str(temp)
            send_notifications(title='Product price decreased!', message=message)
        products[i].save()
