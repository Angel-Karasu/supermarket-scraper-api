from json import dumps

from utils.classes import Address, Product, SortBy, SuperMarket
from utils.scrap import bs4_request, json_request

BASE_URL = 'www.intermarche.com'

class InterMarche(SuperMarket):
    def search_products(self, search:str, page:int, sortby:SortBy, descending_order:bool) -> list[Product]:
        sort = 'prix' if sortby == SortBy.price_absolute else 'prixkg' if sortby == SortBy.price_relative else 'pertinence'
        order = ('de' if descending_order else '') + 'croissant'

        soup = bs4_request(
            f'https://{BASE_URL}/recherche/{search}?page={page}&trier={sort}&ordre={order}',
            cookies=self.cookies,
            html_element={'div': {'class':'stime-product-card-course'}}
        )

        products = []

        for product in soup.select('.stime-product-card-course'):
            try:
                content_sr = product.select_one('.content-S-R').text
                products.append(Product(
                    product.select_one('.stime-product--details__summary > p').text,
                    product.select_one('.stime-product--details__title').text + '\n' + content_sr.split('|')[0],
                    product.select_one('.stime-product--details__image')['src'],
                    'https://' + BASE_URL + product.select_one('a')['href'],
                    float(product.select_one('.product--price').text.split()[0].replace(',', '.')),
                    float(content_sr.split()[-2].replace(',', '.')),
                    '€',
                    product.select_one('.content-S-R').text.split('/')[-1],
                ))
            except: pass

        return products

def get_supermarkets() -> list[SuperMarket]:
    supermarkets = []

    for market in json_request(
        f'https://{BASE_URL}/api/service/pdvs/v4/pdvs/zone?r=10000',
        headers={'x-red-device': 'red_fo_desktop', 'x-red-version': '3'},
        cookies={'datadome': 'y3wBsQjboarO8qlMEYZ62GeCJ_oG_m0lohMRkWpgkmfaVssb5d~~sPaYm4H8zUP4tYqIwlHXIwWbtyyohfvUG0Ml1XZVgWDTrUVCFSvNUJsMN8tBf3Szckk40emoQqRZ'}
    )['resultats']:

        name = 'Intermarché ' + market['modelLabel'].title()
        add = market['addresses'][0]
        address = Address(add['address'], int(add['postCode']), add['townLabel'])

        supermarkets.append(InterMarche(
            name, address, BASE_URL,
            {'itm_pdv': dumps({'ref': market['entityCode'], 'name': f'{name.split()[1]} {address.city}', 'city': address.city})}
        ))

    return supermarkets