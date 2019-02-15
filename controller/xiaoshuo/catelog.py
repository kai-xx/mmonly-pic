# -*- coding: utf-8 -*
__author__ = 'double k'
"""
获取小说信息
https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=2
"""
from endpoint.bookCreateData import CreateData

class GetDetail:
    def getMainHtml(self):

        create = CreateData('xiaoshuo', "xs_")
        # 增加导航信息
        for categorys in self.cateList():
            for key in range(0, len(categorys)):
                if key == 0:
                    tdk = self.tdkList(categorys[key])
                    list1 = {
                        'classname': categorys[key],
                        'keywords': tdk['keyword'],
                        'description': tdk['description'],
                        'pid': 0,
                    }
                    print('开始写入一级栏目信息')
                    category1 = create.checkClassify(categorys[key])
                    if category1 == None:
                        category1 = create.insertClassify(list1)
                    else:
                        create.updateCate(category1, tdk['title'],  keyword=tdk['keyword'],description=tdk['description'])
                    print(category1)
                if key == 1:
                    tdk = self.tdkList(categorys[0])
                    list2 = {
                        'classname': categorys[key],
                        'keywords': tdk['keyword'],
                        'description': tdk['description'],
                        'pid': category1,
                    }
                    print('开始写入二级栏目信息')
                    category2 = create.checkClassify(categorys[key])
                    if category2 == None:
                        category2 = create.insertClassify(list2)
                    else:
                        create.updateCate(category2, tdk['title'], keyword=tdk['keyword'],description=tdk['description'])
    def tdkList(self, key):
        list = {
            "玄幻":{
                'title': '玄幻小说_玄幻小说推荐_玄幻小说排行榜_小说网',
                'keyword': '玄幻小说,玄幻小说推荐,玄幻小说排行榜',
                'description': '小说网玄幻小说栏目为您提供最新玄幻小说排行榜以及玄幻小说推荐，在这里您可以在线免费阅读完本的优质玄幻小说以及最新更新章节。更多玄幻小说尽在小说网。',
            },
            "武侠": {
                'title': '武侠小说_武侠小说推荐_武侠小说排行榜_小说网',
                'keyword': '武侠小说,武侠小说推荐,武侠小说排行榜',
                'description': '小说网武侠小说栏目为您提供最新武侠小说排行榜以及武侠小说推荐，在这里您可以在线免费阅读完本的优质武侠小说以及最新更新章节。更多武侠小说尽在小说网。',
            },
            "军事": {
                'title': '军事小说_军事小说推荐_军事小说排行榜_小说网',
                'keyword': '军事小说,军事小说推荐,军事小说排行榜',
                'description': '小说网军事小说栏目为您提供最新军事小说排行榜以及军事小说推荐，在这里您可以在线免费阅读完本的优质军事小说以及最新更新章节。更多军事小说尽在小说网。',
            },
            "都市": {
                'title': '都市小说_都市小说推荐_都市小说排行榜_小说网',
                'keyword': '都市小说,都市小说推荐,都市小说排行榜',
                'description': '小说网都市小说栏目为您提供最新都市小说排行榜以及都市小说推荐，在这里您可以在线免费阅读完本的优质都市小说以及最新更新章节。更多都市小说尽在小说网。',
            },
            "游戏": {
                'title': '游戏小说_游戏小说推荐_游戏小说排行榜_小说网',
                'keyword': '游戏小说,游戏小说推荐,游戏小说排行榜',
                'description': '小说网游戏小说栏目为您提供最新游戏小说排行榜以及游戏小说推荐，在这里您可以在线免费阅读完本的优质游戏小说以及最新更新章节。更多游戏小说尽在小说网。',
            },
            "科幻": {
                'title': '科幻小说_科幻小说推荐_科幻小说排行榜_小说网',
                'keyword': '科幻小说,科幻小说推荐,科幻小说排行榜',
                'description': '小说网科幻小说栏目为您提供最新科幻小说排行榜以及科幻小说推荐，在这里您可以在线免费阅读完本的优质科幻小说以及最新更新章节。更多科幻小说尽在小说网。',
            },
            "现实": {
                'title': '现实小说_现实小说推荐_现实小说排行榜_小说网',
                'keyword': '现实小说,现实小说推荐,现实小说排行榜',
                'description': '小说网现实小说栏目为您提供最新现实小说排行榜以及现实小说推荐，在这里您可以在线免费阅读完本的优质现实小说以及最新更新章节。更多现实小说尽在小说网。',
            },
            "历史": {
                'title': '历史小说_历史小说推荐_历史小说排行榜_小说网',
                'keyword': '历史小说,历史小说推荐,历史小说排行榜',
                'description': '小说网历史小说栏目为您提供最新历史小说排行榜以及历史小说推荐，在这里您可以在线免费阅读完本的优质历史小说以及最新更新章节。更多历史小说尽在小说网。',
            },
            "体育": {
                'title': '体育小说_体育小说推荐_体育小说排行榜_小说网',
                'keyword': '体育小说,体育小说推荐,体育小说排行榜',
                'description': '小说网体育小说栏目为您提供最新体育小说排行榜以及体育小说推荐，在这里您可以在线免费阅读完本的优质体育小说以及最新更新章节。更多体育小说尽在小说网。',
            },
            "悬疑灵异": {
                'title': '灵异小说_灵异小说推荐_灵异小说排行榜_小说网',
                'keyword': '灵异小说,灵异小说推荐,灵异小说排行榜',
                'description': '小说网灵异小说栏目为您提供最新灵异小说排行榜以及灵异小说推荐，在这里您可以在线免费阅读完本的优质灵异小说以及最新更新章节。更多灵异小说尽在小说网。',
            },
            "二次元": {
                'title': '二次元小说_二次元小说推荐_二次元小说排行榜_小说网',
                'keyword': '二次元小说,二次元小说推荐,二次元小说排行榜',
                'description': '小说网二次元小说栏目为您提供最新二次元小说排行榜以及二次元小说推荐，在这里您可以在线免费阅读完本的优质二次元小说以及最新更新章节。更多二次元小说尽在小说网。',
            }
        }
        return list[key]
    def cateList(self):
        list1 = [
                   ['玄幻', '东方玄幻'],
                   ['玄幻', '异世大陆'],
                   ['玄幻', '王朝争霸'],
                   ['玄幻', '高武世界'],

                   ['武侠', '传统武侠'],
                   ['武侠', '国术无双'],
                   ['武侠', '武侠幻想'],

                   ['军事', '军事战争'],
                   ['军事', '军旅生涯'],
                   ['军事', '抗战烽火'],
                   ['军事', '谍战特工'],
                   ['军事', '战争幻想'],

                   ['都市', '都市生活'],
                   ['都市', '爱情婚姻'],
                   ['都市', '异术超能'],
                   ['都市', '恩怨情仇'],
                   ['都市', '娱乐明星'],
                   ['都市', '青春校园'],

                   ['游戏', '游戏主播'],
                   ['游戏', '电子竞技'],
                   ['游戏', '虚拟网游'],
                   ['游戏', '游戏异界'],

                   ['科幻', '星际文明'],
                   ['科幻', '古武机甲'],
                   ['科幻', '时空穿梭'],
                   ['科幻', '超级科技'],
                   ['科幻', '进化变异'],
                   ['科幻', '末世危机'],
                   ['科幻', '未来世界'],

                   ['现实', '现实百态'],
                   ['现实', '爱情婚姻'],
                   ['现实', '社会乡土'],

                   ['历史', '架空历史'],
                   ['历史', '秦汉三国'],
                   ['历史', '两晋隋唐'],
                   ['历史', '两宋元明'],
                   ['历史', '清史民国'],
                   ['历史', '外国历史'],

                   ['体育', '篮球运动'],
                   ['体育', '足球运动'],
                   ['体育', '体育赛事'],

                   ['悬疑灵异', '悬疑侦探'],
                   ['悬疑灵异', '恐怖惊悚'],
                   ['悬疑灵异', '寻墓探险'],
                   ['悬疑灵异', '灵异鬼怪'],
                   ['悬疑灵异', '风水秘术'],

                   ['二次元', '原生幻想'],
                   ['二次元', '青春日常'],
                   ['二次元', '变身入替'],
                   ['二次元', '搞笑吐槽'],
                   ['二次元', '衍生同人']
               ]
        return list1


