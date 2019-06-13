import time
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from .flipkart import scrape
import http
import validators


def cat_list(category):
    is_category_url = False
    print('im here')
    # try:
    #     page_html = urlopen(category).read()
    #     is_category_url = True
    #     print('should be here')
    #     return scrape(category)
    # except ValueError as e:
    #     category_url = 'https://www.flipkart.com/search?q=' + category
    #     print('should not be here')
    # except http.client.IncompleteRead as e:
    #     print('can be here ')
    #     page_html = e.partial
    #     is_category_url = True
    #     return scrape(category)

    # start_time =  time.time()
    # print('start_time:', start_time)

    if validators.url(category):
        # print('time_taken:', time.time() - start_time)
        return scrape([category, ])

    category_url = 'https://www.flipkart.com/search?q=' + category

    urls = []

    known_class_values = ['_31qSD5', 'Zhf2z-', '_3dqZjq']
    if not is_category_url:
        try:
            page_html = urlopen(category_url).read()
        except http.client.IncompleteRead as e:
            page_html = e.partial

    page_soup = soup(page_html, 'lxml')

    for known_class in known_class_values:
        class_list = page_soup.findAll('a', {'class': known_class})
        print(len(class_list))
        if len(class_list) > 0:
            for i in range(len(class_list)):
                urls.append('')

            for i in range(len(class_list)):
                s = str(class_list[i]['href'])
                urls[i] = 'https://www.flipkart.com' + s
            return scrape(urls)

# _3togXc _3wp706
