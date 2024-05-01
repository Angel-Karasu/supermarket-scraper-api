from json import loads

from utils.classes import Address, Product, SortBy, SuperMarket

class Monoprix(SuperMarket):
    def search_products(self, search:str, page:int, sortby:SortBy, descending_order:bool) -> list[Product]:
        if page > 1: return []
        sort = 'price' if sortby == SortBy.price_absolute else 'pricePer' if sortby == SortBy.price_relative else ''
        sort += ('De' if descending_order else 'A') + 'scending'

        soup = self.bs4_request(
            f'/products/search?q={search}&sortBy={sort}',
            html_element={'div':{'class':'product-card-container'}}
        )

        products = []

        for product in soup.select('.product-card-container'):
            if product.select_one('[data-test="fop-featured"]') is None:
                product_url = self.url_origin() + product.select_one('a')['href']
                
                product_data = loads(self.bs4_request(
                    product_url,
                    html_element={'script':{'data-test':'product-details-structured-data'}}
                ).select_one('[data-test="product-details-structured-data"]').text)

                price_per_unit = product.select_one('[data-test="fop-price-per-unit"]').text.split()

                products.append(Product(
                    product_data['brand'],
                    product_data['name'],
                    product_data['image'][0],
                    product_url,
                    float(product_data['offers']['price']),
                    float(price_per_unit[0].replace(',', '.').replace('(', '')),
                    '€',
                    'L' if 'litre' in price_per_unit[-1] else 'Kg'
                ))

        return products

def get_supermarkets() -> list[SuperMarket]:
    return [Monoprix('Monoprix', Address('', '', ''), 'courses.monoprix.fr', {})]