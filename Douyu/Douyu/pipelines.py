# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json,scrapy, os
from Douyu.settings import *
from  scrapy.pipelines.images import ImagesPipeline

class DouyuPipeline(object):
    def __init__(self):
        self.file = open('douyu.json', 'wb')


    def process_item(self, item, spider):
        item_json = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.file.write(item_json.encode())
        return item

    def __del__(self):
        self.file.close()

class DouyuImagesPipeline(ImagesPipeline):
    images_store = IMAGES_STORE

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image'])
    def item_completed(self, results, item, info):
        image = [ data['path']  for status, data in results if status][0]
        old_name = self.images_store + os.sep + image
        new_name = self.images_store + os.sep + image.split('/')[0] +os.sep + item['nick_name'] + '.jpg'
        os.rename(old_name, new_name)
        item['image'] = new_name
        return item

