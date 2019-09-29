# -*- coding: utf-8 -*-
import scrapy
import re
from dangdang.items import DangdangItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['search.dangdang.com']
    start_urls = ['http://search.dangdang.com/?key=python&act=input&page_index=1']
    page = 1

    def parse(self, response):
        item = DangdangItem()
        book_list = response.css('ul.bigimg li')

        for book in book_list:
            item['title'] = book.css('p.name a::attr(title)').extract_first()  # title

            images_urls = book.css('img::attr(data-original)').extract_first()
            item['images_urls'] = [images_urls] if images_urls is not None else [] # imgurl
            item['images'] = item['title']  # imgurl
            item['detail'] = book.css('p.detail::text').extract_first()  # detail
            item['now_price'] = book.css('span.search_now_price::text').extract_first()  # now_price
            item['pre_price'] = book.css('span.search_pre_price::text').extract_first()  # pre_price
            item['comment_num'] = book.css('a.search_comment_num::text').extract_first()[:-3]  # comment_num
            item['publication'] = book.xpath(".//a[@dd_name='单品出版社']/text()").extract_first()  # publication

            pre_price = book.css('span.search_pre_price::text').extract_first()
            item['pre_price'] = None if pre_price is None else pre_price[1:]  # pre_price

            now_price = book.css('span.search_now_price::text').extract_first()
            item['now_price'] = None if now_price is None else now_price[1:]  # now_price

            discount = book.re('search_discount">.*?([\d.]*?)折')
            item['discount'] = discount[0] if len(discount) > 0 else None  # discount

            author = book.re('search_book_author"><span>.*?<a.*?title="(.*?)">')
            item['author'] = author[0] if len(author) > 0 else None # author

            date = book.re('<span> /(.*?)</span>')
            item['date'] = date[0] if len(date) > 0 else None  # date

            print(item['images_urls'],'[[[[[[[[[[[[[[')
            yield item
            print('=='*10)

        self.page += 1
        print(self.page)

        if len(book_list) > 0:
            yield scrapy.Request(url='&'.join(response.url.split('&')[:-1])+'&page_index='+str(self.page), callback=self.parse)
