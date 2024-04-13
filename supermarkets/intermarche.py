from classes import Address, Product, SortBy, SuperMarket
from scrap import bs4_request, json_request

INTERMARCHE_BASE_URL = 'www.intermarche.com'

class InterMarche(SuperMarket):
    def search_products(self, search:str, page:int, sortby:SortBy, descending_order:bool) -> list[Product]:
        sort = 'prix' if sortby == SortBy.price_absolute else 'prixkg' if sortby == SortBy.price_relative else 'pertinence'
        order = 'decroissant' if descending_order else 'croissant'

        soup = bs4_request(
            f'https://{INTERMARCHE_BASE_URL}/recherche/{search}?page={page}&trier={sort}&ordre={order}',
            cookies=self.cookies
        )

        products = []

        for product in soup.select('.stime-product-card-course'):
            try: products.append(Product(
                product.select_one('.stime-product--details__summary > p').text,
                product.select_one('.stime-product--details__title').text,
                product.select_one('.stime-product--details__image')['src'],
                float(product.select_one('.product--price').text.split(' ')[0].replace(',', '.')),
                float(product.select_one('.content-S-R').text.split(' ')[-2].replace(',', '.')),
                '€',
                product.select_one('.content-S-R').text.split('/')[-1],
            ))
            except: pass

        return products

def get_supermarkets() -> list[SuperMarket]:
    supermarkets = []

    for market in json_request(
        f'https://{INTERMARCHE_BASE_URL}/api/service/pdvs/v4/pdvs/zone?r=10000',
        headers={'x-red-device': 'red_fo_desktop', 'x-red-version': '3'},
        cookies={'datadome': 'y3wBsQjboarO8qlMEYZ62GeCJ_oG_m0lohMRkWpgkmfaVssb5d~~sPaYm4H8zUP4tYqIwlHXIwWbtyyohfvUG0Ml1XZVgWDTrUVCFSvNUJsMN8tBf3Szckk40emoQqRZ'}
    )['resultats']:

        name = 'Intermarché ' + market['modelLabel'].title()
        add = market['addresses'][0]
        address = Address(add['address'], int(add['postCode']), add['townLabel'], **{l:float(add[l]) for l in ['latitude', 'longitude']})

        supermarkets.append(InterMarche(
            name, address, INTERMARCHE_BASE_URL,
            {'itm_pdv': str({'ref': market['entityCode'], 'name': f'{name.split()[1]} {address.city}', 'city': address.city}).replace("'", '"')}
        ))

    return supermarkets