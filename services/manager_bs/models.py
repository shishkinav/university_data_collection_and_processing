import requests
from abc import ABC
from urllib.parse import urljoin
from .bs_exceptions import BSRequestFail, BSConnectionError
from bs4 import BeautifulSoup


class MyBaseBS(ABC):
    _base_url: str = ""
    _path_result_dir: str = ""
    TIMEOUT: int = 20

    def __str__(self):
        return self.__class__.__name__

    def prepare_headers(self, headers: dict) -> dict:
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        return headers

    def _check_base_url(self, url: str) -> str:
        return f'{url}/' if url[-1] != '/' else url

    def _check_part_url(self, part_url: str) -> str:
        return part_url[1:] if part_url[0] == '/' else part_url

    def send_request(self, part_url: str,
                     method: str = 'GET',
                     data: dict = {},
                     json: dict = {},
                     params: dict = {},
                     headers: dict = {}):
        _headers = self.prepare_headers(headers)
        _request = {'GET': requests.get,
                    'POST': requests.post,
                    'PUT': requests.put,
                    'DELETE': requests.delete}[method.upper()]
        _url = urljoin(
            self._check_base_url(self._base_url),
            self._check_part_url(part_url)
        )
        try:
            response = _request(_url, data=data, json=json, params=params,
                                headers=_headers, timeout=self.TIMEOUT)
            if not response.ok:
                raise BSRequestFail(response.status_code, response.text)
            return response
        except (requests.ConnectionError, requests.ReadTimeout, requests.Timeout) as err:
            raise BSConnectionError(err)

    def save_page(self, part_url: str, path_file: str, params: dict = {}) -> bool:
        """
        Сохраняем страницу в файл
        :param part_url: оставшаяся часть пути после base_url
        :param path_file: полный путь куда необходимо сохранить файл
        :return: True or Exception
        """
        html = self.send_request(part_url, params=params)
        with open(path_file, 'w', encoding='utf-8') as wfile:
            wfile.write(html.text)
        return True

    def get_soup(self, path: str, file: bool = False, params: dict = {}) -> BeautifulSoup:
        """
        Получить объект BeautifulSoup на основе файла или url
            с необходимым текстом html для парсинга
        :param path: полный путь до файла или part_url (часть пути,
            которая дополняет base_url)
        :param params: get-параметры для запроса страницы
        :param file: признак указывающий что для сборки soup будет
            использоваться path, который является полным путём до
            файла (True), иначе path - это part_url страницы
        :return: экземпляр BeautifulSoup
        """
        if file:
            with open(path, 'r', encoding='utf-8') as file:
                text_parse = file.read()
        else:
            html = self.send_request(path, params=params)
            text_parse = html.text
        return BeautifulSoup(text_parse, 'html.parser')


