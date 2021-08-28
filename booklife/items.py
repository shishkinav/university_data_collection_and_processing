# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from decimal import Decimal, ROUND_HALF_UP


class BooklifeItem(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
    authors = scrapy.Field()
    price_old = scrapy.Field()
    price_new = scrapy.Field()
    rate = scrapy.Field()
    _id = scrapy.Field()


def get_price(value):
    try:
        return float(Decimal(value).quantize(Decimal("1.00", ROUND_HALF_UP)))
    except:
        return value


class LeroyMerlinItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    params = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(get_price), output_processor=TakeFirst())
    _id = scrapy.Field(output_processor=TakeFirst())


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    username = scrapy.Field()
    image = scrapy.Field()
    likes = scrapy.Field()
    # post_data = scrapy.Field()
    _id = scrapy.Field()


class FollowerItem(scrapy.Item):
    user_id = scrapy.Field()
    username = scrapy.Field()
    follower_id = scrapy.Field()
    follower_username = scrapy.Field()
    _id = scrapy.Field()
