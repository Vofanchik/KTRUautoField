import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint


class ParseKTRU:

    def get_response(self, ktru):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/51.0.2704.103 Safari/537.36 '
            }
            payloads_ = {f'searchString': ktru, 'recordsPerPage': '_1'}
            response = requests.get(
                f"https://zakupki.gov.ru/epz/ktru/search/results.html",
                params=payloads_, headers=headers)

            soup = BeautifulSoup(response.text, 'html.parser')
            # id_ktru = soup.select('body > form > section:nth-child(2) > div > div >  div:nth-child(1) >  div:nth-child(4) ')
            id_ktru = soup.find(class_='registry-entry__header-mid__number').a.get('href')

            return id_ktru.split('=')[1]
        except:
            return None

    def get_common_info(self, id_ktru):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/51.0.2704.103 Safari/537.36 '
        }
        payload = {'itemId': id_ktru}
        response = requests.get(
            "https://zakupki.gov.ru/epz/ktru/ktruCard/commonInfo.html",
            headers=headers, params=payload)

        soup = BeautifulSoup(response.text, 'html.parser')
        common_info = soup.find(class_='cardMainInfo__section')
        title_ktru = common_info.find(class_='cardMainInfo__content').getText()
        measure_ktru = common_info.find(class_='cardMainInfo__title').getText().replace("Единица измерения:", "").strip()
        common_info_table = soup.find(id='classfrContent')   #.find_all(class_='tableBlock__col')
        nkmi = common_info_table                             #[7].getText().strip().split('\n')[0]
        headers_table = []
        for i in common_info_table.find_all('td'):
            title = i.text.replace('\n', ' ').replace('  ', '').strip()
            headers_table.append(title)

        i_of_okpd = headers_table.index('Общероссийский классификатор продукции по видам экономической деятельности '
 '(ОКПД2)') + 1
        i_of_nkmi = headers_table.index('НОМЕНКЛАТУРНАЯ КЛАССИФИКАЦИЯ МЕДИЦИНСКИХ ИЗДЕЛИЙ ПО ВИДАМ') + 1

        nkmi_dict = {}
        count = 0
        for i in headers_table[i_of_nkmi::2]:
            splited = i.split(' ', 1)
            if splited[0] in headers_table[i_of_nkmi+1+count]:
                lis = [splited[1], headers_table[i_of_nkmi + count]]
            else:
                lis = [splited[1], headers_table[i_of_nkmi + 1 + count]]
            nkmi_dict[splited[0]] = lis
            count+=1

        okpd_dict = {}
        for i in headers_table[i_of_okpd:i_of_nkmi-1:2]:
            splited = i.split(' ', 1)
            okpd_dict[splited[0]] = splited[1]
            count+=1

        classif_dict = {}
        classif_dict['nkmi'] = nkmi_dict#headers_table[i_of_nkmi:]
        classif_dict['okpd'] = okpd_dict#headers_table[i_of_okpd:i_of_nkmi-1:2]
        classif_dict['name'] = title_ktru
        classif_dict['measure'] = measure_ktru


        return classif_dict

    def get_tz_ktru(self, id_ktru):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/51.0.2704.103 Safari/537.36 '
            }
            payload = {'itemId': id_ktru}
            response = requests.get(
                "https://zakupki.gov.ru/epz/ktru/ktruCard/ktru-description.html",
                headers=headers, params=payload)
            soup = BeautifulSoup(response.text, 'html.parser')
            tz_table = soup.find(id='ktruCharacteristicContent')
            headers_table = []

            for i in tz_table.find_all('td'):
                title = i.text.replace('\n', ' ').replace('  ', '').replace('\xa0', '').strip()
                headers_table.append(title)

            indexes_for_table = []
            for i in headers_table:
                if re.search(r'характеристика', i):
                    indexes_for_table.append(headers_table.index(i))

            tz_content = {}
            count = 0
            for i in indexes_for_table:
                if len(indexes_for_table) > count+1:
                    tz_content[headers_table[i].replace('(характеристика', f' {headers_table[i+2]} (характеристика')] = \
                        headers_table[i+1:indexes_for_table[count+1]:2]
                else:
                    tz_content[headers_table[i]] = headers_table[i + 1::2]
                count+=1

            return tz_content
        except:
            return None



# r = ParseKTRU()
# id_ktru = r.get_response('32.50.13.190-00007060')
# # id_ktru = r.get_response('32.50.13.190-00007224')
# # # # id_ktru = r.get_response('32.50.30.110-00000142')
# # #
# # #
# pprint(r.get_common_info(id_ktru))