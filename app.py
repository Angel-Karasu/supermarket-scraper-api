from fastapi import FastAPI, Path, Query
from uvicorn import run

from classes import Product, SortBy, SuperMarket
from main import SUPERMARKETS

HOST = '0.0.0.0'
PORT = 5500

app = FastAPI()

@app.get('/get_sortby_methods')
def get_sortby_methods() -> list[tuple[str, str]]: return [(sortby.name, sortby.value) for sortby in SortBy]

@app.get('/get_supermarkets')
def get_supermarkets() -> list[SuperMarket]: return SUPERMARKETS.supermarkets

@app.get('/search_product/{search}')
def search_product(
    search:str, page:int = 1, sortby:SortBy = SortBy.relevant, descending_order:bool = False,
    list_supermarket_id:list[int] = Query([0])
) -> list[Product]: return SUPERMARKETS.search_products(list_supermarket_id, search, page, sortby, descending_order)

@app.get('/supermarket/{id}/get_supermarket')
def supermarket_get_supermarket(id:int = Path(ge=0, lt=SUPERMARKETS.max_id)) -> SuperMarket: return SUPERMARKETS.supermarkets[id]

@app.get('/supermarket/{id}/search_product/{search}')
def supermarket_search_product(
    search:str, page:int = 1, sortby:SortBy = SortBy.relevant, descending_order:bool = False,
    id:int = Path(ge=0, lt=SUPERMARKETS.max_id)    
) -> list[Product]: return search_product(search, page, sortby, descending_order, [id])

if __name__ == '__main__': run('app:app', host=HOST, port=PORT, reload=True)