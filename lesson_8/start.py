from pprint import pprint

from pymongo.collection import Collection
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from booklife.spiders.insta import InstaSpider
from booklife import settings
from main import INSTAGRAM_LOGIN
from services.manager_mongo.models import MyMongoClient

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaSpider)
    process.start()

    client = MyMongoClient(database_name='books')
    collection: Collection = client.get_collection('followers')
    pprint(collection.find({"username": INSTAGRAM_LOGIN}))

