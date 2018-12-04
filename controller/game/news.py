# -*- coding: utf-8 -*
__author__ = 'double k'
"""
获取游戏资讯信息
http://www.ali213.net/news/game/
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
from endpoint.gameInnerChain import InnerChain
from endpoint import pseudoStatic

class GetList:
    def __init__(self, baseUrl, waitTime):
        self.baseUrl = baseUrl
        self.waitTime = waitTime
        self.brower = None
        self.html = None
        self.fatHtml = None
        self.count = 0
        self.wait = None
        self.isPaging = False

    def getHtml(self, url, page):
        self.isPaging = True
        self.brower.get(url)
        self.wait = WebDriverWait(self.brower, self.waitTime)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.t5c .t5c_l .n_lone')))
        self.html = self.brower.page_source
        self.fatHtml = pq(self.html)
        items = self.fatHtml(".t5c .t5c_l .n_lone").items()
        lists = []
        print("第", page, "页，开始获取数据")
        for item in items:
            if self.count > getPageNumber.getCount():
                print("本栏目已经获取", self.count, "条记录，目前允许最大获取数量为：", getPageNumber.getCount())
                exit()
            title = item.find(".lone_t").text()
            if not title:
                continue
            detailHref = item(".lone_t").children().attr.href
            thumbImg = item(".lone_f .lone_f_l").children().children().attr.src
            print(thumbImg)
            list = {
                "title": title,
                "detail-href": detailHref,
                "thumb-img": thumbImg
            }
            print(list)
            lists.append(list)
            self.count += 1
            print("当前第", self.count, "获取的图文信息为：", list)
            create = CreateData('gameali', "game_")
            if create.checkText(title) == None:
                detail = GetDetail(detailHref, self.waitTime, list)
                detail.getHtml()
    def waitForGetAllData(self):
        page = 2
        if self.html == None:
            return
        items = self.fatHtml(".n_lpage .p_bar").children()
        if not items:
            self.isPaging = False
            print("所有数据已经全部抓完，共抓取", self.count, "条数据")
        pageInfo = items.eq(len(items)-1)
        href = pageInfo.attr.href
        pageNum = getPageNumber.main()
        if not pageNum:
            pageNum = re.search(re.compile(".{0,}_(\d+).{0,}",re.DOTALL), href).group(1)
        while self.isPaging == True :
            if page > int(pageNum):
                return
            try:
                # text_to_be_present_in_element
                self.wait.until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, '.n_lpage .p_bar a:nth-last-child(2)'), '下页'
                    )
                )
                url = re.sub(re.compile("(?<=_)(\d+)(?=\.)"), str(page), href)
                baseUrl = self.baseUrl + url
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

        # try:
        #     print("--------", "开始获取图文列表信息", "--------")
        #     self.getHtml(self.baseUrl, 1)
        #     self.waitForGetAllData()
        #     print("--------", "结束获取图文列表信息，共获取到", self.count, "条数据--------")
        # except Exception as e:
        #     print("抓取数据失败，链接为：", self.baseUrl, "，错误信息为：", e)
        # finally:
        #     self.brower.quit()


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

        socp = BeautifulSoup(self.html, "lxml")
        keywordsEle = socp.select('meta[name=keywords]')
        descriptionEle = socp.select('meta[name=description]')
        keywords = keywordsEle[0].get("content") if len(keywordsEle) > 0 else ""
        description = descriptionEle[0].get("content") if len(descriptionEle) > 0 else ""


        # 标题有多种样式  现发现 .newstit .newstit1
        title = fatHtml(".ns_t4 .newstit").text()
        if not title:
            title = fatHtml(".newstit1").text()

        create = CreateData('gameali', "game_")
        if create.checkText(title) != None:
            print("标题为:", title, "数据已经存在，跳过")
            return
        tag = fatHtml(".newstag_l").text()
        dateObj = re.search(re.compile("\d+-\d+-\d+.*?\d+:\d+"), tag)
        if dateObj:
            dateTime = dateObj.group()
        else:
            dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        authorObj = re.search(re.compile("编辑：(.*)(?=浏)"), tag)
        if authorObj:
            author = authorObj.group(1).strip()
        else:
            author = "admin"
        viws = fatHtml.find("#totalhits").text()
        intro = tool.replace(fatHtml(".n_guide").text())
        if len(intro) > 200:
            intro = ""
        content = self.handleContent(fatHtml("#Content").html(), tool, title)
        # 导航有多种格式 不同样式先发现 .n_nav .n_nav1
        categorysHtml = fatHtml(".n_nav").children().children().items()
        if not categorysHtml:
            categorysHtml = fatHtml(".n_nav1").children().children().items()
        categorys = []
        for categoryHtml in categorysHtml:
            text = categoryHtml.text()
            category = text.replace(">", "")
            category = category.replace("\n", "")
            category = category.strip()
            if category == "游侠网":
                continue
            if category == "正文":
                continue
            categorys.append(category)
        detail = {
            "title": title,
            "author": author,
            "date": dateTime,
            "viws": viws,
            "intro": intro,
            "content": content,
            "categorys": categorys,
            "keywords": keywords,
            "description": description,
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
    def handleContent(self, html, tool, title):
        db = MySQLSingle()
        db.get_conn('gameali')
        sql = 'select * from game_sysconfig where varname="cfg_basehost"'
        config = db.getone(sql)
        if config:
            host = config['value']
        else:
            host = "http://127.0.0.1"

        html = tool.replace(html)
        soap = BeautifulSoup(html, "lxml")
        pb = soap.find("div", class_="page_fenye")
        if pb:
            soap.find("div", class_="page_fenye").extract()
        for i in range(0, len(soap.find_all('img'))):
            del soap.find_all('img')[i]['onclick']
            del soap.find_all('img')[i]['onmouseover']
            del soap.find_all('img')[i]['alt']
            down = DownLoadPicture(soap.find_all('img')[i].get('src'), objectName="gameali")
            imageInfo, thumbInfo = down.handleDown()
            path = host + imageInfo['path']
            soap.find_all('img')[i]['src'] = path
        content = str(soap)
        content = pseudoStatic.handleStatic(content)
        content = InnerChain(content=content).replace2()
        soapAlt = BeautifulSoup(content, "lxml")
        for i in range(0, len(soapAlt.find_all('img'))):
            soapAlt.find_all('img')[i]['alt'] = title
            soapAlt.find_all('img')[i]['style'] = "max-width: 712px;"
        content = str(soapAlt)
        return content
# news = GetList("http://www.ali213.net/news/game/", 5)
# news.main()
# detail = GetDetail("http://www.ali213.net/news/html/2018-9/382579.html", 5)
# detail.getHtml()
# html = '<li><a href="http://www.ali213.net" target="_blank">游侠网</a>&nbsp;&gt;&nbsp;</li>'
# aa = pq(html)
# print(aa('a').text())
