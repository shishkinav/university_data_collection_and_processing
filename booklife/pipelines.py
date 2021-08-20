# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from services.manager_mongo.models import MyMongoClient
from pymongo.collection import Collection


class BooklifePipeline:
    """
    Единый pipeline для обработки поступающих Item
    """
    def __init__(self):
        self.client = MyMongoClient(database_name='books')

    def process_item(self, item, spider):
        collection: Collection = self.client.get_collection(spider.name)
        if not collection:
            collection: Collection = self.client.create_collection(spider.name)
        item_data = spider.converter.prepare_data(item)
        # collection.update_one({'_id': {"$eq": item_data["_id"]}}, item_data, upsert=True)
        collection.insert_one(item_data)
        return item
