import urllib
from pyquery import PyQuery as py

url = 'https://cart.jd.com/cart.action#none'


headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'Accept-Encoding: gzip, deflate, br
'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'user-key=fe3a107e-14ec-4040-895e-51ec415ab12a; cd=0; shshshfp=ff8f6fe1fe21e832c6282fe635fa8b9d; shshshfpa=6a620fb6-15b6-6487-25be-baaf96c141ea-1536455060; shshshfpb=04f84e982e7f1da5319769d4320b44bde9917ffdced25f7d15b9471956; __jda=122270672.15364550617311782657344.1536455062.1536455062.1536455062.1; __jdc=122270672; __jdv=122270672|direct|-|none|-|1536455061732; __jdu=15364550617311782657344; 3AB9D23F7A4B3C9B=ECPU5L4JJGLBV4P7QDVLOAEHPJRZKUMEPK24IF2SOV7CQH5OHIKEUWNI57OB3ZEUREHCQ4QJ34YFEABLFACUEPODNE; cart-main=xx; ipLoc-djd=1-72-2819; wlfstk_smdl=l69kfuqh3hclessm4bqep755voydw1kh; mt_xid=V2_52007VwMWUFpdVl4eThlaB2cDFFteX1ZcHUwcbAAyBEdaWw9SRk9LSlkZYlQTU0EIVl8XVRwIAGECFloOCFFZH3kaXQVuHxNaQVlaSx5BEl0BbAATYl9oUWocSB9UAGIzElRVUQ%3D%3D; cn=7; shshshsID=8b9bac675a5ac22ba1128f85f17c99be_4_1536455125814; __jdb=122270672.6.15364550617311782657344|1.1536455062',
'Host': 'cart.jd.com',
'Referer': 'https://cart.jd.com/cart.action',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

def cart():
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    doc = py(response.read().decode('utf-8'))

    items = doc('div.item-form').items()

    for item in items:
        yield {
            'title': item.find('div.item-msg').text(),
            'props-txt': item.find('div.props-txt').text(),
            'price': item.find('div.cell.p-price.p-price-new strong').text(),
            'sale': item.find('a.sales-promotion.ml5').text(),
            'promotion': item.find('ul li:eq(0)').text(),
            'weight': item.find('span.weight').attr('data'),
            'image': item.find('div.p-img a img').attr('src')
        }

for i in cart():
    print(i)
    print()