from dataclasses import dataclass, field
from enum import Enum

from utils.scrap import bs4_request, SoupStrainer

@dataclass
class Address:
    address:str = ''
    postal_code:int|str = ''
    city:str = ''

    def include(self, address:'Address') -> bool:
        return self.address in address.address and str(self.postal_code) in str(address.postal_code) and self.city in address.city

@dataclass
class Product:
    brand:str
    description:str
    image_url:str
    product_url:str

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
    address:Address = field(default_factory=Address)

    base_url:str = ''
    cookies:dict[str, str] = field(default_factory=dict)
    
    def bs4_request(self, url:str, html_element:str = 'body', attrs:dict[str, str] = {}):
        return bs4_request(f'{self.url_origin()}{url}' if url[0] == '/' else url, self.cookies, SoupStrainer(html_element, attrs))

    def include(self, supermarket:'SuperMarket') -> bool:
        return (
            (self.name in supermarket.name or supermarket.name in self.name) and
            (self.address.include(supermarket.address) or supermarket.address.include(self.address))
        )

    def search_products(self, search:str, page:int, sortby:SortBy, descending_order:bool) -> list[Product]: return []
    
    def url_origin(self) -> str: return 'https://' + self.base_url