import scrapy
from .base import BaseSpider
from booklife.converters import LeroyMerlinItemConverter
from urllib.parse import urljoin


class LmSpider(BaseSpider):
    """
    Паук унаследованный от расширенной модели.
        Парсинт Леруа Мерлен по фразе, передаваемой в target при инициализации.
    """
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://volgograd.leroymerlin.ru/search/?q={target}']
    custom_settings: dict = {
        "ITEM_PIPELINES": {'booklife.pipelines.BooklifePipeline': 300,
                           'booklife.pipelines.ParamsPipline': 250,
                           'booklife.pipelines.PhotosObjectPipeline': 200
        }
    }
    converter = LeroyMerlinItemConverter()

    def __init__(self, *args, **kwargs):
        super(LmSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        links = response.xpath('//a[@data-qa="product-name"]/@href').getall()
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            page_number = next_page[-1:]
            yield response.follow(
                urljoin(response.url, f'?q={self.target}&page={page_number}'),
                callback=self.parse
            )
        for link in links:
            yield response.follow(link,
                                  callback=self.converter.parse_data)

