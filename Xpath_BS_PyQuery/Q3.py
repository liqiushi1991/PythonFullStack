import os, time
import requests
from urllib.request import urlretrieve
import json

def baidu_image(page):
    url='https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E8%A1%97%E6%8B' \
        '%8D&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E8%A1%97%E6%8B%8D&s=&se=&tab=&width=&height=&face=0&' \
        'istype=2&qc=&nc=1&fr=&pn={}&rn=5&gsm=14a&1536460636398='.format(page)
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'BDqhfp=%E8%A1%97%E6%8B%8D%26%260-10-1undefined%26%260%26%261; BAIDUID=C30E8BB58FE2AF3489BC0D03E1AFF088:FG=1; BIDUPSID=C30E8BB58FE2AF3489BC0D03E1AFF088; PSTM=1518371494; BDUSS=pQcmJvcHBkVmRNd1NnTUIwTzNKZ0lXRlYtRks5WklPOEViWjVTV3RsbklEOEphQVFBQUFBJCQAAAAAAAAAAAEAAAB8AqMbz-jKtbXEz8m61wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMiCmlrIgppaeF; __cfduid=d772fdac4d4dd489a0417aefee85588bd1522523584; pgv_pvi=2451620864; locale=zh; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=7; H_PS_PSSID=26522_1454_21081_26350_20929; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; firstShowTip=1; indexPageSugList=%5B%22%E8%A1%97%E6%8B%8D%22%5D; cleanHistoryStatus=0',
        'Host': 'image.baidu.com',
        'Referer': 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E8%A1%97%E6%8B%8D&oq=%E8%A1%97%E6%8B%8D&rsp=-1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',

    }

    request = requests.get(url=url, headers=headers)

    data = json.loads(request.content.decode('utf-8'))['data']

    print(len(data))
    for item in data:
        try:
            yield{
                'image': item['middleURL'],
                'title': item['fromPageTitleEnc']
            }
        except Exception as err:
            print(err)
            yield None


def saveImage(item):
    '''储存图片'''
    # 处理每组图片的存储路径
    if item is not None:
        path = os.path.join("./mypic")
        if not os.path.exists(path):
            os.mkdir(path)

        # 拼装原图和目标图片的路径即名称
        local_image_url = item.get('image')
        image_url = local_image_url
        save_pic = path+"/"+item.get('title')+".jpg"

        # 使用urllib中urlretrieve直接存储图片
        # 如果已经下载过即不保存
        if item.get('title')+".jpg" not in os.listdir():
            try:
                urlretrieve(image_url, save_pic)
                return True
            except Exception as err:
                print(err)
                return False
    return True


def main(offset):
    ''' 主程序函数，负责调度执行爬虫处理 '''
    json = baidu_image(offset)
    for item in json:
        print(item)
        # 由于网络阻塞，反复下载直到成功为止
        while not saveImage(item):
            print(item)
        time.sleep(0.5)


if __name__ == '__main__':
    for i in range(5, 300, 5):
        main(i)
