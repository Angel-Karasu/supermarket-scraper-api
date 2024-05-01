from classes import Address, Product, SortBy, SuperMarket
from scrap import bs4_request

BASE_URL = 'www.auchan.fr'

class Auchan(SuperMarket):
    def search_products(self, search:str, page:int, sortby:SortBy, descending_order:bool) -> list[Product]:
        sort = ('de' if descending_order else 'a') + 'sc_'
        sort += ('' if sortby == SortBy.price_absolute else 'unit') + 'price_pos'
        sort = 'default' if sortby == SortBy.relevant else sort

        soup = bs4_request(
            f'https://{BASE_URL}/recherche?text={search}&sort={sort}&page={page}',
            html_element={'article'}
        )

        products = []

        for product in soup.select('article'):
            try: 
                brand = product.select_one('[itemprop="brand"]')
                price_absolute = float(product.select_one('[itemprop="price"]')['content'])
                price_relative = product.select_one('.product-thumbnail__attributes span[data-offer-id]')
            
                products.append(Product(
                    product.select('.product-thumbnail__details span')[1].text if brand is None else brand.text,
                    product.select_one('.product-thumbnail__description').text.split('\n')[-2].strip(),
                    product.select_one('[itemprop="image"]')['content'],
                    'https://' + BASE_URL + product.select_one('a')['href'],
                    price_absolute,
                    price_absolute if price_relative is None else float(price_relative.text.split('€')[0].replace(',', '.')),
                    '€',
                    'u' if price_relative is None else price_relative.text.split('/ ')[1],
                ))
            except: pass

        return products

def get_supermarkets() -> list[SuperMarket]:
    return [Auchan('Auchan', Address('', '', ''), BASE_URL, {})]