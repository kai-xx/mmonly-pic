# -*- coding: utf-8 -*
__author__ = 'double k'

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import os
import datetime
import threading
import re
from ownModule.down import DownLoadPicture
from ownModule.tool import Tool
from ownModule import overTimeHandle
from endpoint.createData import CreateData
from endpoint import getPageNumber

"""
    获取导航信息
"""
class GetNavbar:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.browser = None
        self.homeHtml = None
        self.navbar = {}
        self.count = 0
    def getNavbar(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chromeOptions)
        self.browser.get(self.baseUrl)
        # self.homeHtml = pq(self.browser.page_source)
        # lis = self.homeHtml("#SonNavBox").children().children()
        # for li in lis:
        #     print(BeautifulSoup(li, "a"))
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        lis = soup.select("#SonNavBox ul li")
        navbars = []
        for li in lis:
            category = li.select('a')[0].string
            attrs = li.select('a')[0].attrs
            if category not in ['首页', '标签云', '图说天下', None]:
                navbar ={
                    'category': category,
                    'href': attrs['href']
                }
                navbars.append(navbar)
                self.count += 1
                print("获取到第", self.count, "个可用导航，信息为：", navbar)
        print("共获取到", self.count, "个可用导航")
        return navbars

    def close(self):
        self.browser.quit()
"""
    根据导航获取列表信息
"""
class GetList:
    def __init__(self, navbarInfo):
        self.navbarInfo = navbarInfo
        self.baseUrl = navbarInfo['href']
        self.brower = None
        self.wait = None
        self.listHtml = None
        self.listHtmlOriginal = None
        self.lists = []
        self.picCount = 0
        self.textCount = 0
        self.isPaging = False

    def getPicCount(self, string):
        num = re.findall(re.compile('共([0-9],{0,})张', re.S), string)
        if len(num) > 0:
            return num[0]
        else:
            return 1
    def getData(self, url):
        self.isPaging = True
        self.brower.get(url)
        self.listHtmlOriginal = self.brower.page_source
        self.listHtml = pq(self.listHtmlOriginal)
        # 获取图片数据
        self.getPicture()
        self.getPictureDetail()
        # 获取文章数据
        print("共获取到图片数据", self.picCount, "条")

    def waitForGetAllData(self):
        page = 2
        if self.listHtmlOriginal == None:
            return
        items = self.listHtml("#pageNum").children()
        if not items:
            self.isPaging = False
            print("所有数据已经全部抓完，共抓取", self.picCount, "条数据")
        pageInfo = items.eq(len(items)-1)
        href = pageInfo.attr.href
        pageNum = getPageNumber.main()
        if not pageNum:
            pageNum = re.search(re.compile(".{0,}_\d+_(\d+).{0,}",re.DOTALL), href).group(1)
        wait = WebDriverWait(self.brower, 5)
        while self.isPaging == True :
            if page > int(pageNum):
                return
            try:
                # text_to_be_present_in_element
                wait.until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, '#pageNum a:nth-last-child(2)'), '下一页'
                    )
                )
                url = re.sub(re.compile("(?<=_)(\d+)(?=\.)"), str(page), href)
                baseUrl = self.baseUrl + url
                self.getData(baseUrl)
                page += 1
            except TimeoutException:
                self.isPaging = False
                count = self.textCount + self.picCount
                print("所有数据已经全部抓完，共抓取", count, "条数据")
    def main(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        self.brower = webdriver.Chrome(chrome_options=chromeOptions)
        print("--------导航为", self.navbarInfo['category'], "开始获取数据--------")
        # 初始化页面并获取第一页数据
        self.getData(self.baseUrl)
        # 根据第一页数据判断是否需要翻页 ， 以及共有需翻页多少次
        self.waitForGetAllData()

        self.brower.quit()
        print("--------导航为", self.navbarInfo['category'], "结束获取数据--------")
        return
    def getPicture(self):
        items = self.listHtml(".Clbc_Game_l_a .item_list .item").items()
        self.lists = []
        for item in items:
            title = item.find(".title").text()
            image = item(".item_t .img .ABox").children().children().attr.original
            detailHref = item(".title").children().children().attr.href
            picCount = self.getPicCount(item.find(".items_likes").text())
            if detailHref:
                list = {
                    "title": title,
                    "image": image,
                    "detail-href": detailHref,
                    'pic-count': picCount
                }
                self.lists.append(list)
                self.picCount += 1
                print("图片数据 - 获取到第", self.picCount, "条数据，信息为：", list)
        return
    def getPictureDetail(self):
        for list in self.lists:
            d = GetPictureDetail(list)
            d.main()
        return
    def getText(self):
        return
class GetPictureDetail:
    def __init__(self, picture):
        self.picture = picture
        self.detail = None
        self.baseUrl = picture['detail-href']
        self.brower = None

    def getPictures(self, url = "", defaultImage = None):
        images = []
        maxNum = int(self.picture['pic-count']) + 1
        if defaultImage:
            images.append(defaultImage)

        for i in range(2, maxNum):
            end = "_" + str(i) + ".html"
            href = re.sub(".html", end, url)
            self.brower.get(href)
            imageHtml = pq(self.brower.page_source)
            image = imageHtml(".pic-down").children().attr.href
            if image:
                images.append(image)
        return images

    def getCategorys(self, detailHtml):
        soup = BeautifulSoup(detailHtml, 'lxml')
        catItems = soup.select(".topmbx a")
        categorys = []
        for item in catItems:
            category = item.string
            if category == "唯一图库":
                continue
            if category:
                categorys.append(category)
        return categorys

    def main(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        self.brower = webdriver.Chrome(chrome_options=chromeOptions)
        self.brower.get(self.baseUrl)
        html = self.brower.page_source
        detailHtml = pq(html)
        # print(detailHtml)
        defaultImage = detailHtml(".pic-down").children().attr.href
        images = self.getPictures(self.baseUrl, defaultImage)
        categorys = self.getCategorys(html)
        tool = Tool()
        detail = tool.replace(detailHtml(".descriptionBox").text())
        tip = detailHtml(".tip").text()
        authorOrigin = re.findall(re.compile("编辑：(.*?)更新时间："), tip)
        if len(authorOrigin) > 0:
            author = authorOrigin[0].split()[0]
        else:
            author = "管理员"
        dateOrigin = re.findall(re.compile("更新时间：(.*?)\Z"), tip)
        if len(dateOrigin) > 0:
            date = dateOrigin[0]
        else:
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(images) > 0:
            detail = {
                'title': self.picture['title'],
                "date": date,
                "author": author,
                "viws": 0,
                "intro": "",
                "content": detail,
                "categorys": categorys
            }
            print(detail)
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

            # 下载图片 图文获取缩略图
            imageInfos = []
            thumbInfos = []
            for key in range(0, len(images)):
                if key == 0:
                    thumb = True
                else:
                    thumb = False
                down = DownLoadPicture(images[key], thumb)
                imageInfo, thumbInfo = down.handleDown()
                if not thumbInfo:
                    thumbInfo = imageInfo
                imageInfos.append(imageInfo)
                thumbInfos.append(thumbInfo)
            # 写入数据
            if create.checkText(self.picture['title']) == None:
                # 图片必须是列表
                create.insertText(category1, category2, 2, detail, imageInfos, thumbInfos)
        self.brower.quit()

code = overTimeHandle.main()

if code != 100200:
    url = "http://www.mmonly.cc/"
    navbar = GetNavbar(url)
    navbars = navbar.getNavbar()
    navbars.append({'category': '美女图片', 'href': 'http://www.mmonly.cc/mmtp/'})
    navbar.close()
    def worke(nav):
        # nav = {'category': '其他图片', 'href': 'http://www.mmonly.cc/qttp/'}
        listItem = GetList(nav)
        listItem.main()
    thres = [threading.Thread(target=worke, args=(nav,))
                for nav in navbars]
    # 开始执行线程
    [thr.start() for thr in thres]
    # 等待线程执行结束
    [thr.join() for thr in thres]
    # while True:
    #     length=len(threading.enumerate())#枚举返回个列表
    #     print('当前运行的线程数为：%d'%length)
    #     if length<=1:
    #         break


    # navbar1 = {'category': '其他图片', 'href': 'http://www.mmonly.cc/qttp/'}
    # listItem = GetList(navbar1)
    # listItem.main()


    # detail = {'title': '女性脚背上的蜻蜓纹身图案', 'image': 'http://t1.hxzdhn.com/uploads/tu/201810/9999/rnce5e970959.jpg', 'detail-href': 'http://www.mmonly.cc/sgtp/jrsg/279337.html', 'pic-count': 4}
    # detail = {'title': '高广泽炫酷写真 玩转艺术范儿', 'image': 'http://t1.hxzdhn.com/uploads/tu/201811/9999/50eda7caf2.jpg', 'detail-href': 'http://www.mmonly.cc/sgtp/omsg/279836.html', 'pic-count': 4}
    # d = GetPictureDetail(detail)
    # d.main()

    # string = "编辑：唯一图库 \xa0\xa0\xa0更新时间：2018-10-30 09:40"
    #
    # print(re.findall(re.compile("更新时间：(.*?)\Z"), string)[0])
