from utils.classes import Product, SortBy, SuperMarket
from utils.scripts import euro_to_float

class Casino(SuperMarket):
    def search_products(self, search:str, page:int, sortby:SortBy, descending_order:bool) -> list[Product]:
        sort = 52 + (sortby == SortBy.price_absolute) + 2*(sortby == SortBy.price_relative)

        soup = self.bs4_request(
            f'/ecommerce/recherche/WE38337/Acheter/{search}?SORT_ORDER={sort}|{int(descending_order)}&page={page}',
            'section'
        )

        products = []
        for product in soup.select('.product-item__inner'):
            price_absolute = euro_to_float(product.select_one('.product-item__offer-price').text)

            price_relative = product.select_one('.product-item__conditioning').text
            quantity_unit = 'u'
            try:
                price_relative = price_relative.split(')')[0].split('(')[1]
                quantity_unit = price_relative.split('/')[1]
                price_relative = euro_to_float(price_relative)
            except:
                try: price_relative = price_absolute / float(price_relative.split('x')[1])
                except: price_relative = price_absolute
            
            products.append(Product(
                product.select_one('.product-item__brand').text,
                product.select_one('.product-item__description').text.strip(),
                self.url_origin() + product.select_one('img')['data-original'],
                self.url_origin() + product.select_one('a')['href'],
                price_absolute,
                price_relative,
                '€', quantity_unit,
            ))

        return products

def get_supermarkets() -> list[SuperMarket]:
    return [Casino('Casino', base_url='www.casino.fr', cookies={'JSESSIONID': 'POGw_Xl7xU4OJwaS-8hTO9esjVBsjwEoew4U_SAPMorr0cO867gg8--yp2YQEWXF'})]