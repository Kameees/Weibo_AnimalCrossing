# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboAnimalcrossingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'weibousers'
    id = scrapy.Field()#用户id
    screen_name = scrapy.Field()#用户名
    verified = scrapy.Field()#true为认证用户，false为无认证用户
    verified_type = scrapy.Field()#0为黄V，-1为普通用户,2为蓝V
    verified_reason = scrapy.Field()#认证类型
    created_at = scrapy.Field()#发布时间
    profile_url = scrapy.Field()#用户主页链接
    description = scrapy.Field()#用户个人简介
    gender = scrapy.Field()#性别，m为男性，f为女性
    text = scrapy.Field()#微博内容
    text_little = scrapy.Field()
    reposts_count = scrapy.Field()#转发数
    comments_count = scrapy.Field()#评论数
    attitudes_count = scrapy.Field()#点赞数
    scheme = scrapy.Field()#微博原地址
