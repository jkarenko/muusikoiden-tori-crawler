import re

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://muusikoiden.net/"
SEARCH_URL = "/tori/haku.php?keyword="

def get_items_from_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = {}
    names = [element.parent.text for element in soup.find_all("b", text=re.compile('Myydään:'))]
    descriptions = [element.parent.parent.text for element in soup.find_all("b", text=re.compile('Myydään:'))]
    links = [BASE_URL + element['href'] for element in
             soup.find_all("a", href=re.compile(r'/tori/ilmoitus/\d+$'))]
    prices = [element.parent.text for element in soup.find_all("b", text=re.compile('Hinta:'))]
    for (name, description, price, link) in zip(names, descriptions, prices, links):
        items[name] = {'description': description, 'price': price, 'link': link}
    return items


if __name__ == "__main__":
    search_term = "sm58"
    items = get_items_from_url(BASE_URL + SEARCH_URL + search_term)
    for name, data in items.items():
        description, price, link = data['description'], data['price'], data['link']
        print(name, price, link)
