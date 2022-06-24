import requests
from bs4 import BeautifulSoup
from pprint import pprint


class ParseKTRU:

    def get_response(self, ktru):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
            }
            payloads_ = {f'searchString': ktru, 'recordsPerPage': '_1'}
            response = requests.get(
                f"https://zakupki.gov.ru/epz/ktru/search/results.html",
                params=payloads_, headers=headers)

            soup = BeautifulSoup(response.text, 'html.parser')
            # id_ktru = soup.select('body > form > section:nth-child(2) > div > div >  div:nth-child(1) >  div:nth-child(4) ')
            id_ktru = soup.find(class_='registry-entry__header-mid__number').a.get('href')

            return id_ktru
        except:
            return None

    def get_common_info(self, id_ktru):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }
        response = requests.get(
            f"https://zakupki.gov.ru{id_ktru}",
            headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        return response.text


r = ParseKTRU()
id_ktru = r.get_response('32.50.13.190-00007224')
# pprint(id_ktru)
pprint(r.get_common_info(id_ktru))