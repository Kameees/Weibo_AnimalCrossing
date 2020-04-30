# Weibo_AnimalCrossing
<h4>微博超话“集合啦动物森友会”爬虫+数据分析</h4>
<br>爬虫代码参考:https://github.com/Python3WebSpider/Weibo
<br>
<br>最近在学scrapy和数据分析，本项目仅个人练习用。
<br>
<br>原本是想把动森超话的所有微博爬下来分析的....但是因为微博爬取限制只能爬一部分数据，就只能当练习用了没有什么具体价值。
<br>
<br>突然想起如果是进行用户分析的话还需要考虑重复问题,可以通过id判断
<br>
<h4> NEW UPDATE
<br>增加了付费代理池的设置，通过代理可以爬到1W+数据啦，只要购买的代理IP时间够长+数量多(100+)，按道理可以爬取超话10w+的数据。
<br>**具体爬取过程文档可看个人博客
<br><a href='http://www.kameee.top/archives/scrapyweibospider'>[「Scrapy」爬取微博‘集合啦动物森友会’超话 ]</a>
> 本文及代码参考崔庆才老师的《Python3 网络爬虫开发实战》
>Github地址：https://github.com/Python3WebSpider/Weibo
本项目的Github地址为：[Weibo_AnimalCrossing](https://github.com/Kameees/Weibo_AnimalCrossing)

# **事前准备**

推荐在Anaconda创建虚拟环境进行。请确保事先安装好Scrapy、PyMongo、Requests库。

# **爬取思路**

在微博‘集合啦动物森友会’超话可以看到各个用户发的微博。可通过微博获取用户的id，用户名，性别等用户详情。

# **爬取分析**

选取微博移动端网页(https://m.weibo.cn)作为爬取站点。

![scrapyweibo1.png](https://kameee.top/upload/2020/04/scrapy-weibo-1-1762914280384496bd453af45a905c52.png)

打开开发者工具，切换到XHR过滤器下拉网页可以看到Ajax请求，这些请求就是获取微博详细信息的Ajax请求。

![scrapyweibo2.png](https://kameee.top/upload/2020/04/scrapy-weibo-2-6f9d41e9511c475bb248159f008be1b9.png)

可以看到首页的请求网址为：https://m.weibo.cn/api/container/getIndex?containerid=100808a6c64b07163fe20e1a35fee1538280ed_-_feed&luicode=10000011&lfid=100103type%3D1%26q%3D%E9%9B%86%E5%90%88%E5%95%A6%E5%8A%A8%E7%89%A9%E6%A3%AE%E5%8F%8B%E4%BC%9A

第二页的请求网址为：https://m.weibo.cn/api/container/getIndex?containerid=100808a6c64b07163fe20e1a35fee1538280ed_-_feed&luicode=10000011&lfid=100103type%3D1%26q%3D%E9%9B%86%E5%90%88%E5%95%A6%E5%8A%A8%E7%89%A9%E6%A3%AE%E5%8F%8B%E4%BC%9A&since_id=4497891324776816

可以看出首页请求和第二页的请求网址的区别是多了个since_id参数。

点开请求网址可以看到是一个JSON格式的数据。

![scrapyweibo3.png](https://kameee.top/upload/2020/04/scrapy-weibo-3-33326b42e1874ae3b8fc003cd3af0be2.png)

了解一下JSON的数据结构我们可以找到对应的since_id。

> 微博分页机制：根据时间分页，每一条微博都有一个since_id，时间越大的since_id越大所以在请求时将since_id传入，则会加载对应话题下比此since_id小的微博，然后又重新获取最小since_id将最小since_id传入，依次请求，这样便实现分页。
>
> 了解微博分页机制之后，我们就可以制定我们的分页策略：**我们将上一次请求返回的微博中最小的since_id作为下次请求的参数，这样就等于根据时间倒序分页抓取数据**！

分析一下JSON(data-cards-card_group-mblog)数据格式

每一个mblog都是一条微博。

```
id: 用户id
screen_name: 用户名
verified: true为认证用户，false为无认证用户
verified_type: 认证用户类型
verified_reason: 认证类型
created_at: 发布时间
profile_url: 用户主页链接
description: 用户个人简介
gender: 性别，m为男性，f为女性
text: 微博内容
reposts_count: 转发数
comments_count: 评论数
attitudes_count: 点赞数
scheme: 当前微博原地址
```

# **开始爬取**

使用Scrapy。

创建weibo_animalcrossing项目。

`scrapy startproject weibo_animalcrossing`

进入项目新建spider。

`scrapy genspider weibomember m.weibo.cn`

修改item,设置需要爬取的数据参数。

代码如下：

```python
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
    text_little = scrapy.Field()#清洗后的微博内容
    reposts_count = scrapy.Field()#转发数
    comments_count = scrapy.Field()#评论数
    attitudes_count = scrapy.Field()#点赞数
    scheme = scrapy.Field()#微博原地址
```

修改spider文件夹weibomember.py编写爬取规则。

因为首页和下一页的请求JSON格式有稍稍的不同，所以写了first_weibo_parse()和weibo_parse()两个方法进行解析。

代码如下：

```python
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
```

# **清洗爬取的数据和存储**

有些微博的时间(created_at)并没有具体时间只有‘刚刚’，‘几分钟前’等这种。需要处理一下格式。

数据清洗完毕之后，需要将爬取的数据存入MongoDB和保存为CSV文件。具体代码实现在pipelines.py中。

```
WeiboPipeline():数据清洗
MongoPipeline():存入MongoDB
CsvPipeline():存入CSV
```

代码如下：

```python
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
        self.file = open('weibo.csv', 'w', newline='', encoding='utf-8-sig')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['id', 'screen_name', 'verified', 'verified_type', 'verified_reason', 'created_at', 'profile_url', 'description', 'gender', 'text', 'text_little', 'reposts_count', 'comments_count', 'attitudes_count', 'scheme'])

    def process_item(self, item, spider):
        self.writer.writerow([item['id'], item['screen_name'], item['verified'], item['verified_type'], item['verified_reason'], item['created_at'], item['profile_url'], item['description'], item['gender'], item['text'], item['text_little'], item['reposts_count'], item['comments_count'], item['attitudes_count'], item['scheme']])
        return item

    def close_spider(self, spider):
        self.file.close()
```

# **应对微博反爬**

微博的反爬能力很强，之前测试的时候发现每当爬到1600条数据时就爬取不到请求了，这是因为微博的反爬措施。但是为了顺利进行爬取，我们需要搭建代理池或者cookies池。

因为没有批量的微博账号获取cookie，所以这里使用了付费代理的方式。(这里实现了使用cookie进行爬取的方法，但是没有调用)。因为使用的是付费代理池，每个代理商获取代理的接口、方式都不同，需要根据不同情况进行修改。

代码如下：

```python
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random
import telnetlib

import requests
from scrapy import signals


class WeiboAnimalcrossingSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WeiboAnimalcrossingDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CookiesMiddleware():
    def __init__(self, cookies_url):
        self.logger = logging.getLogger(__name__)
        self.cookies_url = cookies_url

    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_url)
            if response.status_code == 200:
                cookies = json.loads(response.text)
                return cookies
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        self.logger.debug('正在获取cookies')
        cookies = self.get_random_cookies()
        if cookies:
            request.cookies = cookies
            self.logger.debug('使用cookies' + json.dumps(cookies))

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(cookies_url=settings.get('COOKIES_URL'))


class ProxyMiddleware():
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            proxy_list = []
            data_list = json.load(open('proxy.json')).get('data')
            for p in data_list:
                proxy_ip = p.get('ip')
                proxy_port = p.get('port')
                proxy = str(proxy_ip) + ':' + str(proxy_port)
                '''
                #   测试代理是否可用,因为每次都会调用很浪费时间，待优化。
                try:
                    requests.get('https://m.weibo.cn', proxies={'https': 'https://'+proxy})
                    proxy_list.append(proxy)
                except:
                    continue
                '''
                proxy_list.append(proxy)
            try:
                proxy = proxy_list[random.randint(0, len(proxy_list))]
                return proxy
            except:
                return False
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        #if request.meta.get('retry_times'):
        proxy = self.get_random_proxy()
        if proxy:
            uri = 'https://{proxy}'.format(proxy=proxy)
            self.logger.debug('使用代理' + proxy)
            request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )
```

# **启用设置,修改settings**

启用pipelines和middlewares。设置MongoDB数据集参数。

代码如下：

```python
# -*- coding: utf-8 -*-

# Scrapy settings for weibo_animalcrossing project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weibo_animalcrossing'

SPIDER_MODULES = ['weibo_animalcrossing.spiders']
NEWSPIDER_MODULE = 'weibo_animalcrossing.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'weibo_animalcrossing (+http://www.yourdomain.com)'

# Obey robots.txt rules\
#ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

DEFAULT_REQUEST_HEADERS = {
    'Host': 'm.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
   }

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'weibo_animalcrossing.middlewares.WeiboAnimalcrossingSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'weibo_animalcrossing.middlewares.CookiesMiddleware': 80,
    'weibo_animalcrossing.middlewares.ProxyMiddleware': 90,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'weibo_animalcrossing.pipelines.WeiboPipeline': 300,
    'weibo_animalcrossing.pipelines.CsvPipeline': 301,
    'weibo_animalcrossing.pipelines.MongoPipeline': 302,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MONGO_URI = 'localhost'

MONGO_DATABASE = 'weibo'

COOKIES_URL = 'http://localhost:5000/weibo/random'

RETRY_ENABLED: True

RETRY_HTTP_CODES = [301, 401, 403, 408, 414, 500, 502, 503, 504]

RETRY_TIMES = 10
```

# **运行scrapy项目**

`scrapy crawl weibomember`

运行一段时间后可在MongoDB和weibo.csv查看爬取的数据。

![scrapyweibo4.png](https://kameee.top/upload/2020/04/scrapy-weibo-4-6c1f2e525aa547b19564526d320d520b.png)

![scrapyweibo5.png](https://kameee.top/upload/2020/04/scrapy-weibo-5-60452ffb753943cda873231a56f68628.png)

