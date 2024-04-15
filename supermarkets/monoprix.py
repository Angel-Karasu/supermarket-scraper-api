from classes import Address, Product, SortBy, SuperMarket
from scrap import bs4_request, bs4_to_json

BASE_URL = 'courses.monoprix.fr'

class Monoprix(SuperMarket):
    def search_products(self, search:str, page:int, sortby:SortBy, descending_order:bool) -> list[Product]:
        if page > 1: return []
        sort = 'price' if sortby == SortBy.price_absolute else 'pricePer' if sortby == SortBy.price_relative else ''
        sort += 'De' if descending_order else 'A' + 'scending'

        soup = bs4_request(
            f'https://{BASE_URL}/products/search?q={search}&sortBy={sort}',
            html_element={'div':{'class':'components__ProductCardContainer-sc-filq44-2'}}
        )

        products = []

        for product in soup.select('.components__ProductCardContainer-sc-filq44-2'):
            if product.select_one('[data-test="fop-featured"]') is None:
                product_data = bs4_to_json(bs4_request(
                    f'https://{BASE_URL}' + product.select_one('a')['href'],
                    html_element={'script':{'data-test':'product-details-structured-data'}}
                ).select_one('[data-test="product-details-structured-data"]'))

                price_per_unit = product.select_one('[data-test="fop-price-per-unit"]').text.split()

                products.append(Product(
                    product_data['brand'],
                    product_data['name'],
                    product_data['image'][0],
                    float(product_data['offers']['price']),
                    float(price_per_unit[0].replace(',', '.').replace('(', '')),
                    '€',
                    'L' if 'litre' in price_per_unit[-1] else 'Kg'
                ))

        return products

def get_supermarkets() -> list[SuperMarket]:
    return [Monoprix('Monoprix', Address('', '', ''), BASE_URL, {})]