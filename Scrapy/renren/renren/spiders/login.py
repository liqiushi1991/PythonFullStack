# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['www.renren.com']
    start_urls = ['http://zhibo.renren.com/top']

    post_headers = {}
    post_headers['Accept'] = '*/*'
    post_headers['Accept - Language'] = 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    post_headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

    def start_requests(self):
        return [FormRequest(url='http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=2018861044434',
                                          headers=self.post_headers,
                                          formdata={
                                              'email': '443493878@qq.com',
                                              'password': '06e3a759d7c8e1fa49d82532d195b2877db96b3eaaf044dc64127b8d4ae56196',
                                              'origURL': 'http://www.renren.com/home',
                                              'domain': 'renren.com',
                                              'key_id': '1',
                                              'captcha_type': 'web_login',
                                              'rkey': '5e164456e3500a73a245eae0a6da18e6',
                                              'f': 'http%3A%2F%2Fzhibo.renren.com%2Ftop'
                                          },
                                          callback=self.parse)]

    def parse(self, response):
        print('=='*100)
        print(response.status)
        print(response.css('title::text').extract())
        yield Request('http://www.renren.com/home', callback=self.parse_page)

    def parse_page(self, response):
        print('*='*100)
        print(response.status)
        print(response.css('title::text').extract())
        pass