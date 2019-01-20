# -*- coding: utf-8 -*
__author__ = 'double k'

from controller.finance.finance import GetList
from controller.finance.stock import GetList as GetStockList
from controller.finance.money import GetList as GetMoneyList
from controller.finance.metal import GetList as GetMetalList
from controller.finance.share import GetList as GetShareList
# from controller.game.download import GetDetail as GetDownLoadDetail

import time
from ownModule import overTimeHandle
from threading import Thread
def financeThread():
    time.sleep(2)
    # 获取金融
    finance = GetList("http://finance.jrj.com.cn/list/cjgundong.shtml", 5, 'http://finance.jrj.com.cn/list/')
    finance.main()
    # listInfo = {'title': '李开复：机器或不会像人一样思考 相信人类灵魂神圣性', 'detail-href': 'http://finance.jrj.com.cn/2019/01/14154626901707.shtml', 'thumb-img': ''}
    # detail = GetDetail(listInfo['detail-href'], 5, listInfo)
    # detail.getHtml()

def stockThread():
    time.sleep(2)
    # 获取个股
    stock = GetStockList("http://stock.jrj.com.cn/list/stockgszx.shtml", 5, 'http://stock.jrj.com.cn/list/')
    stock.main()
    # listInfo = {'title': '李开复：机器或不会像人一样思考 相信人类灵魂神圣性', 'detail-href': 'http://finance.jrj.com.cn/2019/01/14154626901707.shtml', 'thumb-img': ''}
    # detail = GetStockDetail(listInfo['detail-href'], 5, listInfo)
    # detail.getHtml()
def moneyThread():
    time.sleep(2)
    # 获取理财
    stock = GetMoneyList("http://money.jrj.com.cn/list/moneygdxw2017.shtml", 5, 'http://money.jrj.com.cn/list/')
    stock.main()
    # listInfo = {'title': '李开复：机器或不会像人一样思考 相信人类灵魂神圣性', 'detail-href': 'http://finance.jrj.com.cn/2019/01/14154626901707.shtml', 'thumb-img': ''}
    # detail = GetMoneyDetail(listInfo['detail-href'], 5, listInfo)
    # detail.getHtml()

def metalThread():
    time.sleep(2)
    # 获取贵金属
    stock = GetMetalList("http://gold.jrj.com.cn/list/sckx.shtml", 5, 'http://gold.jrj.com.cn/list/')
    stock.main()
    # listInfo = {'title': '李开复：机器或不会像人一样思考 相信人类灵魂神圣性', 'detail-href': 'http://finance.jrj.com.cn/2019/01/14154626901707.shtml', 'thumb-img': ''}
    # detail = GetMoneyDetail(listInfo['detail-href'], 5, listInfo)
    # detail.getHtml()

def shareThread():
    time.sleep(2)
    # 获取个股
    stock = GetShareList("http://stock.jrj.com/list/stockssgs.shtml", 5, 'http://stock.jrj.com/list/')
    stock.main()
    # listInfo = {'title': '李开复：机器或不会像人一样思考 相信人类灵魂神圣性', 'detail-href': 'http://finance.jrj.com.cn/2019/01/14154626901707.shtml', 'thumb-img': ''}
    # detail = GetMoneyDetail(listInfo['detail-href'], 5, listInfo)
    # detail.getHtml()
def worke(className):
    # if className == "finance":
    #     financeThread()
    # if className == "stock":
    #     stockThread()
    # if className == "money":
    #     moneyThread()
    # if className == "metal":
    #     metalThread()
    if className == "share":
        shareThread()

code = overTimeHandle.main(False, objectName="jinrong")
if code != 100200:
    threads = ["finance", 'stock', 'money', 'metal', 'share']
    #  开启线程
    thres = [Thread(target=worke, args=(t,))
                for t in threads]
    # 开始执行线程
    [thr.start() for thr in thres]
    # 等待线程执行结束
    [thr.join() for thr in thres]
