# -*- coding: utf-8 -*-
import re

import scrapy
import json
from weibo_animalcrossing.items import WeiboAnimalcrossingItem


class WeibomemberSpider(scrapy.Spider):
    name = 'weibomember'
    min_since_id = None
    #allowed_domains = ['m.weibo.cn']
    start_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100808a6c64b07163fe20e1a35fee1538280ed_-_sort_time&extparam=%E9%9B%86%E5%90%88%E5%95%A6%E5%8A%A8%E7%89%A9%E6%A3%AE%E5%8F%8B%E4%BC%9A&luicode=10000011&lfid=100808a6c64b07163fe20e1a35fee1538280ed_-_sort_time'
    next_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100808a6c64b07163fe20e1a35fee1538280ed_-_sort_time&extparam=%E9%9B%86%E5%90%88%E5%95%A6%E5%8A%A8%E7%89%A9%E6%A3%AE%E5%8F%8B%E4%BC%9A&luicode=10000011&lfid=100808a6c64b07163fe20e1a35fee1538280ed_-_sort_time&since_id={since_id}'
    #   https://m.weibo.cn/api/container/getIndex?containerid=100808a6c64b07163fe20e1a35fee1538280ed_-_sort_time&extparam=%E9%9B%86%E5%90%88%E5%95%A6%E5%8A%A8%E7%89%A9%E6%A3%AE%E5%8F%8B%E4%BC%9A&luicode=10000011&lfid=100808a6c64b07163fe20e1a35fee1538280ed_-_sort_time&since_id=4496460294649692

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.first_weibo_parse)

    def first_weibo_parse(self, response):
        """
            解析weibo超话首页的页面信息
            :param response:
            :return:
        """
        result = json.loads(response.text)
        cards = len(result.get('data').get('cards'))
        if result.get('ok') and result.get('data').get('cards')[cards-1].get('card_group'):
            weibos = result.get('data').get('cards')[cards-1].get('card_group')
            for weibo in weibos:
                mblog = weibo.get('mblog')
                if mblog:
                    user = mblog.get('user')
                    # 获取最小since_id,下次请求使用
                    r_since_id = mblog['id']
                    if self.min_since_id:
                        self.min_since_id = r_since_id if self.min_since_id > r_since_id else self.min_since_id
                    else:
                        self.min_since_id = r_since_id
                    #   获取各参数存入item
                    weibo_item = WeiboAnimalcrossingItem()
                    weibo_item['id'] = user.get('id')
                    weibo_item['screen_name'] = user.get('screen_name')
                    weibo_item['created_at'] = mblog.get('created_at')
                    weibo_item['profile_url'] = user.get('profile_url')
                    weibo_item['description'] = user.get('description')
                    weibo_item['gender'] = user.get('gender')
                    weibo_item['text'] = mblog.get('text')
                    weibo_item['text_little'] = re.compile(r'<[^>]+>', re.S).sub(" ", mblog.get('text'))
                    weibo_item['reposts_count'] = mblog.get('reposts_count')
                    weibo_item['comments_count'] = mblog.get('comments_count')
                    weibo_item['attitudes_count'] = mblog.get('attitudes_count')
                    weibo_item['verified'] = user.get('verified')
                    weibo_item['verified_type'] = user.get('verified_type')
                    weibo_item['verified_reason'] = user.get('verified_reason')
                    weibo_item['scheme'] = weibo.get('scheme')
                    yield weibo_item
        yield scrapy.Request(self.next_url.format(since_id=self.min_since_id), callback=self.weibo_parse, dont_filter=True)

    def weibo_parse(self, response):
        """
        解析weibo超话页面信息
        :param response:
        :return:
        """
        result = json.loads(response.text)
        cards = result.get('data').get('cards')
        if result.get('ok') and cards[0].get('card_group'):
            weibos = cards[0].get('card_group')
            for weibo in weibos:
                mblog = weibo.get('mblog')
                if mblog:
                    user = mblog.get('user')
                    r_since_id = mblog['id']
                    if self.min_since_id:
                        self.min_since_id = r_since_id if self.min_since_id > r_since_id else self.min_since_id
                    else:
                        self.min_since_id = r_since_id
                    weibo_item = WeiboAnimalcrossingItem()
                    weibo_item['id'] = user.get('id')
                    weibo_item['screen_name'] = user.get('screen_name')
                    weibo_item['created_at'] = mblog.get('created_at')
                    weibo_item['profile_url'] = user.get('profile_url')
                    weibo_item['description'] = user.get('description')
                    weibo_item['gender'] = user.get('gender')
                    weibo_item['text'] = mblog.get('text')
                    weibo_item['text_little'] = re.compile(r'<[^>]+>', re.S).sub(" ", mblog.get('text'))
                    weibo_item['reposts_count'] = mblog.get('reposts_count')
                    weibo_item['comments_count'] = mblog.get('comments_count')
                    weibo_item['attitudes_count'] = mblog.get('attitudes_count')
                    weibo_item['verified'] = user.get('verified')
                    weibo_item['verified_type'] = user.get('verified_type')
                    weibo_item['verified_reason'] = user.get('verified_reason')
                    weibo_item['scheme'] = weibo.get('scheme')
                    yield weibo_item
        yield scrapy.Request(self.next_url.format(since_id=self.min_since_id), callback=self.weibo_parse, dont_filter=True)