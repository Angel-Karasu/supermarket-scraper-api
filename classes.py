from dataclasses import dataclass
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

@dataclass
class SuperMarket:
    name:str
    address:Address

    base_url:str
    cookies:dict[str, str]

    def search_products(self, session:Session, search:str, page:int, sortby:str, order:str) -> list[Product]: return []