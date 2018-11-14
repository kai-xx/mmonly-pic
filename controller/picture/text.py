# -*- coding: utf-8 -*
__author__ = 'double k'

"""
获取游戏下载
http://down.ali213.net/pcgame/
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
from endpoint.innerChain import InnerChain
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
                EC.presence_of_element_located((By.CSS_SELECTOR, '.listlbc_cont_l .Clbc_Game_l_a .gxnew-kc')))
            self.html = self.brower.page_source
            self.fatHtml = pq(self.html)
            items = self.fatHtml(".listlbc_cont_l .Clbc_Game_l_a .gxnew-kc").items()
            lists = []
            print("第", page, "页，开始获取数据")
            for item in items:
                title = item.find(".gxnew-bt").children().eq(0).text()
                if not title:
                    continue
                href = item.find(".gxnew-bt").children().eq(0).attr.href
                if not re.match("^http(s)?.*?", href):
                    href = self.host + href
                detailHref = href
                thumbImg = item(".gxnew-cont-imgshow").children().children().attr("original")
                list = {
                    "title": title,
                    "detail-href": detailHref,
                    "thumb-img": thumbImg
                }
                lists.append(list)
                self.count += 1
                print("当前第", self.count, "获取的图文信息为：", list)
                create = CreateData()
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
        items = self.fatHtml("#pageNum").children()
        if not items:
            self.isPaging = False
            print("所有数据已经全部抓完，共抓取", self.count, "条数据")
        pageInfo = items.eq(len(items)-1)
        href = pageInfo.attr.href
        pageNum = getPageNumber.main()
        if not pageNum:
            pageNum = re.search(re.compile("(?<=_)(\d+)(?=\.html)", re.DOTALL), href).group()
        while self.isPaging == True :
            if page > int(pageNum):
                return
            try:
                # text_to_be_present_in_element
                self.wait.until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, '#pageNum a:nth-last-child(2)'), '下一页'
                    )
                )
                url = re.sub(re.compile("(?<=_)(\d+)(?=\.html)"), str(page), href)
                baseUrl = self.host + url
                self.getHtml(baseUrl, page)
                page += 1
                if self.count > getPageNumber.getCount():
                    print("本栏目已经获取", self.count, "条记录，目前允许最大获取数量为：", getPageNumber.getCount())
                    return
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

        title = fatHtml(".show-cont-title").children().children().text()
        info = fatHtml(".updateTime").text()
        dateObj = re.search(re.compile("\d+-\d+-\d+ \d+:\d+"), info)
        if dateObj:
            dateTime = dateObj.group()
        else:
            dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        author = "admin"
        viws = 0
        intro = tool.replace(fatHtml(".Arc_description").text())
        if len(intro) > 200:
            intro = ""
        content = self.handleContent(fatHtml, tool)

        # 导航有多种格式 不同样式先发现 .n_nav .n_nav1
        categorysHtml = fatHtml(".show-gps").children().items()
        categorys = []
        i = 0
        for categoryHtml in categorysHtml:
            i += 1
            if i > 3 or i < 2:
                continue
            text = categoryHtml.text()
            category = text.replace(">", "")
            category = category.replace("\n", "")
            category = category.strip()
            categorys.append(category)
        tags = fatHtml(".detail_game_l_r_tag ").children().items()
        tagsList = []
        for tag in tags:
            tagsList.append(tag.text())
            print(tag.text())
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
        print("获取到的信息信息为：", detail)
        create = CreateData()
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
        down = DownLoadPicture(self.listInfo['thumb-img'], True)
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
    def handleContent(self, html, tool):
        db = MySQLSingle()
        db.get_conn()
        sql = 'select * from pic_sysconfig where varname="cfg_basehost"'
        config = db.getone(sql)
        if config:
            host = config['value']
        else:
            host = "http://127.0.0.1"
        body = html(".imgcont").html()
        body = tool.replace(body)
        imgSoap = BeautifulSoup(body, "lxml")
        for i in range(0, len(imgSoap.find_all('img'))):
            del imgSoap.find_all('img')[i]['onclick']
            del imgSoap.find_all('img')[i]['onmouseover']
            down = DownLoadPicture(imgSoap.find_all('img')[i].get('original'))
            imageInfo, thumbInfo = down.handleDown()
            if not imageInfo:
                imgSoap.find_all('img')[i].extract()
                continue
            path = host + imageInfo['path']
            imgSoap.find_all('img')[i]['original'] = path
            imgSoap.find_all('img')[i]['src'] = path
        content = imgSoap.prettify()
        content = pseudoStatic.handleStatic(content)
        content = InnerChain(content=content).replace()
        return content

# news = GetList("http://down.ali213.net/pcgame/", 5)
# news.main()
# detail = GetDetail("http://www.ali213.net/news/html/2018-9/382579.html", 5)
# detail.getHtml()
# html = '<li><a href="http://www.ali213.net" target="_blank">游侠网</a>&nbsp;&gt;&nbsp;</li>'
# aa = pq(html)
# print(aa('a').text())