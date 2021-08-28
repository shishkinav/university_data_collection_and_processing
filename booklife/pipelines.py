# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import pathlib as ph
from services.manager_mongo.models import MyMongoClient
from pymongo.collection import Collection
from scrapy.pipelines.images import ImagesPipeline
from lxml import html
from booklife.items import FollowerItem


class BooklifePipeline:
    """
    Единый pipeline для сохранения Item в БД
    """
    def __init__(self):
        self.client = MyMongoClient(database_name='books')

    def process_item(self, item, spider):
        if isinstance(item, FollowerItem):
            return item
        collection: Collection = self.client.get_collection(spider.name)
        if not collection:
            collection: Collection = self.client.create_collection(spider.name)
        item_data = spider.converter.prepare_data(item)
        collection.update_one({'_id': item_data['_id']}, {"$set": item_data}, upsert=True)
        # collection.insert_one(item_data)
        return item


class ParamsPipline:
    """
    Собирает характеристики товаров с Леруа Мерлен
    """
    def process_item(self, item, spider):
        params = item['params']
        _p_data = dict()
        for param in params:
            dom = html.fromstring(param)
            name = dom.xpath(".//dt/text()")[0].strip()
            value = dom.xpath(".//dd/text()")[0].strip()
            _p_data.update({name: value})
        item['params'] = _p_data
        return item


class PhotosObjectPipeline(ImagesPipeline):
    """
    Единый pipeline для обработки информации по изображениям и их загрузки
    """
    def file_path(self, request, response=None, info=None, *, item=None):
        """
        Переопределяем путь для сохраняемого изображения
        """
        path = ph.Path(request.url)
        image_name = path.name
        if item:
            return f'{item["_id"]}/{image_name}'
        else:
            return f'full/{image_name}.jpg'

    def get_media_requests(self, item, info):
        """
        Загрузка изображений, если они определены для item
        """
        if item['images']:
            for img in item['images']:
                try:
                    yield scrapy.Request(img)
                except Exception as err:
                    print(err)

    def item_completed(self, results, item, info):
        """
        Финальная сборка данных по изображениям в поле images для item
        """
        if results:
            item['images'] = [data for status, data in results if status]
        return item


class InstaFollowersPipeline(BooklifePipeline):
    """
    pipeline обработки инстаграмм пользователей
    """
    def process_item(self, item, spider):
        if not isinstance(item, FollowerItem):
            return item
        collection: Collection = self.client.get_collection('followers')
        if not collection:
            collection: Collection = self.client.create_collection('followers')
        collection.update_one({'_id': item['_id']}, {"$set": item}, upsert=True)
        return item