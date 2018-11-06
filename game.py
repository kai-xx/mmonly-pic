# -*- coding: utf-8 -*
__author__ = 'double k'

from controller.game.news import GetDetail
from controller.game.news import GetList
from controller.game.download import GetList as GetDownLoadList
from controller.game.download import GetDetail as GetDownLoadDetail

from ownModule import overTimeHandle

overTimeHandle.main(True, objectName="gameali")
# 获取新闻资讯
# news = GetList("http://www.ali213.net/news/game/", 5)
# news.main()
# listInfo = {'title': '言之游理：这些成就令人难忘或抓狂…你达成过吗？', 'detail-href': 'http://www.ali213.net/news/html/2018-11/390787.html', 'thumb-img': 'http://imgs.ali213.net/news/2018/11/05/2018110553803828.jpg'}
# listInfo = {'title': '言之游理：这些成就令人难忘或抓狂…你达成过吗？', 'detail-href': 'http://www.ali213.net/news/html/2018-11/391409.html', 'thumb-img': 'http://imgs.ali213.net/news/2018/11/05/2018110553803828.jpg'}
# detail = GetDetail("http://www.ali213.net/news/html/2018-11/391409.html", 5, listInfo)
# detail.getHtml()

# 获取下载信息
download = GetDownLoadList("http://down.ali213.net/pcgame/", 5)
download.main()
# imges =['http://game-ali.com/uploads/allimg/20181106/20181106153306927_2018051712548124.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153307e711d28c-5138-4385-0ac1-fc6e8c63c6a0.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153307927_201805171255157.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153308927_2018051712553935.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153308927_2018051712556140.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153309927_2018051712558812.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153309927_2018051712601336.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153310927_2018051712603145.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153310927_2018051712605553.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311120X90_2018051712548124.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311fe956cbf-2da0-27de-57cd-45dfa289fc4e.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311120X90_201805171255157.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311120X90_2018051712553935.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311120X90_2018051712556140.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311120X90_2018051712558812.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153311120X90_2018051712601336.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153312120X90_2018051712603145.jpg','http://game-ali.com/uploads/allimg/20181106/20181106153312120X90_2018051712605553.jpg']

# downloadListInfo ={'title': '魔堡之主', 'detail-href': 'http://down.ali213.net/pcgame/machiavillain.html', 'thumb-img': 'http://imgs.ali213.net/oday/uploadfile/2018/05/17/201805171340914.jpg'}
# downloadDetail = GetDownLoadDetail("http://down.ali213.net/pcgame/machiavillain.html", 5, downloadListInfo)
# downloadDetail.getHtml()
# print(downloadDetail.addPic(imges))