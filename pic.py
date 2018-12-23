# -*- coding: utf-8 -*
__author__ = 'double k'

# from controller.picture.picture import GetDetail
from controller.picture.picture import GetList
import time
from ownModule import overTimeHandle
from threading import Thread
def worke(url):
    time.sleep(1)
    # 获取图片信息
    pic = GetList(url, 1, url)
    pic.main()
    # listInfo = {
    #     'title': '邻家极品漂亮幼妻大胆私房艳照酥胸性感深沟图片',
    #     'detail-href': 'http://www.mmonly.cc/mmtp/xgmn/281357.html',
    #     'thumb-img': 'http://t1.hxzdhn.com/uploads/tu/201811/10086/81aa4ec7ed.jpg'
    # }
    # detail = GetDetail("http://www.mmonly.cc/mmtp/xgmn/281357.html", 1, listInfo)
    # detail.getHtml()
navs =[
    {'category': '美女图片', 'href': 'http://mmonly.cc/mmtp/'},
    {'category': '帅哥图片', 'href': 'http://www.mmonly.cc/sgtp/'},
    {'category': '唯美图片', 'href': 'http://www.mmonly.cc/wmtp/'},
    {'category': '卡通漫画', 'href': 'http://www.mmonly.cc/ktmh/'},
    {'category': '搞笑图片', 'href': 'http://www.mmonly.cc/gxtp/'},
    {'category': '高清壁纸', 'href': 'http://www.mmonly.cc/gqbz/'},
]
#  开启线程
thres = [Thread(target=worke, args=(nav['href'],))
            for nav in navs]
# 开始执行线程
[thr.start() for thr in thres]
# 等待线程执行结束
[thr.join() for thr in thres]
# worke('http://mmonly.cc/mmtp/')
