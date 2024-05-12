from bs4 import BeautifulSoup, SoupStrainer
from requests import Session

SESSION = Session()
SESSION.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'

def bs4_request(url:str, cookies:dict[str, str], soupstrainer:SoupStrainer) -> BeautifulSoup:
    return BeautifulSoup(SESSION.get(url, cookies=cookies).content, 'lxml', parse_only=soupstrainer)

def get_redirect_url(url:str, headers:dict[str, str] = {}, cookies:dict[str, str] = {}) -> str:
    return SESSION.get(url, headers=headers, cookies=cookies).url

def json_request(url:str, headers:dict[str, str] = {}, cookies:dict[str, str] = {}) -> dict:
    return SESSION.get(url, headers=headers, cookies=cookies).json()