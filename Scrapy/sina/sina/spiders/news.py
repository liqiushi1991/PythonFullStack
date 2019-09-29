# -*- coding: utf-8 -*-
import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide']

    def parse(self, response):
        durls = response.css('div.section')

        for durl in durls:
            print('.'.join(durl.css('h2.tit01::text').extract()))

            url = durl.css('div.clearfix')

            for ur in url:
                print(''.join(ur.css('h3.tit02::text, h3.tit02 a::text, h3.tit02 span::text').extract()))

                for u in ur.css('ul'):
                    print('|'.join(u.css('li a::text').extract()))

                print()
                print('-'*20)

            print()
            print('=='*40)
        pass
