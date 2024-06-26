from utils.classes import Product, SortBy, SuperMarket
from utils.scrap import get_redirect_url
from utils.scripts import euro_to_float

class Auchan(SuperMarket):
    def search_products(self, search:str, page:int, sortby:SortBy, descending_order:bool) -> list[Product]:
        sort = ('de' if descending_order else 'a') + 'sc_'
        sort += ('' if sortby == SortBy.price_absolute else 'unit') + 'price_pos'
        sort = 'default' if sortby == SortBy.relevant else sort

        soup = self.bs4_request(
            get_redirect_url(f'{self.url_origin()}/recherche?text={search}')+ f'&sort={sort}&page={page}',
            'article'
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
                    self.url_origin() + product.select_one('a')['href'],
                    price_absolute,
                    price_absolute if price_relative is None else euro_to_float(price_relative.text),
                    '€', 'u' if price_relative is None else price_relative.text.split('/ ')[1],
                ))
            except: pass

        return products

def get_supermarkets() -> list[SuperMarket]:
    return [Auchan('Auchan', base_url='www.auchan.fr', cookies={'lark-journey': '9d43e4d0-c397-4ffc-a998-c0572174fd84'})]