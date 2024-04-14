from dataclasses import dataclass
from enum import Enum
from requests import Session

@dataclass
class Address:
    address:str
    postal_code:int
    city:str

    def include(self, address:'Address') -> bool:
        return self.address in address.address and str(self.postal_code) in str(address.postal_code) and self.city in address.city

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
    relevant = 'relevant'
    price_absolute = 'price_absolute'
    price_relative = 'price_relative'

@dataclass
class SuperMarket:
    name:str
    address:Address

    base_url:str
    cookies:dict[str, str]

    def include(self, supermarket:'SuperMarket') -> bool:
        return self.name in supermarket.name and self.address.include(supermarket.address)

    def search_products(self, search:str, page:int, sortby:SortBy, descending_order:bool) -> list[Product]: return []