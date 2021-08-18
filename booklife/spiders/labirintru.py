import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urljoin
from booklife.items import BooklifeItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    base_url = 'https://www.labirint.ru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/фантастика/?stype=0']

    def parse(self, response: HtmlResponse):
        template_part_url = 'search/фантастика/?stype=0&page={page_number}'
        links = response.xpath("//a[@class='product-title-link']/@href").extract()
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").extract_first()
        if next_page:
            page_number = next_page[-1:]
            yield response.follow(
                urljoin(self.base_url, template_part_url.format(page_number=page_number)),
                callback=self.parse
            )

        for link in links:
            yield response.follow(
                urljoin(self.base_url, link),
                callback=self._parse_data
            )

    def _parse_data(self, response: HtmlResponse):
        """
        * Ссылку на книгу
        * Наименование книги
        * Автор(ы)
        * Основную цену
        * Цену со скидкой
        * Рейтинг книги
        """
        link = response.url
        name = response.xpath("//h1/text()").extract_first()
        authors = response.xpath("//a[@data-event-label='author']/text()").extract()
        price_old = response.xpath('//span[@class="buying-priceold-val-number"]/text()').extract_first()
        price_new = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').extract_first()
        rate = response.xpath('//div[@id="rate"]/text()').extract_first()
        yield BooklifeItem(link=link, name=name, authors=authors, price_old=price_old,
                           price_new=price_new, rate=rate)
