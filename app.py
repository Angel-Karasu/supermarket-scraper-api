from fastapi import FastAPI, Path
from uvicorn import run

from classes import Product, SuperMarket
from main import SUPERMARKETS

HOST = '0.0.0.0'
PORT = 5500

app = FastAPI()

@app.get('/get_supermarkets')
def get_supermarkets() -> list[SuperMarket]: return SUPERMARKETS.supermarkets

@app.get('/get_supermarket_by_id/{id}')
def get_supermarket_by_id(id:int = Path(ge=0, lt=len(SUPERMARKETS.supermarkets))) -> SuperMarket:
    return SUPERMARKETS.supermarkets[id]

@app.get('/search_product/{list_index_supermarket}/{search}/{page}/{sortby}/{ascending_order}')
def search_product(list_index_supermarket:str, search:str, page:int, sortby:str, ascending_order:bool) -> list[Product]:
    return SUPERMARKETS.search_products(list(map(int, list_index_supermarket.split(','))), search, page, sortby, ascending_order)

if __name__ == '__main__': run('app:app', host=HOST, port=PORT, reload=True)