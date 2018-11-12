# -*- coding: utf-8 -*
__author__ = 'double k'
"""
获取图片网站
"""
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import re
import datetime
from ownModule.down import DownLoadPicture
from ownModule.tool import Tool
from endpoint.createData import CreateData
from endpoint import getPageNumber
from ownModule.brower import Brower
from bs4 import BeautifulSoup
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
                EC.presence_of_element_located((By.CSS_SELECTOR, '.Clbc_Game_l_a .item_list .item')))
            self.html = self.brower.page_source
            self.fatHtml = pq(self.html)
            items = self.fatHtml('.Clbc_Game_l_a .item_list .item').items()
            lists = []
            print("第", page, "页，开始获取数据")
            for item in items:
                title = item(".title").children().text()
                if not title:
                    continue
                href = item(".title").children().children().attr.href
                if not re.match("^http(s)?.*?", href):
                    href = self.host + href
                detailHref = href
                thumbImg = item(".img .ABox").children().children().attr("original")
                list = {
                    "title": title,
                    "detail-href": detailHref,
                    "thumb-img": thumbImg
                }
                lists.append(list)
                self.count += 1
                print("当前第", self.count, "获取的图片信息为：", list)
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
            except TimeoutException:
                self.isPaging = False
                print("所有数据已经全部抓完，共抓取", self.count, "条数据")

    def main(self):
        self.brower = Brower().exem()
        print("--------", "开始获取图片列表信息", "--------")
        self.getHtml(self.baseUrl, 1)
        self.waitForGetAllData()
        print("--------", "结束获取图片列表信息，共获取到", self.count, "条数据--------")
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
        print("开始获取图片详情，链接为：", self.baseUrl)
        try:
            self.brower = Brower().exem()
            tool = Tool()
            self.brower.get(self.baseUrl)
            self.html = self.brower.page_source
            fatHtml = pq(self.html)
            socp = BeautifulSoup(self.html, "lxml")
            keywordsEle = socp.select('meta[name=keywords]')
            descriptionEle = socp.select('meta[name=description]')
            keywords = keywordsEle[0].get("content") if len(keywordsEle) > 0 else ""
            description = descriptionEle[0].get("content") if len(descriptionEle) > 0 else ""

            title = self.listInfo['title']
            tip = fatHtml(".tip").text()
            authorOrigin = re.findall(re.compile("编辑：(.*?)更新时间："), tip)
            if len(authorOrigin) > 0:
                author = authorOrigin[0].split()[0]
            else:
                author = "管理员"
            dateOrigin = re.findall(re.compile("更新时间：(.*?)\Z"), tip)
            if len(dateOrigin) > 0:
                dateTime = dateOrigin[0]
            else:
                dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            viws = 0
            intro = tool.replace(fatHtml(".descriptionBox").text())
            content = ""
            categorysHtml = fatHtml(".topmbx").children().items()
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
                if category == "唯一图库":
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
                "tags": "",
                "keywords": keywords,
                "description": description,
            }
            imageCountHtml = fatHtml('.pages').children().children()
            if len(imageCountHtml) > 0:
                imageCount = re.search(re.compile("(?<=共)(\d+)(?=页)", re.DOTALL), imageCountHtml.eq(0).text()).group()
            else:
                imageCount = 0
            defaultImage = fatHtml(".pic-down").children().attr.href

            create = CreateData()
            # 增加导航信息
            category1 = 0
            category2 = 0
            for key in range(0, len(categorys)):
                if key == 0:
                    category1 = create.checkAndInsertCate(categorys[key], 0, 2)
                    print(category1)
                if key == 1:
                    category2 = create.checkAndInsertCate(categorys[key], category1, 2)
            # 下载图片 图片获取缩略图
            down = DownLoadPicture(self.listInfo['thumb-img'], True)
            imageInfo, thumb = down.handleDown()
            if not thumb:
                thumb = imageInfo
            images = self.getPictures(imageCount, defaultImage)
            imageInfos = []
            for image in images:
                down = DownLoadPicture(image)
                imageInfo, thumbInfo = down.handleDown()
                imageInfos.append(imageInfo)
            # 写入数据
            if create.checkText(title) == None:
                # 图片必须是列表
                create.insertText(category1, category2, 2, detail, imageInfos, [thumb])
            self.brower.close()

        except Exception as e:
            print("抓取数据失败，链接为：", self.baseUrl, "，错误信息为：", e)
        finally:
            self.brower.quit()

    def getPictures(self, maxNum, defaultImage=None):
        images = []
        if defaultImage:
            images.append(defaultImage)
        if int(maxNum) > 0:
            maxNum = int(maxNum) + 1
            for i in range(2, maxNum):
                end = "_" + str(i) + ".html"
                href = re.sub(".html", end, self.baseUrl)
                self.brower.get(href)
                imageHtml = pq(self.brower.page_source)
                image = imageHtml(".pic-down").children().attr.href
                if image:
                    images.append(image)
        print("图片集信息为：", images)
        return images