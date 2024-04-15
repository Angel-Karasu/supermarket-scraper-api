from bs4 import BeautifulSoup, SoupStrainer
from json import loads
from requests import Session

SESSION = Session()
SESSION.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'

def bs4_request(url:str, headers:dict[str, str] = {}, cookies:dict[str, str] = {}, html_element:str|dict[str, dict[str, str]] = 'body') -> BeautifulSoup:
    return BeautifulSoup(SESSION.get(url, headers=headers, cookies=cookies).content, 'lxml', parse_only=SoupStrainer(html_element))

def bs4_to_json(soup: BeautifulSoup) -> dict: return loads(soup.text)

def json_request(url:str, headers:dict[str, str] = {}, cookies:dict[str, str] = {}) -> dict:
    return loads(SESSION.get(url, headers=headers, cookies=cookies).text)