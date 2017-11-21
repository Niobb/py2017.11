# -*- coding: utf-8 -*-
import scrapy
import json
from Douyu.items import *


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['douyucdn.cn']
    start_urls = ['http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=100&offset=']
    offset = 0
    def parse(self, response):
        # print(response.status)
        data_list = json.loads(response.body.decode())['data']
        # print(len(data_list))
        if len(data_list) != 0:
            for data in data_list:
                item = DouyuItem()
                item['nick_name'] = data['nickname']
                item['uid'] = data['owner_uid']
                item['city'] = data['anchor_city']
                item['room_name'] = data['room_name']
                item['image'] = data['vertical_src']
                # print(item)
                yield item

            self.offset += 100
            url = self.start_urls[0] + str(self.offset)
            yield scrapy.Request(url, callback=self.parse)
