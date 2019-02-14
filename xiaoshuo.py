# -*- coding: utf-8 -*
__author__ = 'double k'

# from controller.picture.text import GetDetail
from controller.xiaoshuo.book import GetList
import time
from ownModule import overTimeHandle
from threading import Thread
def worke(url):
    time.sleep(1)
    # 获取图片文章信息
    book = GetList(url, 5, '')
    book.main()
    # listInfo = {
    #     'title': '曾沛慈自爆被示爱会上厕所 男友顿感超尴尬',
    #     'detail-href': 'http://www.mmonly.cc/tstx/ylxw/189696.html',
    #     'thumb-img': 'http://t1.hxzdhn.com/uploads/tu/201709/9999/rndcca0d812c.jpg'
    # }
    # detail = GetDetail("http://www.mmonly.cc/tstx/ylxw/189696.html", 1, listInfo)
    # detail.getHtml()
code = overTimeHandle.main(True, "xiaoshuo", 2019, 2, 1, 40)
if code != 100200:
    navs =[
        # 玄幻
        'https://www.qidian.com/all?chanId=21&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0',
        # 武侠，
        'https://www.qidian.com/all?chanId=2&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0',
        # 军事，'
        'https://www.qidian.com/all?chanId=6&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0',
        # 都市，
        'https://www.qidian.com/all?chanId=4&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0',
        # 游戏，
        'https://www.qidian.com/all?chanId=7&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0',
        # 科幻，
        'https://www.qidian.com/all?chanId=9&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0',
        # 现实，
        'https://www.qidian.com/all?chanId=15&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0',
        # 历史，
        'https://www.qidian.com/all?chanId=5&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0',
        # 体育，
        'https://www.qidian.com/all?chanId=8&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0'
        # 灵异，
        'https://www.qidian.com/all?chanId=10&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0',
        # 二次元
        'https://www.qidian.com/all?chanId=12&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0'
    ]
    #  开启线程
    thres = [Thread(target=worke, args=(nav,))
                for nav in navs]
    # 开始执行线程
    [thr.start() for thr in thres]
    # 等待线程执行结束
    [thr.join() for thr in thres]
    # worke('http://mmonly.cc/tstx/ylxw/')
















