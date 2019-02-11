# -*- coding: utf-8 -*
__author__ = 'double k'
"""
获取小说信息
https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=2
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import re
import datetime
import random
from bs4 import BeautifulSoup
from ownModule.down import DownLoadPicture
from ownModule.tool import Tool
from endpoint.bookCreateData import CreateData
from endpoint import getPageNumber
from ownModule.mysql import MySQLSingle
from endpoint.gameInnerChain import InnerChain
from endpoint import pseudoStatic
from ownModule.brower import Brower

class GetList:
    def __init__(self, baseUrl, waitTime, host):
        self.host = host
        self.baseUrl = baseUrl
        self.waitTime = waitTime
        self.brower = None
        self.html = None
        self.fatHtml = None
        self.count = 0
        self.wait = None
        self.isPaging = False

    def getHtml(self, url, page):
        print(url, "----", page)
        self.isPaging = True
        self.brower.get(url)
        self.wait = WebDriverWait(self.brower, self.waitTime)
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.all-book-list .book-img-text .all-img-list')))
        self.html = self.brower.page_source
        self.fatHtml = pq(self.html)
        items = self.fatHtml(".all-img-list").children().items()
        lists = []
        print("第", page, "页，开始获取数据")
        for item in items:
            if self.count > getPageNumber.getCount():
                print("本栏目已经获取", self.count, "条记录，目前允许最大获取数量为：", getPageNumber.getCount())
                exit()
            title = item(".book-mid-info").children().eq(0).children().text()
            author = item(".book-mid-info .author .name").eq(0).text()
            if not title:
                continue
            href = item(".book-mid-info").children().children().attr.href
            if not re.match("^http(s)?.*?", href):
                href = 'https:' + href
            detailHref = href

            imageSrc = item(".book-img-box").children().children().attr.src
            if not re.match('^http(s)?.*?', imageSrc):
                imageSrc = 'https:' + imageSrc
            thumbImg = re.sub('/150', '', imageSrc)
            intro = item(".book-mid-info .intro").text()
            list = {
                "title": title,
                "author": author,
                "detail-href": detailHref,
                "thumb-img": thumbImg,
                "intro": intro
            }
            lists.append(list)
            self.count += 1
            print("当前第", self.count, "获取的图文信息为：", list)
            try:
                create = CreateData('xiaoshuo', "xs_")
                if create.checkBook(title, author) == None:
                    print("小说名称为:", title, "作者为:", author, "数据不存在，开始获取详情")
                    detail = GetDetail(detailHref, self.waitTime, list)
                    detail.getHtml()
                else:
                    print("小说名称为:", title, "作者为:", author, "数据已经存在，跳过")
            except Exception as e:
                print("列表-页面抓取异常，没有返回信息，链接为：", self.baseUrl, "，错误信息为：", e)
                continue


    def waitForGetAllData(self):
        url = 'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page='
        page = 2
        if self.html == None:
            return
        if page > 55555:
            self.isPaging = False
            print("所有数据已经全部抓完，共抓取", self.count, "条数据")
        pageNum = 2
        if not pageNum:
            pageNum = 5
        while self.isPaging == True :
            if page > int(pageNum):
                return
            try:
                baseUrl = url + str(page)
                self.getHtml(baseUrl, page)
                page += 1
            except TimeoutException:
                self.isPaging = False
                print("所有数据已经全部抓完，共抓取", self.count, "条数据")

    def main(self):
        self.brower = Brower().exem()

        print("--------", "开始获取图文列表信息", "--------")
        self.getHtml(self.baseUrl, 1)
        self.waitForGetAllData()
        print("--------", "结束获取图文列表信息，共获取到", self.count, "条数据--------")
        self.brower.quit()


class GetDetail:
    def __init__(self, baseUrl, waitTime, listInfo):
        self.brower = None
        self.listInfo = listInfo
        self.baseUrl = baseUrl
        self.waitTime = waitTime
        self.html = None
        self.wait = None
        self.count = 0
    def getHtml(self):
        print('开始抓取小说信息，URL为：', self.baseUrl)
        brower = Brower().exem()
        brower.get(self.baseUrl)
        wait = WebDriverWait(brower, self.waitTime)
        try:
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.catalog-content-wrap .volume-wrap')))
            html = brower.page_source
            fatHtml = pq(html)
            items = fatHtml('#j-catalogWrap .volume-wrap .volume .cf').children().items()
            score = fatHtml('#score1').text()
            if not score:
                score = random.randint(6, 9)
            print('开始循环获取小说章节信息')
            book = None
            category = None
            chapter = None
            i = 0
            for item in items:
                url = item.children().attr.href
                if not re.match("^http(s)?.*?", url):
                    url = 'https:' + url
                title = re.sub('\ue63c', '', item.children().text())
                print({
                    'url': url,
                    'title': title
                })
                if i == 0:
                    print('首次写入小说以及小说章节信息')
                    book, category, chapter = self.getMainHtml(url, score)
                else:
                    print('写入小说小说章节信息')
                    self.getNextHtml(url, book, category, chapter)
                i += 1
            brower.quit()
        except Exception as e:
            print("小说-页面抓取异常，没有返回信息，链接为：", self.baseUrl, "，错误信息为：", e)
    def getMainHtml(self, url, score):
        print('开始首次写入小说以及小说章节信息')
        brower = Brower().exem()
        brower.get(url)
        html = brower.page_source
        fatHtml = pq(html)

        tool = Tool()
        socp = BeautifulSoup(html, "lxml")
        keywordsEle = socp.select('meta[name=keywords]')
        descriptionEle = socp.select('meta[name=description]')
        keywords = keywordsEle[0].get("content") if len(keywordsEle) > 0 else ""
        description = descriptionEle[0].get("content") if len(descriptionEle) > 0 else ""
        description = re.sub("起点中文网", "小说网", description)
        dateObj = socp.select('.info-list ul li > em')
        if len(dateObj) > 0:
            dateTime = re.sub('\.', '-', socp.select('.info-list ul li > em')[0].string) + " 09:00"
        else:
            dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        categorysHtml = socp.select('.crumbs-nav > a')
        categorys = []
        i = 0
        for categoryHtml in categorysHtml:
            i += 1
            if i > 3 or i == 1:
                continue
            text = categoryHtml.string
            category = text.replace(">", "")
            category = category.replace("\n", "")
            category = category.strip()
            categorys.append(category)
        title = fatHtml.find('.j_chapterName').text()
        title = re.sub('第.*章', '', title)
        content = self.handleContent(fatHtml, tool)
        detail = {
            "title": title,
            "date": dateTime,
            "content": content,
            "categorys": categorys,
            "tags": "",
            "keywords": keywords,
            "description": description,
        }
        create = CreateData('xiaoshuo', "xs_")
        # 增加导航信息
        category1 = 0
        category2 = 0
        for key in range(0, len(categorys)):
            if key == 0:
                list1 = {
                    'classname': categorys[key],
                    'pid': 0,
                }
                print('开始写入一级栏目信息')
                category1 = create.checkClassify(categorys[key])
                if category1 == None:
                    category1 = create.insertClassify(list1)
                print(category1)
            if key == 1:
                list2 = {
                    'classname': categorys[key],
                    'pid': category1,
                }
                print('开始写入二级栏目信息')
                category2 = create.checkClassify(categorys[key])
                if category2 == None:
                    category2 = create.insertClassify(list2)
        # 下载图片 图文获取缩略图
        down = DownLoadPicture(self.listInfo['thumb-img'], True, objectName="xiaoshuo")
        imageInfo, thumbInfo = down.handleDown()
        if not thumbInfo:
            thumbInfo = imageInfo
        # 写入小说
        print('开始首次写入小说信息')
        bookList = {
            'catid': category2,
            'bookname': self.listInfo['title'],
            'thumbInfo': [thumbInfo],
            'imageInfo': [imageInfo],
            'author': self.listInfo['author'],
            'pubdate': dateTime,
            'keywords': keywords,
            'description': description,
            'body': self.listInfo['intro'],
        }
        book = create.checkBook(self.listInfo['title'], self.listInfo['author'])
        if book == None:
            book = create.insertBook(bookList)
        # 写入章节
        print('开始首次写入小说章节信息')
        chapterList = {
            'bookid': book,
            'catid': category2,
            'bookname': self.listInfo['title'],
            'booktype': '',
            'title': title,
            'addchapter': 1,
            'chapternew': self.listInfo['title'],
            'body': content,
            'Submit': '保 存'
        }
        chapter = create.checkChapter(book, self.listInfo['title'])
        if chapter == None:
            chapter = create.inserChapter(chapterList)
        # 更新评分
        print('开始更新评分')
        create.updateBookStars(book, int(score))
        brower.quit()
        return book, category2, chapter
    def getNextHtml(self, url, book, category, chapter):
        print('开始写入小说以及小说章节信息')
        brower = Brower().exem()
        brower.get(url)
        html = brower.page_source
        fatHtml = pq(html)
        tool = Tool()
        title = fatHtml.find('.j_chapterName').text()
        title = re.sub('第.*章', '', title)
        content = self.handleContent(fatHtml, tool)
        detail = {
            "title": title,
            "content": content,
        }
        create = CreateData('xiaoshuo', "xs_")
        # 写入章节
        print('开始写入小说章节信息')
        chapterList = {
            'bookid': book,
            'catid': category,
            'bookname': self.listInfo['title'],
            'booktype': 0,
            'title': title,
            'chapterid': chapter,
            'chapternew': '默认章节',
            'body': content,
            'Submit': '保 存'
        }
        content2 = create.checkContent(book, title)
        if content2 == None:
            create.inserChapter(chapterList)

        brower.quit()
    def handleContent(self, html, tool):
        body = html(".read-content").html()
        body = tool.replace(body)
        imgSoap = BeautifulSoup(body, "lxml")
        content = imgSoap.prettify()
        content = pseudoStatic.handleStatic(content)
        return content