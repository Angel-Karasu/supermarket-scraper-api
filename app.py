from fastapi import FastAPI, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from functools import reduce
from uvicorn import run

from classes import Product, SortBy, SuperMarket
from main import SUPERMARKETS

HOST = '0.0.0.0'
PORT = 5500

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

@app.get('/get_sortby_methods')
def get_sortby_methods() -> list[str]: return [sortby.name for sortby in SortBy]

@app.get('/get_supermarkets')
def get_supermarkets(name:str = '', address:str = '', city:str = '', postal_code:str = '') -> list[tuple[int, SuperMarket]]:
    return [
        (id, supermarket) for id, supermarket in enumerate(SUPERMARKETS.supermarkets)
        if name in supermarket.name and address in supermarket.address.address and city in supermarket.address.city and postal_code in str(supermarket.address.postal_code)
    ]

@app.get('/search_product')
def search_product(
    search:str, page:int = 1, sortby:SortBy = SortBy.relevant, descending_order:bool = False,
    list_supermarket_id:list[int] = Query([0])
) -> list[Product]: return SUPERMARKETS.search_products(list_supermarket_id, search, page, sortby, descending_order)

@app.get('/supermarket/{id}/get_supermarket')
def supermarket_get_supermarket(id:int = Path(ge=0, lt=SUPERMARKETS.max_id)) -> SuperMarket: return SUPERMARKETS.supermarkets[id]

@app.get('/supermarket/{id}/search_product')
def supermarket_search_product(
    search:str, page:int = 1, sortby:SortBy = SortBy.relevant, descending_order:bool = False,
    id:int = Path(ge=0, lt=SUPERMARKETS.max_id)    
) -> list[Product]: return search_product(search, page, sortby, descending_order, [id])

if __name__ == '__main__': run('app:app', host=HOST, port=PORT, reload=True)