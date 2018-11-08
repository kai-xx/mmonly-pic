# -*- coding: utf-8 -*
__author__ = 'double k'

from controller.game.news import GetDetail
from controller.game.news import GetList
from controller.game.download import GetList as GetDownLoadList
from controller.game.download import GetDetail as GetDownLoadDetail
from controller.game.patch import GetList as GetPatchList
from controller.game.patch import GetDetail as GetPatchDetail
from controller.game.qqvs import GetList as GetQqvsList
from controller.game.qqvs import GetDetail as GetQqvsDetail
from controller.game.vrNews1 import GetList as GetVrNews1List
from controller.game.vrNews1 import GetDetail as GetVrNews1Detail
from controller.game.vrNews2 import GetList as GetvrNews2List
from controller.game.vrNews2 import GetDetail as GetvrNews2Detail
from controller.game.mgame import GetList as GetmgameList
from controller.game.mgame import GetDetail as GetmgameDetail
from controller.game.ids import GetList as GetidsList
from controller.game.ids import GetDetail as GetidsDetail
import time
from ownModule import overTimeHandle
from threading import Thread

def newsThread():
    time.sleep(2)
    # 获取新闻资讯
    news = GetList("http://www.ali213.net/news/game/", 5)
    news.main()
    # listInfo = {'title': '言之游理：这些成就令人难忘或抓狂…你达成过吗？', 'detail-href': 'http://www.ali213.net/news/html/2018-11/390787.html', 'thumb-img': 'http://imgs.ali213.net/news/2018/11/05/2018110553803828.jpg'}
    # listInfo = {'title': '言之游理：这些成就令人难忘或抓狂…你达成过吗？', 'detail-href': 'http://www.ali213.net/news/html/2018-11/391409.html', 'thumb-img': 'http://imgs.ali213.net/news/2018/11/05/2018110553803828.jpg'}
    # detail = GetDetail("http://www.ali213.net/news/html/2018-11/391409.html", 5, listInfo)
    # detail.getHtml()
def downThread():
    time.sleep(2)
    # 获取下载信息
    download = GetDownLoadList("http://down.ali213.net/pcgame/", 5)
    download.main()
    # imges =['http://game-ali.com/uploads/allimg/20181106/20181106153306927_2018051712548124.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153307e711d28c-5138-4385-0ac1-fc6e8c63c6a0.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153307927_201805171255157.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153308927_2018051712553935.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153308927_2018051712556140.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153309927_2018051712558812.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153309927_2018051712601336.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153310927_2018051712603145.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153310927_2018051712605553.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311120X90_2018051712548124.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311fe956cbf-2da0-27de-57cd-45dfa289fc4e.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311120X90_201805171255157.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311120X90_2018051712553935.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311120X90_2018051712556140.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311120X90_2018051712558812.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311120X90_2018051712601336.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153312120X90_2018051712603145.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153312120X90_2018051712605553.jpg']

    # downloadListInfo ={'title': '黑色五叶草：四重奏骑士', 'detail-href': 'http://down.ali213.net/pcgame/blackcloverquartetknights.html', 'thumb-img': 'http://imgs.ali213.net/oday/uploadfile/2017/12/06/2017120693843591.jpg'}
    #
    # downloadDetail = GetDownLoadDetail("http://down.ali213.net/pcgame/blackcloverquartetknights.html", 5, downloadListInfo)
    # downloadDetail.getHtml()
    # print(downloadDetail.addPic(imges))

def patchThread():
    time.sleep(2)
    # 获取补丁信息
    patch = GetPatchList("http://patch.ali213.net/showclass/class_top200_1.html", 5)
    patch.main()
    # patchListInfo = {'title': '无双大蛇3（Musou Orochi 3）吕布神格化常驻MOD', 'detail-href': 'http://patch.ali213.net/showpatch/104283.html', 'thumb-img': ''}
    #
    # patchDetail = GetPatchDetail("http://patch.ali213.net/showpatch/104283.html", 5, patchListInfo)
    # patchDetail.getHtml()

def qqvsThread():
    time.sleep(2)
    # 获取攻略信息
    qqvs = GetQqvsList("http://gl.ali213.net/new/", 5)
    qqvs.main()
    # qqvsListInfo = {'title': '《香港之战》配置要求高吗？最低配置要求介绍', 'detail-href': 'http://gl.ali213.net/html/2018-11/278831.html', 'thumb-img': 'http://img1.ali213.net/glpic/2018/11/07/2018110715148691.jpg', 'intro': '新作是一款快节奏的俯视射击游戏，预计将上架steam，发售日期还没公布，这里给大家带来了香港之战最低配置要求介绍，详情一起看下文中介绍吧。'}
    # qqvsDetail = GetQqvsDetail("http://gl.ali213.net/html/2018-11/278831.html", 5, qqvsListInfo)
    # qqvsDetail.getHtml()
def vr1Thread():
    time.sleep(2)
    # 获取VR信息1
    vr1 = GetVrNews1List("http://www.ali213.net/vr/news", 5)
    vr1.main()
    # vr1ListInfo = {'title': '全球首部VR叙事长片《Calling》首映 大朋VR提供VR观影解决方案', 'detail-href': 'http://www.ali213.net/news/html/2018-11/391451.html', 'thumb-img': 'http://imgs.ali213.net/news/2018/11/05/2018110550714221.jpg'}
    # vr1Detail = GetVrNews1Detail("http://www.ali213.net/news/html/2018-11/391451.html", 5, vr1ListInfo)
    # vr1Detail.getHtml()

def vr2Thread():
    time.sleep(2)
    # 获取VR信息2
    vr2 = GetvrNews2List("http://www.ali213.net/vr/pingce/", 5)
    vr2.main()
    # vr2ListInfo = {'title': '大朋VR全景声巨幕VR影院值不值购买?详细体验总结', 'detail-href': 'http://www.ali213.net/news/html/2018-9/383729.html', 'thumb-img': 'http://imgs.ali213.net/news/2018/09/21/20180921103816171.jpg'}
    # vr2Detail = GetvrNews2Detail("http://www.ali213.net/news/html/2018-9/383729.html", 5, vr2ListInfo)
    # vr2Detail.getHtml()

def mgameThread():
    time.sleep(2)
    # 获取手机端游戏信息
    mgame = GetmgameList("http://m.ali213.net/news/", 5)
    mgame.main()
    # mgameListInfo = {'title': '《阴阳师》入殓师一反木棉双退治活动开启 体验服11月7日更新内容', 'detail-href': 'http://m.ali213.net/news/181107/116583.html', 'thumb-img': 'http://img1.ali213.net/shouyou/article/0/116583.jpg'}
    # mgameDetail = GetmgameDetail("http://m.ali213.net/news/181107/116583.html", 5, mgameListInfo)
    # mgameDetail.getHtml()


def idsThread():
    time.sleep(2)
    # 获取游戏硬件信息信息
    ids = GetidsList("http://in.ali213.net/news/", 5)
    ids.main()
    # idsListInfo =  {'title': '64核心128线程!AMD官宣全球首款7nm工艺霄龙处理器', 'detail-href': 'http://in.ali213.net/news/201811/5910.html', 'thumb-img': 'http://img2.ali213.net/hardware/news/2018/11/07/2018110744208761.jpg', 'intro': '11月7日凌晨，AMD在美国旧金山召开主题为Next Horizon的主题会议，全面披露了下一代7n…'}
    # idsDetail = GetidsDetail("http://in.ali213.net/news/201811/5910.html", 5, idsListInfo)
    # idsDetail.getHtml()
def worke(className):
    if className == "news":
        newsThread()
    elif className == "down":
        downThread()
    elif className == "patch":
        patchThread()
    elif className == "qqvs":
        qqvsThread()
    elif className == "vr1":
        vr1Thread()
    elif className == "vr2":
        vr2Thread()
    elif className == "mgame":
        mgameThread()
    elif className == "ids":
        idsThread()

code = overTimeHandle.main(True, objectName="gameali")
if code != 100200:
    threads = ["news", "down", "patch", "qqvs", "vr1", "vr2", "mgame", "ids"]
    #  开启线程
    thres = [Thread(target=worke, args=(t,))
                for t in threads]
    # 开始执行线程
    [thr.start() for thr in thres]
    # 等待线程执行结束
    [thr.join() for thr in thres]
