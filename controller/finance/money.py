# -*- coding: utf-8 -*
__author__ = 'double k'
"""
获取理财
http://money.jrj.com.cn/list/moneygdxw2017.shtml
"""
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
from ownModule.brower import Brower
from endpoint.picInnerChain import InnerChain
from endpoint import pseudoStatic

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
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.jrj-l1')))
            self.html = self.brower.page_source
            self.fatHtml = pq(self.html)
            items = self.fatHtml(".jrj-l1").children().items()
            lists = []
            print("第", page, "页，开始获取数据")
            for item in items:
                if self.count > getPageNumber.getCount():
                    print("本栏目已经获取", self.count, "条记录，目前允许最大获取数量为：", getPageNumber.getCount())
                    exit()
                title = item.children().eq(-1).text()
                if not title:
                    continue
                href = item.children().eq(-1).attr.href
                if not re.match("^http(s)?.*?", href):
                    href = self.host + href
                detailHref = href
                thumbImg = ''
                list = {
                    "title": title,
                    "detail-href": detailHref,
                    "thumb-img": thumbImg
                }
                lists.append(list)
                self.count += 1
                print("当前第", self.count, "获取的图文信息为：", list)
                create = CreateData('jinrong', "jr_")
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
        items = self.fatHtml(".page_newslib").children('a')
        if not items:
            self.isPaging = False
            print("所有数据已经全部抓完，共抓取", self.count, "条数据")
        pageInfo = items.eq(1)
        href = pageInfo.attr.href
        pageNum = getPageNumber.main()
        if not pageNum:
            pageNum = 10
        while self.isPaging == True :
            if page > int(pageNum):
                # self.isPaging = False
                print("所有数据已经全部抓完，共抓取", self.count, "条数据")
                return
            try:
                url = re.sub(re.compile("(?<=-)(\d+)(?=\.html)"), str(page), href)
                baseUrl = self.host + url
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
        self.brower.close()


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
        print("开始获取图文详情，链接为：", self.baseUrl)
        self.brower = Brower().exem()
        tool = Tool()
        self.brower.get(self.baseUrl)
        self.html = self.brower.page_source
        fatHtml = pq(self.html)
        # 标题有多种样式  现发现 .newstit .newstit1
        socp = BeautifulSoup(self.html, "lxml")
        keywordsEle = socp.select('meta[name=keywords]')
        descriptionEle = socp.select('meta[name=description]')
        keywords = keywordsEle[0].get("content") if len(keywordsEle) > 0 else ""
        description = descriptionEle[0].get("content") if len(descriptionEle) > 0 else ""
        description = tool.replace(description)
        title = fatHtml(".texttitbox").children().eq(0).text()
        info = fatHtml(".texttitbox .inftop .mh-title .time").text()
        dateObj = re.search(re.compile("\d+-\d+-\d+ \d+:\d+"), info)
        if dateObj:
            dateTime = dateObj.group()
        else:
            dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        author = "admin"
        viws = 0
        intro = description
        if len(intro) > 200:
            intro = ""
        content = self.handleContent(fatHtml, tool, title)

        # 导航有多种格式 不同样式先发现
        categorysHtml = fatHtml(".crumbs").children().children().items()
        categorys = []
        i = 0
        for categoryHtml in categorysHtml:
            i += 1
            if i > 4 or i < 3:
                continue
            text = categoryHtml.text()
            category = text.replace(">", "")
            category = category.replace("\n", "")
            category = category.strip()
            categorys.append(category)
        tagsList = []
        detail = {
            "title": title,
            "author": author,
            "date": dateTime,
            "viws": viws,
            "intro": intro,
            "content": content,
            "categorys": categorys,
            "tags": tagsList,
            "keywords": keywords,
            "description": description,
        }
        print(detail)
        create = CreateData('jinrong', "jr_")
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
        down = DownLoadPicture(self.listInfo['thumb-img'], True, objectName='jinrong')
        imageInfo, thumbInfo = down.handleDown()
        if not thumbInfo:
            thumbInfo = imageInfo
        # 写入数据
        if create.checkText(title) == None:
            # 图片必须是列表
            create.insertText(category1, category2, 1, detail, [imageInfo], [thumbInfo])
        self.brower.close()

        # try:
        #     a:1
        # except Exception as e:
        #     print("抓取数据失败，链接为：", self.baseUrl, "，错误信息为：", e)
        # finally:
        #     self.brower.quit()
    def handleContent(self, html, tool, title):
        db = MySQLSingle()
        db.get_conn('jinrong')
        # 替换xxx
        sql = 'select * from jr_sysconfig where varname="cfg_basehost"'
        config = db.getone(sql)
        if config:
            host = config['value']
        else:
            host = "http://127.0.0.1"
        body = html(".texttit_m1").html()
        body = tool.replace(body)
        imgSoap = BeautifulSoup(body, "lxml")
        for i in range(0, len(imgSoap.find_all('img'))):
            del imgSoap.find_all('img')[i]['onclick']
            del imgSoap.find_all('img')[i]['onmouseover']
            del imgSoap.find_all('img')[i]['alt']
            down = DownLoadPicture(imgSoap.find_all('img')[i].get('src'), objectName='jinrong')
            imageInfo, thumbInfo = down.handleDown()
            if not imageInfo:
                imgSoap.find_all('img')[i].extract()
                continue
            path = host + imageInfo['path']
            imgSoap.find_all('img')[i]['original'] = path
            imgSoap.find_all('img')[i]['src'] = path
        content = imgSoap.prettify()
        content = pseudoStatic.handleStatic(content)
        # content = InnerChain(content=content).replace2()
        soapAlt = BeautifulSoup(content, "lxml")
        for i in range(0, len(soapAlt.find_all('img'))):
            soapAlt.find_all('img')[i]['alt'] = title
        content = str(soapAlt)
        return content

# news = GetList("http://down.ali213.net/pcgame/", 5)
# news.main()
# detail = GetDetail("http://www.ali213.net/news/html/2018-9/382579.html", 5)
# detail.getHtml()
# html = '<li><a href="http://www.ali213.net" target="_blank">游侠网</a>&nbsp;&gt;&nbsp;</li>'
# aa = pq(html)
# print(aa('a').text())