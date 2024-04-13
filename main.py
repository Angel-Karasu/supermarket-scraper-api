from heapq import merge
from itertools import zip_longest

from classes import Product, SortBy, SuperMarket
from supermarkets import intermarche

class SuperMarkets:
    supermarkets:list[SuperMarket] = intermarche.get_supermarkets()
    max_id:int = len(supermarkets) - 1

    def search_products(self, list_supermarket_id: list[int], search:str, page:int, sortby:SortBy, descending_order:bool) -> list[Product]:
        list_products:list[list[Product]] = [self.supermarkets[i].search_products(search, page, sortby, descending_order) for i in list_supermarket_id]

        return (
            [product for products in zip_longest(*list_products, fillvalue=None) for product in products if product is not None]
            if sortby == SortBy.relevant else
            list(merge(*list_products, key=lambda product: vars(product)[sortby.name], reverse=descending_order))
        )

SUPERMARKETS = SuperMarkets()