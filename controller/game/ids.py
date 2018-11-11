# -*- coding: utf-8 -*
__author__ = 'double k'
"""
获取游戏硬件信息信息
http://in.ali213.net/news/
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import re
import datetime
from bs4 import BeautifulSoup
from ownModule.down import DownLoadPicture
from ownModule.tool import Tool
from endpoint.createData import CreateData
from endpoint import getPageNumber
from ownModule.mysql import MySQLSingle
from endpoint.innerChain import InnerChain
from endpoint import pseudoStatic

class GetList:
    def __init__(self, baseUrl, waitTime):
        self.host = "http://in.ali213.net"
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
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.it-ltl .ltl-l .ltl-l-o')))
            self.html = self.brower.page_source
            self.fatHtml = pq(self.html)
            items = self.fatHtml(".it-ltl .ltl-l .ltl-l-o").items()
            lists = []
            print("第", page, "页，开始获取数据")
            for item in items:
                title = item(".ltl-l-o-r-t").children().text()
                if not title:
                    continue
                href = item(".ltl-l-o-r-t").children().attr.href
                if not re.match("^http(s)?.*?", href):
                    href = self.host + href
                detailHref = href
                thumbImg = item(".ltl-l-o-l").children().children().attr.src
                intro = re.sub("\[阅读更多\]", "", item(".ltl-l-o-r-m").text())
                intro = re.sub("\n", "", intro)
                list = {
                    "title": title,
                    "detail-href": detailHref,
                    "thumb-img": thumbImg,
                    "intro": intro
                }
                lists.append(list)
                self.count += 1
                print("当前第", self.count, "获取的图文信息为：", list)
                create = CreateData('gameali', "game_")
                if create.checkText(title) == None:
                    print("标题为:", title, "数据不存在，开始获取详情")
                    detail = GetDetail(detailHref, self.waitTime, list)
                    detail.getHtml()
                else:
                    print("标题为:", title, "数据已经存在，跳过")
        except Exception as e:
            print("页面抓取异常，没有返回信息，链接为：", self.baseUrl, "，错误信息为：", e)


    def waitForGetAllData(self):
        page = 2
        if self.html == None:
            return
        items = self.fatHtml(".ltl-l-p").children()
        if not items:
            self.isPaging = False
            print("所有数据已经全部抓完，共抓取", self.count, "条数据")
        pageInfo = items.eq(len(items)-1)
        href = pageInfo.attr.href
        pageNum = getPageNumber.main()
        if not pageNum:
            pageNum = re.search(re.compile("(?<=news\/)\d+(?=.html)", re.DOTALL), href).group()
        while self.isPaging == True :
            if page > int(pageNum):
                return
            try:
                # text_to_be_present_in_element
                self.wait.until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, '.ltl-l-p a:nth-last-child(2)'), '下一页'
                    )
                )
                url = re.sub(re.compile("(?<=news\/)\d+(?=.html)"), str(page), href)
                if not re.match("^http(s)?.*?", url):
                    baseUrl = self.host + url
                else:
                    baseUrl = url
                self.getHtml(baseUrl, page)
                page += 1
            except TimeoutException:
                self.isPaging = False
                print("所有数据已经全部抓完，共抓取", self.count, "条数据")

    def main(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        chromeOptions.add_argument('--window-size=1024,768')
        self.brower = webdriver.Chrome(chrome_options=chromeOptions)

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
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        chromeOptions.add_argument('--window-size=1024,768')
        self.brower = webdriver.Chrome(chrome_options=chromeOptions)
        tool = Tool()
        self.brower.get(self.baseUrl)
        self.html = self.brower.page_source
        fatHtml = pq(self.html)
        title = fatHtml(".stl-l-t").text()
        info = fatHtml(".stl-l-i").text()
        dateObj = re.search(re.compile("\d+-\d+-\d+ \d+:\d+"), info)
        if dateObj:
            dateTime = dateObj.group()
        else:
            dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        authorObj = re.search(re.compile("(?<=编辑：).*(?=我要评论|)"), info)
        if authorObj:
            author = authorObj.group()
        else:
            author = "admin"
        viws = 0
        intro = self.listInfo['intro']
        content = self.handleContent(fatHtml, tool)
        categorysHtml = fatHtml(".stl-l-n").children().items()
        categorys = []
        i = 0
        for categoryHtml in categorysHtml:
            i += 1
            if i > 3:
                continue
            text = categoryHtml.text()
            category = text.replace(">", "")
            category = category.replace("\n", "")
            category = category.strip()
            if category == "热门资讯":
                continue
            if category == "游侠硬件":
                category = re.sub("游侠", "游戏", category)
            categorys.append(category)
        detail = {
            "title": title,
            "author": author,
            "date": dateTime,
            "viws": viws,
            "intro": intro,
            "content": content,
            "categorys": categorys,
            "tags": ""
        }
        print("获取到的信息信息为：", detail)
        create = CreateData('gameali', "game_")
        # 增加导航信息
        category1 = 0
        category2 = 0
        for key in range(0, len(categorys)):
            if key == 0:
                category1 = create.checkAndInsertCate(categorys[key], 0, 1)
                print(category1)
            if key == 1:
                category2 = create.checkAndInsertCate(categorys[key], category1, 1)
        # 下载图片 图文获取缩略图
        down = DownLoadPicture(self.listInfo['thumb-img'], True, objectName="gameali")
        imageInfo, thumbInfo = down.handleDown()
        if not thumbInfo:
            thumbInfo = imageInfo
        # 写入数据
        if create.checkText(title) == None:
            # 图片必须是列表
            create.insertText(category1, category2, 1, detail, [imageInfo], [thumbInfo])
        self.brower.quit()

        # try:
        #     a:1
        # except Exception as e:
        #     print("抓取数据失败，链接为：", self.baseUrl, "，错误信息为：", e)
        # finally:
        #     self.brower.quit()
    def handleContent(self, html, tool):
        db = MySQLSingle()
        db.get_conn('gameali')
        sql = 'select * from game_sysconfig where varname="cfg_basehost"'
        config = db.getone(sql)
        if config:
            host = config['value']
        else:
            host = "http://127.0.0.1"
        body = html(".stl-l-g").html()
        body = tool.replace(body)
        imgSoap = BeautifulSoup(body, "lxml")
        for i in range(0, len(imgSoap.find_all('img'))):
            del imgSoap.find_all('img')[i]['onclick']
            del imgSoap.find_all('img')[i]['onmouseover']
            down = DownLoadPicture(imgSoap.find_all('img')[i].get('src'), objectName="gameali")
            imageInfo, thumbInfo = down.handleDown()
            path = host + imageInfo['path']
            imgSoap.find_all('img')[i]['src'] = path
        content = imgSoap.prettify()
        content = pseudoStatic.handleStatic(content)
        content = InnerChain(content=content).replace()
        return content