# -*- coding: utf-8 -*
__author__ = 'double k'

from controller.game.news import GetDetail
from controller.game.news import GetList
# 获取新闻资讯
# news = GetList("http://www.ali213.net/news/game/", 5)
# news.main()
# listInfo = {'title': '言之游理：这些成就令人难忘或抓狂…你达成过吗？', 'detail-href': 'http://www.ali213.net/news/html/2018-11/390787.html', 'thumb-img': 'http://imgs.ali213.net/news/2018/11/05/2018110553803828.jpg'}
listInfo = {'title': '言之游理：这些成就令人难忘或抓狂…你达成过吗？', 'detail-href': 'http://www.ali213.net/news/html/2018-11/391409.html', 'thumb-img': 'http://imgs.ali213.net/news/2018/11/05/2018110553803828.jpg'}

detail = GetDetail("http://www.ali213.net/news/html/2018-11/391409.html", 5, listInfo)
detail.getHtml()