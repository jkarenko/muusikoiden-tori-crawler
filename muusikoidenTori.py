import re

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://muusikoiden.net/"
SEARCH_URL = "/tori/haku.php?keyword="
QUERY_PREFIX = "&type="


class Item:
    def __init__(self, name, description, price, link):
        self.name = name
        self.description = description
        self.price = price
        self.link = link

    def __str__(self):
        return f"{self.name} - {self.price} - {self.link}"


def get_items_from_url(url, query_type):
    keyword = "Myydään:" if query_type == "sell" else "Ostetaan:"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    items_list = []
    names = [element.parent.text for element in soup.find_all("b", text=re.compile(keyword))]
    descriptions = [element.parent.parent.text for element in soup.find_all("b", text=re.compile(keyword))]
    links = [BASE_URL + element['href'] for element in
             soup.find_all("a", href=re.compile(r'^/tori/ilmoitus/\d+$'))]
    if query_type == "sell":
        prices = [element.parent.text for element in soup.find_all("b", text=re.compile('Hinta:'))]
    else:
        # make an empty list as long as names
        prices = [None] * len(names)
    for (name, description, price, link) in zip(names, descriptions, prices, links):
        items_list.append(Item(name, description, price, link))
    return items_list


def search(query, query_type):
    url = BASE_URL + SEARCH_URL + query + QUERY_PREFIX + query_type
    return get_items_from_url(url, query_type)


if __name__ == "__main__":
    search_term = "ibanez"
    query_type = "buy"
    url = BASE_URL + SEARCH_URL + search_term + QUERY_PREFIX + query_type
    items = get_items_from_url(url, query_type)
    for item in items:
        print(item)
