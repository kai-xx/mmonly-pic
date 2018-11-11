# -*- coding: utf-8 -*
__author__ = 'double k'

from controller.picture.text import GetDetail
from controller.picture.text import GetList
import time
from ownModule import overTimeHandle
from threading import Thread
def worke(url):
    time.sleep(1)
    # 获取图片文章信息
    # pic = GetList(url, 1, url)
    # pic.main()
    listInfo = {
        'title': '曾沛慈自爆被示爱会上厕所 男友顿感超尴尬',
        'detail-href': 'http://www.mmonly.cc/tstx/ylxw/189696.html',
        'thumb-img': 'http://t1.hxzdhn.com/uploads/tu/201709/9999/rndcca0d812c.jpg'
    }
    detail = GetDetail("http://www.mmonly.cc/tstx/ylxw/189696.html", 1, listInfo)
    detail.getHtml()
code = overTimeHandle.main()
if code != 100200:
    # navs =[
    #     'http://www.mmonly.cc/tstx/ylxw/',
    #     'http://www.mmonly.cc/tstx/shbt/',
    #     'http://www.mmonly.cc/tstx/qwys/',
    #     'http://www.mmonly.cc/tstx/dyyp/'
    # ]
    # #  开启线程
    # thres = [Thread(target=worke, args=(nav,))
    #             for nav in navs]
    # # 开始执行线程
    # [thr.start() for thr in thres]
    # # 等待线程执行结束
    # [thr.join() for thr in thres]
    worke('http://mmonly.cc/tstx/ylxw/')
















