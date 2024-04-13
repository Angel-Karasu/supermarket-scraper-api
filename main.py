from requests import Session

from classes import SuperMarket
from supermarkets import intermarche

session = Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'

SUPERMARKETS: list[SuperMarket] = intermarche.get_supermarkets(session)