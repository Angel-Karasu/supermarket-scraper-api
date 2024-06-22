#!/bin/python
from heapq import merge
from itertools import zip_longest
from threading import Thread

from utils.classes import Product, SortBy, SuperMarket
from supermarkets import auchan, casino, intermarche, monoprix

class SuperMarkets:
    supermarkets:list[SuperMarket] = sum(map(lambda sm:sm.get_supermarkets(), [auchan, casino, intermarche, monoprix]), [])
    max_id:int = len(supermarkets) - 1

    def search_products(self, supermarkets_id: list[int], search:str, page:int, sortby:SortBy, descending_order:bool) -> list[tuple[int, Product]]:
        list_products:list[list[tuple[int, Product]]] = []
        threads:list[Thread] = []

        for i, id in enumerate(supermarkets_id):
            threads.append(Thread(
                target=lambda id: list_products.append([(id, product) for product in self.supermarkets[id].search_products(search, page, sortby, descending_order)]), args=(id,)
            ))
            threads[i].start()
            
        for th in threads: th.join()

        return (
            [product for products in zip_longest(*list_products, fillvalue=None) for product in products if product is not None]
            if sortby == SortBy.relevant else
            list(merge(*list_products, key=lambda product: vars(product[1])[sortby.name], reverse=descending_order))
        )

SUPERMARKETS = SuperMarkets()