# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooklifeItem(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
    authors = scrapy.Field()
    price_old = scrapy.Field()
    price_new = scrapy.Field()
    rate = scrapy.Field()
    _id = scrapy.Field()
