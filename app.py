from fastapi import FastAPI, Path
from uvicorn import run

from classes import Product, SortBy, SuperMarket
from main import SUPERMARKETS

HOST = '0.0.0.0'
PORT = 5500

app = FastAPI()

@app.get('/get_supermarkets')
def get_supermarkets() -> list[SuperMarket]: return SUPERMARKETS

@app.get('/get_supermarket_by_id/{id}')
def get_supermarket_by_id(id:int = Path(ge=0, lt=len(SUPERMARKETS))) -> SuperMarket:
    return SUPERMARKETS[id]

@app.get('/search_product/{id_supermarket}/?search={search}&page={page}&sortby={sortby}&ascending_order={ascending_order}')
def search_product(search:str, sortby:SortBy, ascending_order:bool, page:int = Path(ge=1), id_supermarket:int = Path(ge=0, lt=len(SUPERMARKETS))) -> list[Product]:
    return SUPERMARKETS[id_supermarket].search_products(search, page, sortby, ascending_order)

if __name__ == '__main__': run('app:app', host=HOST, port=PORT, reload=True)