import urllib
from bs4 import BeautifulSoup as bs
from pyquery import PyQuery as py
from lxml import etree
import json
import time


def get_page(url):
    try:
        header = {
            'User-Agent': 'User-Agent:Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1'
        }

        request = urllib.request.Request(url=url, method='GET', headers=header)
        response = urllib.request.urlopen(request)
        return response.read().decode('utf-8')

    except Exception as err:
        print(err)


def parse_page_pyquery(content):
    print('pyquery')
    doc = py(content)
    for item in doc('tr.item').items():
        yield {
            'title': item.find('p.pl').text(),
            'decription': item.find('div.pl2 a').text(),
            'rating': item.find('.rating_nums').text(),
            'counts': item.find('div.star.clearfix span.pl').text(),
            'quotes': item.find('p.quote span.inq').text(),
            'image_url': item.find('a.nbg img').attr('src')
        }


def parse_page_xpath(content):
    print('xpath')
    items = etree.HTML(content).xpath('//tr[@class="item"]')
    for item in items:
        try:
            yield {
                'title': item.xpath('.//p[@class="pl"]/text()')[0],
                'decription': item.xpath('.//div[@class="pl2"]/a/text()')[0],
                'rating': item.xpath('.//span[@class="rating_nums"]/text()')[0],
                'counts': item.xpath('.//div[@class="star clearfix"]/span[@class="pl"]/text()')[0],
                'quotes': item.xpath('.//p[@class="quote"]/span[@class="inq"]/text()')[0],
                'image_url': item.xpath('.//a[@class="nbg"]/img/@src')[0]
            }

        except Exception as err:
            print(err)

            yield
            {
                'title': item.xpath('.//p[@class="pl"]/text()')[0],
                'decription': item.xpath('.//div[@class="pl2"]/a/text()')[0],
                'rating': item.xpath('.//span[@class="rating_nums"]/text()')[0],
                'counts': item.xpath('.//div[@class="star clearfix"]/span[@class="pl"]/text()')[0],
                'quotes': '',
                'image_url': item.xpath('.//a[@class="nbg"]/img/@src')[0]
            }


def parse_page_bs(content):
    print('beautiful soup')
    soup = bs(content, 'lxml')
    items = soup.find_all(name='tr', attrs={"class": "item"})

    for item in items:
        try:
            yield {
                'title': item.find(name='p', attrs={'class': 'pl'}).string,
                'decription': item.select('div.pl2 a')[0].string,
                'rating': item.find(name='span', attrs={'class': 'rating_nums'}).string,
                'counts': item.select('div.star.clearfix span.pl')[0].string,
                'quotes': item.select('p.quote span.inq')[0].string,
                'image_url': item.select('a.nbg img')[0].attrs['src']
            }
        except Exception as err:
            print(err)
            yield {
                'title': item.find(name='p', attrs={'class': 'pl'}).string,
                'decription': item.select('div.pl2 a')[0].string,
                'rating': item.find(name='span', attrs={'class': 'rating_nums'}).string,
                'counts': item.select('div.star.clearfix span.pl')[0].string,
                'quotes': '',
                'image_url': item.select('a.nbg img')[0].attrs['src']
            }


def write_to_file(content, name):
    with open("./result_%s.txt" % name, 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'https://book.douban.com/top250?start=' + str(offset)
    content = get_page(url)

    # pyquery
    start_t = time.time()
    for item in parse_page_pyquery(content):
        write_to_file(item, 'pyquery')
    t1 = time.time() - start_t

    # xpath
    start_t = time.time()
    for item in parse_page_xpath(content):
        write_to_file(item, 'xpath')
    t2 = time.time() - start_t

    # beautiful soup
    start_t = time.time()
    for item in parse_page_bs(content):
        write_to_file(item, 'beautiful_soup')
    t3 = time.time() - start_t
    return t1, t2, t3


if __name__ == '__main__':
    t1, t2, t3 = 0, 0, 0
    for i in range(0, 100, 25):
        print(i)
        tt1, tt2, tt3 = main(i)
        t1 += tt1
        t2 += tt2
        t3 += tt3

    print('pyquery run ', t1, ' xpath run ', t2, ' beautiful soup run ', t3)