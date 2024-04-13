from requests import Session

from classes import Product, SuperMarket
from supermarkets import intermarche

session = Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'

class SuperMarkets:
    def __init__(self) -> None:
        self.supermarkets: list[SuperMarket] = []

    def search_products(self, list_index_supermarket:list[int], search:str = '', page:int = 1, sortby:str = '', ascending_order:bool = True) -> list[Product]:
        products = []
        for i in list_index_supermarket:
            products.extend(self.supermarkets[i].search_products(session, search, page, sortby, ascending_order))

        try: products = sorted(products, key=lambda product: vars(product)[sortby], reverse=not ascending_order)
        except: pass
        
        return products

    def update_supermarkets(self) -> None:
        self.supermarkets = intermarche.get_supermarkets(session)

SUPERMARKETS = SuperMarkets()
SUPERMARKETS.update_supermarkets()