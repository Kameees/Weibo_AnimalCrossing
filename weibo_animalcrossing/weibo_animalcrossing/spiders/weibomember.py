# -*- coding: utf-8 -*-
import scrapy
import json
from weibo_animalcrossing.items import WeiboAnimalcrossingItem


class WeibomemberSpider(scrapy.Spider):
    name = 'weibomember'
    #allowed_domains = ['m.weibo.cn']
    start_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231522type%3D61%26q%3D%23%E9%9B%86%E5%90%88%E5%95%A6%E5%8A%A8%E7%89%A9%E6%A3%AE%E5%8F%8B%E4%BC%9A%23%26t%3D10&extparam=%23%E9%9B%86%E5%90%88%E5%95%A6%E5%8A%A8%E7%89%A9%E6%A3%AE%E5%8F%8B%E4%BC%9A%23&luicode=10000011&lfid=100103type%3D38%26q%3D%E5%8A%A8%E7%89%A9%E6%A3%AE%E5%8F%8B%E4%BC%9A%26t%3D0&page_type=searchall&page={page}'
    #   https://m.weibo.cn/api/container/getIndex?containerid=231522type%3D61%26q%3D%23%E9%9B%86%E5%90%88%E5%95%A6%E5%8A%A8%E7%89%A9%E6%A3%AE%E5%8F%8B%E4%BC%9A%23%26t%3D10&extparam=%23%E9%9B%86%E5%90%88%E5%95%A6%E5%8A%A8%E7%89%A9%E6%A3%AE%E5%8F%8B%E4%BC%9A%23&luicode=10000011&lfid=100103type%3D38%26q%3D%E5%8A%A8%E7%89%A9%E6%A3%AE%E5%8F%8B%E4%BC%9A%26t%3D0&page_type=searchall&page=1

    def start_requests(self):
        yield scrapy.Request(self.start_url.format(page=1), callback=self.weibo_parse, meta={'page': 1})

    def weibo_parse(self, response):
        """
        解析weibo超话页面信息
        :param response:
        :return:
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards'):
            weibos = result.get('data').get('cards')
            for weibo in weibos:
                mblog = weibo.get('mblog')
                user = mblog.get('user')
                #if mblog:
                weibo_item = WeiboAnimalcrossingItem()
                weibo_item['id'] = user.get('id')
                weibo_item['screen_name'] = user.get('screen_name')
                weibo_item['created_at'] = mblog.get('created_at')
                weibo_item['profile_url'] = user.get('profile_url')
                weibo_item['description'] = user.get('description')
                weibo_item['gender'] = user.get('gender')
                weibo_item['text'] = mblog.get('text')
                weibo_item['reposts_count'] = mblog.get('reposts_count')
                weibo_item['comments_count'] = mblog.get('comments_count')
                weibo_item['attitudes_count'] = mblog.get('attitudes_count')
                weibo_item['verified'] = user.get('verified')
                weibo_item['verified_type'] = user.get('verified_type')
                weibo_item['verified_reason'] = user.get('verified_reason')
                weibo_item['scheme'] = weibo.get('scheme')
                yield weibo_item
            page = response.meta.get('page') + 1
            yield scrapy.Request(self.start_url.format(page=page), callback=self.weibo_parse, meta={'page': page})
                    