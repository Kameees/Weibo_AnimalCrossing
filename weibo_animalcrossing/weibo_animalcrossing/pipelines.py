# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
import time
from weibo_animalcrossing.items import WeiboAnimalcrossingItem
import pymongo
import csv


class WeiboPipeline():
    def parse_time(self, date):
        if re.match('刚刚', date):
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        if re.match('\d+分钟前', date):
            minute = re.match('(\d+)', date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(minute) * 60))
        if re.match('\d+小时前', date):
            hour = re.match('(\d+)', date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(hour) * 60 * 60))
        if re.match('昨天.*', date):
            date = re.match('昨天(.*)', date).group(1).strip()
            date = time.strftime('%Y-%m-%d', time.localtime() - 24 * 60 * 60) + ' ' + date
        if re.match('\d{2}-\d{2}', date):
            date = time.strftime('%Y-', time.localtime()) + date + ' 00:00'
        return date

    def process_item(self, item, spider):
        if isinstance(item, WeiboAnimalcrossingItem):
            if item.get('created_at'):
                item['created_at'] = item['created_at'].strip()
                item['created_at'] = self.parse_time(item.get('created_at'))
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[WeiboAnimalcrossingItem.collection].create_index([('id', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, WeiboAnimalcrossingItem):
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)
        return item


class CsvPipeline(object):

    def open_spider(self, spider):
        self.file = open('car.csv', 'w', newline='', encoding='utf-8-sig')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['id', 'screen_name', 'verified', 'verified_type', 'verified_reason', 'created_at', 'profile_url', 'description', 'gender', 'text', 'reposts_count', 'comments_count', 'attitudes_count', 'scheme'])

    def process_item(self, item, spider):
        self.writer.writerow([item['id'], item['screen_name'], item['verified'], item['verified_type'], item['verified_reason'], item['created_at'], item['profile_url'], item['description'], item['gender'], item['text'], item['reposts_count'], item['comments_count'], item['attitudes_count'], item['scheme']])
        return item

    def close_spider(self, spider):
        self.file.close()