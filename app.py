from fastapi import FastAPI, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from classes import Address, Product, SortBy, SuperMarket
from main import SUPERMARKETS

HOST = '0.0.0.0'
PORT = 5500

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

@app.get('/get_sortby_methods')
def get_sortby_methods() -> list[str]: return [sortby.name for sortby in SortBy]

@app.get('/get_supermarkets')
def get_supermarkets() -> list[SuperMarket]: return SUPERMARKETS.supermarkets

@app.get('/search_product')
def search_product(
    search:str, page:int = 1, sortby:SortBy = SortBy.relevant, descending_order:bool = False,
    list_supermarket_id:list[int] = Query()
) -> list[tuple[int, Product]]: return SUPERMARKETS.search_products(list_supermarket_id, search, page, sortby, descending_order)

@app.get('/search_supermarkets')
def search_supermarkets(name:str = '', address:str = '', postal_code:int = '', city:str = '') -> list[tuple[int, SuperMarket]]:
    sm = SuperMarket(name, Address(address, postal_code, city), '', {})
    return [(id, supermarket) for id, supermarket in enumerate(SUPERMARKETS.supermarkets) if sm.include(supermarket)]

@app.get('/supermarket/{id}/get_supermarket')
def supermarket_get_supermarket(id:int = Path(ge=0, le=SUPERMARKETS.max_id)) -> SuperMarket: return SUPERMARKETS.supermarkets[id]

@app.get('/supermarket/{id}/search_product')
def supermarket_search_product(
    search:str, page:int = 1, sortby:SortBy = SortBy.relevant, descending_order:bool = False,
    id:int = Path(ge=0, le=SUPERMARKETS.max_id)    
) -> list[Product]: return SUPERMARKETS.supermarkets[id].search_products(search, page, sortby, descending_order)

if __name__ == '__main__': run('app:app', host=HOST, port=PORT, reload=True)