# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#
# useful for handling different item types with a single interface


import scrapy
import hashlib
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
from scrapy.pipelines.images import ImagesPipeline


class CastoramaParserPipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongobase = client.img

    def process_item(self, item, spider):
        item['_id'] = hashlib.sha256(item['url'].encode()).hexdigest()

        collection = self.mongobase[spider.name]
        try:
            collection.insert_one(item)
        except dke:
            pass
        return item


class CastoramaPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request('https://www.castorama.ru' + img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
