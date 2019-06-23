import http
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup


def scrape(product_url):
    print('amazon')
    try:
        page_html = urlopen(product_url).read()
    except http.client.IncompleteRead as e:
        page_html = e.partial

    names, prices, ratings, image_urls = [], [], [], []

    page_soup = BeautifulSoup(page_html, 'lxml')
    page_title_tag = page_soup.findAll('span', {'id': 'productTitle'})
    names.append(page_title_tag[0].string.strip())
    price_tag = page_soup.findAll('span', {'id': 'priceblock_ourprice'})
    prices.append(price_tag[0].text.strip()[2:])
    ratings.append(0.0)
    image_tag = page_soup.findAll('img', {'id': 'landingImage'})
    image_urls.append(image_tag[0]['src'])

    print('h', names[0], prices[0], ratings[0], image_urls[0])

    return names, prices, ratings, image_urls
