from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
import http
from re import findall


def scrape(product_urls):
    n = len(product_urls)
    prices = []
    names = []
    ratings = []
    image_urls = []
    image_class_names = ['2_AcLJ _3_yGjX', '_2_AcLJ']
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

        # Product image url
        for class_name in image_class_names:
            product_image_url_list = page_soup.findAll("div", {"class": class_name})
            if (len(product_image_url_list) > 0):
                image_url = (product_image_url_list[0])['style']
                image_url = (
                    findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]| [! * \(\),] | (?: %[0-9a-fA-F][0-9a-fA-F]))+',
                            image_url))[0]
                print(image_url)
                image_urls.append(image_url[0:len(image_url) - 1])
                break


    for i in range(n):
        print(names[i], prices[i], ratings[i], image_urls[i])

    return names, prices, ratings, image_urls
