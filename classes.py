from dataclasses import dataclass
from enum import Enum
from requests import Session

@dataclass
class Address:
    address:str
    postal_code:int
    city:str
    
    latitude:float
    longitude:float

@dataclass
class Product:
    brand:str
    description:str
    image_url:str

    price_absolute:float
    price_relative:float

    price_unit:str
    quantity_unit:str

class SortBy(str, Enum):
    price_absolute = 'Price absolute'
    price_relative = 'Price relative'
    relevant = 'Relevant'

@dataclass
class SuperMarket:
    name:str
    address:Address

    base_url:str
    cookies:dict[str, str]

    def search_products(self, search:str, page:int, sortby:SortBy, descending_order:bool) -> list[Product]: return []