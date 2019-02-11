# -*- coding: utf-8 -*
__author__ = 'double k'
from ownModule.mysql import MySQLSingle
import requests
class CreateData:
    def __init__(self, databaseName=None, prefix=""):
        self.db = MySQLSingle()
        self.db.get_conn(databaseName)
        self.prefix = prefix
    def checkBook(self, bookName, author):
        sql = "select bid from " + self.prefix +"story_books where bookname='%s' and author='%s'" % (bookName, author)
        bookInfo = self.db.getone(sql)
        if bookInfo:
            print("小说--", bookName, "作者--", author, "--已经存在，小说ID为：", bookInfo['bid'])
            return bookInfo['bid']
        else:
            return None

    def checkClassify(self, name):
        sql = "select * from " + self.prefix +"story_catalog where classname='%s'" % (name, )
        classifyInfo = self.db.getone(sql)
        if classifyInfo:
            print("栏目--", name, "--已经存在，栏目ID为：", classifyInfo['id'])
            return classifyInfo['id']
        else:
            return None

    def checkChapter(self, bookId, chaptername):
        sql = "SELECT id,chapnum,chaptername FROM " + self.prefix +"story_chapter WHERE bookid=%d and chaptername='%s' ORDER BY chapnum DESC" % (bookId, chaptername)
        chapterInfo = self.db.getone(sql)
        if chapterInfo:
            print("小说ID为--", bookId,"章节名称为--", chaptername, "--已经存在，栏目ID为：", chapterInfo['id'])
            return chapterInfo['id']
        else:
            return None

    def checkContent(self, bookId, title):
        sql = "select * from " + self.prefix +"story_content WHERE bookid=%d and title='%s'" % (bookId, title)
        contentInfo = self.db.getone(sql)
        if contentInfo:
            print("小说ID为--", bookId, "章节名称为--", title, "--已经存在，栏目ID为：", contentInfo['id'])
            return contentInfo['id']
        else:
            return None
    def getHost(self):
        sql = "select * from  " + self.prefix + "sysconfig where varname='cfg_basehost'"
        config = self.db.getone(sql)
        if config:
            host = config['value']
        else:
            host = "http://127.0.0.1"
        return host
    def insertClassify(self, list):
        url = self.getHost() + '/xs/spider_story_catalog.php'
        payload = {
            'action': 'add',
            'classname': list['classname'],
            'pid': list['pid'],
            'rank': 0,
            'booktype': 0,
            'keywords': list['classname'],
            'description': list['classname'],
            'Submit': '增加栏目'
        }
        r = requests.get(url, params=payload)
        return r.json()['id']
    def insertBook(self, list):
        url = self.getHost() + '/xs/spider_story_add_action.php'
        payload = {
            'catid': list['catid'],
            'bookname': list['bookname'],
            'freenum': -1,
            'arcrank': 0,
            'litpicname': self.getThumbImage(list['imageInfo'], list['thumbInfo']),
            'author': list['author'],
            'pubdate': list['pubdate'],
            'click': 0,
            'keywords': list['keywords'],
            'description': list['description'],
            'body': list['body'],
            'Submit': '保 存'
        }
        r = requests.post(url, data=payload)
        return r.json()['id']
    def inserChapter(self, list):
        url = self.getHost() + '/xs/spider_story_add_content_action.php'
        payload = {
            'booktype': 0,
            'Submit': '保 存'
        }
        payload = dict(list, **payload)
        r = requests.post(url, data=payload)
        return r.json()['id']
    def updateBookStars(self, bid, totalvalue):
        sql = 'UPDATE xs_story_bookstars SET totalvalue=%d,totalvotes=1 WHERE bid=%d' %(totalvalue, bid)
        result = self.db.save(sql, bid)
        if result:
            print("小说ID为--", bid, "评分更新成功")
            return result
        else:
            return None
    def getThumbImage(self, imageInfo, thumbInfo):
        thumb = ""
        if len(thumbInfo) > 0:
            if 'path' in thumbInfo[0]:
                thumb = thumbInfo[0]['path']

        if not thumb:
            for image in imageInfo:
                if 'path' in image:
                    thumb = image['path']
                    break

        return thumb

