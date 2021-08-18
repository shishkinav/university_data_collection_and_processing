from services.manager_mongo.models import MyMongoClient
from services.manager_bs.models import MyBaseBS
from pymongo.collection import Collection
import re
import datetime as dt
from main import BASE_DIR
from pprint import pprint


result_dir = BASE_DIR / 'lesson_2_and_3' / 'downloads'
result_dir.mkdir(parents=True, exist_ok=True)


class ParserHH(MyBaseBS):
    _base_url = 'https://volgograd.hh.ru'
    _path_result_dir = result_dir / 'hh_result'

    def __init__(self):
        self._path_result_dir.mkdir(parents=True, exist_ok=True)

    def get_paginate_next_part_url(self, soup) -> str:
        next_page = soup.find('a', {'class': "bloko-button", 'data-qa': "pager-next"})
        if next_page:
            return next_page.attrs.get('href')
        return False

    def parse_all_page(self, save_page: bool = True, search_text: str = ''):
        _params = {'clusters': 'true',
                   'ored_clusters': 'true',
                   'st': 'searchVacancy',
                   'text': search_text,
                   'area': 24}
        count_page = 1
        path_file_search = self._path_result_dir / f'vacancies_{count_page}.html'
        if save_page:
            self.save_page(
                part_url='search/vacancy',
                path_file=path_file_search,
                params=_params
            )
            soup = self.get_soup(path_file_search, file=True)
        else:
            soup = self.get_soup('search/vacancy', params=_params)
        dataset = list()
        while True:
            block_vacancy = soup.find_all('div', {'class': 'vacancy-serp-item vacancy-serp-item_premium'})
            for vac in block_vacancy:
                data_vacancy = self.parse_data_vacancy(vac)
                if data_vacancy:
                    dataset.append(data_vacancy)
            next_page_part_url = self.get_paginate_next_part_url(soup)
            if next_page_part_url:
                count_page += 1
                path_file_search = self._path_result_dir / f'vacancies_{count_page}.html'
                if save_page:
                    self.save_page(part_url=next_page_part_url, path_file=path_file_search)
                    soup = self.get_soup(path_file_search, file=True)
                else:
                    soup = self.get_soup(next_page_part_url)
            else:
                break
        return dataset

    def parse_data_vacancy(self, vac) -> dict:
        vacancy_name = vac.find('a', {'data-qa': "vacancy-serp__vacancy-title"}).getText()
        vacancy_date = vac.find(
            'span',
            {'class': "vacancy-serp-item__publication-date vacancy-serp-item__publication-date_short"}
        ).getText()
        vac_date = dt.datetime.strptime(f'{vacancy_date}.{dt.datetime.now().year}', "%d.%m.%Y")
        vacancy_tag = vac.find('a', {'data-qa': "vacancy-serp__vacancy-title"})
        vacancy_link = vacancy_tag.attrs.get('href')
        com = vac.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"})
        if com:
            pattern_1 = r'\d+\s\d+'  # извлечение сумм
            pattern_2 = r'.+\s(\w+)\.'  # для валюты
            pattern_3 = r'(\w+)\s+.+'  # определяем приставку
            sums = re.findall(pattern_1, com.getText())
            sum_list = [''.join(_.split()) for _ in sums]
            cost = {'min_sum': None, 'max_sum': None, 'valute': None}
            if len(sum_list) == 2:
                cost['min_sum'] = sum_list[0]
                cost['max_sum'] = sum_list[1]
            elif len(sum_list) == 1:
                preffix = re.findall(pattern_3, com.getText())[0]
                if preffix == 'до':
                    cost['max_sum'] = sum_list[0]
                else:
                    cost['min_sum'] = sum_list[0]
            valute = re.findall(pattern_2, com.getText())[0]
            cost['valute'] = valute
        else:
            return False
        return {'name': vacancy_name,
                'min_sum': cost['min_sum'],
                'max_sum': cost['max_sum'],
                'valute': cost['valute'],
                'link': vacancy_link,
                'site': self._base_url,
                'date_publication': vac_date}


if __name__ == '__main__':
    mongo_client = MyMongoClient()
    bs_parser_hh = ParserHH()
    try:
        name_сollection = 'vacancy'
        collection: Collection = mongo_client.get_collection(name_сollection)
        if not collection:
            collection: Collection = mongo_client.create_collection(name_сollection)
        # задаём в search_text поисковую фразу
        dataset = bs_parser_hh.parse_all_page(
            save_page=True,
            search_text='Менеджер'
        )
        mongo_client.save_and_update_database(collection, dataset)
        pprint(mongo_client.get_documents_collection(collection))
        """
        Пример выдачи из сохранённых данных в БД:
        
        [{'_id': ObjectId('610ed07fda3995d57dcca138'),
          'date_publication': datetime.datetime(2021, 8, 2, 0, 0),
          'link': 'https://volgograd.hh.ru/vacancy/46708793?from=vacancy_search_list',
          'max_sum': '80000',
          'min_sum': '40000',
          'name': 'Менеджер по продажам в интернет-магазин',
          'site': 'https://volgograd.hh.ru',
          'valute': 'руб'},
         {'_id': ObjectId('610ed07fda3995d57dcca139'),
          'date_publication': datetime.datetime(2021, 8, 5, 0, 0),
          'link': 'https://volgograd.hh.ru/vacancy/46828480?from=vacancy_search_list',
          'max_sum': None,
          'min_sum': '40000',
          'name': 'Менеджер по персоналу',
          'site': 'https://volgograd.hh.ru',
          'valute': 'руб'},
        ...
        """
    except Exception as err:
        print(err)



