import requests
import json as jsonlib
from urllib.parse import urljoin
from main import (GITHUB_USERNAME, GITHUB_TOKEN,)
from .api_exceptions import APIConnectionError, APIRequestFail


class MyGitHub:
    _base_url: str = "https://api.github.com"
    USERNAME: str = GITHUB_USERNAME
    TOKEN: str = GITHUB_TOKEN
    TIMEOUT: int = 20

    def __str__(self):
        return self.__class__.__name__

    def prepare_headers(self, headers: dict) -> dict:
        return headers.update({"Authorization": f"token {self.TOKEN}"})

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
                raise APIRequestFail(response.text)
            return jsonlib.dumps(response.json(), indent=2, ensure_ascii=False)
        except (requests.ConnectionError, requests.ReadTimeout, requests.Timeout) as err:
            raise APIConnectionError(err)

    def get_public_info(self, username: str):
        """
        Provides publicly available information about someone with a GitHub account.
        """
        return self.send_request(f'/users/{username}',
                                 headers={"Accept": "application/vnd.github.v3+json"})

    def repositories_list(self, username: str):
        """
        Lists public repositories for the specified user
        """
        return self.send_request(f'/users/{username}/repos')

