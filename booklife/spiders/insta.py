import hashlib
import json
import re
from copy import deepcopy
from urllib.parse import urlencode

import scrapy
from scrapy.http import HtmlResponse
from booklife.converters import InstaItemConverter
from booklife.items import InstaparserItem, FollowerItem

from main import INSTAGRAM_LOGIN, INSTAGRAM_HASH_POSTS, INSTAGRAM_HASH_PASSWORD


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com']
    insta_login = INSTAGRAM_LOGIN
    insta_pass = INSTAGRAM_HASH_PASSWORD
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    user_parse = 'bernikovandrey'
    posts_hash = INSTAGRAM_HASH_POSTS
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    custom_settings: dict = {
        "ITEM_PIPELINES": {'booklife.pipelines.BooklifePipeline': 300,
                           'booklife.pipelines.InstaFollowersPipeline': 250,
                           # 'booklife.pipelines.PhotosObjectPipeline': 200
                           }
    }
    converter = InstaItemConverter()

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,
                                 method='POST',
                                 callback=self.user_login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pass},
                                 headers={'X-CSRFToken': csrf})

    def user_login(self, response: HtmlResponse):
        j_body = response.json()
        if j_body['authenticated']:
            # yield response.follow(f'/{self.user_parse}',
            #                       callback=self.user_data_parse,
            #                       cb_kwargs={'username': self.user_parse})
            yield response.follow(f'/{self.insta_login}',
                                  callback=self.get_followers,
                                  cb_kwargs={'username': self.insta_login})

    def get_followers(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        api_url = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=5&search_surface=follow_list_page'
        _headers = deepcopy(response.headers)

        # _headers = 'User-Agent : 'Instagram 155.0.0.37.107''
        yield response.follow(api_url,
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                              callback=self.parse_followers,
                              cb_kwargs={'owner_id': user_id, 'owner_username': self.insta_login,
                                         'old_response': response})

    def parse_followers(self, response: HtmlResponse, owner_id, owner_username, old_response: HtmlResponse):
        _followers_list = response.json().get('users')
        for follower in _followers_list:
            user_id = follower.get('pk')
            username = follower.get('username')
            yield old_response.follow(f'/{username}',
                                      cb_kwargs={'username': username})
            item = FollowerItem(user_id=owner_id,
                                username=owner_username,
                                follower_id=user_id,
                                follower_username=username,
                                _id=hashlib.sha1(str(owner_username + username).encode()).hexdigest()
                                )
            yield item

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            'id': user_id,
            'first': 12
        }
        url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'

        yield response.follow(url_posts,
                              callback=self.user_posts_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)}
                              )

    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
        if response.status == 200:
            j_data = response.json()

            page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
            if page_info.get('has_next_page'):
                variables['after'] = page_info.get('end_cursor')
                variables = deepcopy(variables)
                _url = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
                yield response.follow(_url,
                                      callback=self.user_posts_parse,
                                      cb_kwargs={'username': username,
                                                 'user_id': user_id,
                                                 'variables': variables})

            posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
            for post in posts:
                item = InstaparserItem(user_id=user_id,
                                       username=username,
                                       image=post.get('node').get('display_url'),
                                       likes=post.get('node').get('edge_media_preview_like').get('count'),
                                       # post_data=post.get('node')
                                       _id=post.get('node').get('id')
                                       )
                yield item


    def fetch_csrf_token(self, text):
        """
        Получаем токен для авторизации
        """
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        """
        Получаем id желаемого пользователя
        """
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
