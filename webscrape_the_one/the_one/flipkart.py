from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
import http


def scrape(product_urls):
    n = len(product_urls)
    prices = []
    names = []
    ratings = []
    for i in range(n):

        try:
            page_html = ureq(product_urls[i]).read()
        except http.client.IncompleteRead as e:
            page_html = e.partial

        page_soup = soup(page_html, "lxml")

        product_name_list = page_soup.findAll("span", {"class": "_35KyD6"})

        product_price_list = page_soup.findAll("div", {"class": "_1vC4OE _3qQ9m1"})
        product_price = product_price_list[0].string
        product_price = product_price.replace(product_price[0], "")

        product_rating_list = page_soup.findAll("div", {"class": "hGSR34 _2beYZw"})
        if len(product_rating_list) != 0:
            ratings.append(float(product_rating_list[0].text))
        else:
            ratings.append(0.0)

        names.append(product_name_list[0].text.replace(",", ""))
        prices.append(int(product_price.replace(",", "")))

    for i in range(n):
        print(names[i], prices[i], ratings[i])

    return names, prices, ratings
