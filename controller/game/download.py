# -*- coding: utf-8 -*
__author__ = 'double k'

"""
获取游戏下载
http://down.ali213.net/pcgame/
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


class GetList:
    def __init__(self, baseUrl, waitTime):
        self.host = "http://down.ali213.net"
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
                EC.presence_of_element_located((By.CSS_SELECTOR, '.list_body .list_body_contain .list_body_con')))
            self.html = self.brower.page_source
            self.fatHtml = pq(self.html)
            items = self.fatHtml(".list_body .list_body_contain .list_body_con").items()
            lists = []
            print("第", page, "页，开始获取数据")
            for item in items:
                title = item.find(".list_body_con_con").text()
                if not title:
                    continue
                href = item(".list_body_con_con").children().attr.href
                if not re.match("^http(s)?.*?", href):
                    href = self.host + href
                detailHref = href
                thumbImg = item(".list_body_con_img").children().attr("data-original")
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
        items = self.fatHtml(".list_body_page").children()
        if not items:
            self.isPaging = False
            print("所有数据已经全部抓完，共抓取", self.count, "条数据")
        pageInfo = items.eq(len(items)-1)
        href = pageInfo.attr.href
        pageNum = getPageNumber.main()
        if not pageNum:
            pageNum = re.search(re.compile("(?<=pic-)\d+(?=.html)", re.DOTALL), href).group()
        while self.isPaging == True :
            if page > int(pageNum):
                return
            try:
                # text_to_be_present_in_element
                self.wait.until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, '.list_body_page a:nth-last-child(2)'), '下一页'
                    )
                )
                url = re.sub(re.compile("(?<=pic-)\d+(?=.html)"), str(page), href)
                baseUrl = self.host + url
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
        self.brower = webdriver.Chrome(chrome_options=chromeOptions)
        tool = Tool()
        self.brower.get(self.baseUrl)
        self.html = self.brower.page_source
        fatHtml = pq(self.html)
        # 标题有多种样式  现发现 .newstit .newstit1
        title = fatHtml(".detail_game_l .detail_game_l_r .detail_game_l_r_tit .detail_game_l_r_ctit").children().eq(0).text()
        info = fatHtml(".detail_game_l_r_info").text()
        dateObj = re.search(re.compile("\d+-\d+-\d+"), info)
        if dateObj:
            dateTime = "%s 00:00" % (dateObj.group(),)
        else:
            dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        author = "admin"
        viws = 0
        intro = tool.replace(fatHtml("#yxjs .detail_body_left_info_con").text())
        if len(intro) > 200:
            intro = ""
        content = self.handleContent(fatHtml, tool)

        # 导航有多种格式 不同样式先发现 .n_nav .n_nav1
        categorysHtml = fatHtml(".detail_game_l_nav").children().items()
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
            if category == "下载首页":
                continue
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
            "tags": tagsList
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

        pzyq = html.find('#pzyq').html()
        if not pzyq:
            pzyq = ""
        azsm = html.find('#azsm').html()
        if not azsm:
            azsm = ""
        bbyxk = html.find('.detail_body_left_info').html()
        if not bbyxk:
            bbyxk = ""
        downButten = html.find('.quick_down').html()
        imageInfo = html("#bimg").html()
        images = []
        if imageInfo:
            imgSoap = BeautifulSoup(imageInfo, "lxml")
            for image in imgSoap.select('.detail_body_con_bb_con_con img'):
                src = image.get('src')
                print("獲取到連接為", src)
                if src:
                    down = DownLoadPicture(src, objectName="gameali")
                    imageInfo, thumbInfo = down.handleDown()
                    if not imageInfo:
                        continue
                    path = host + imageInfo['path']
                    images.append(path)

        bodyHtml = pzyq + azsm +bbyxk
        bodyHtml = tool.replace(bodyHtml) + downButten
        # 处理游戏介绍
        yxjs = html.find('#yxjs').html()
        if not yxjs:
            yxjs = ""
        else:
            yxjs = tool.replace(yxjs)
            imgSoap = BeautifulSoup(yxjs, "lxml")
            for i in range(0, len(imgSoap.find_all('img'))):
                down = DownLoadPicture(imgSoap.find_all('img')[i].get('src'), objectName="gameali")
                imageInfo, thumbInfo = down.handleDown()
                path = host + imageInfo['path']
                imgSoap.find_all('img')[i]['src'] = path
            bodyHtml = str(imgSoap) + bodyHtml

        resultHtml = self.addPic(images, bodyHtml)
        return resultHtml

    def addPic(self, images, bodyHtml):
        imageCount = len(images)
        if imageCount > 0:
            html = '<div id="example3" class="slider-pro"></div>'
            soup = BeautifulSoup(html)
            div_tag = soup.div
            slides_tag = soup.new_tag('div', attrs={"class": "sp-slides"})
            thumb_tag = soup.new_tag('div', attrs={"class": "sp-thumbnails"})
            for image in range(0, imageCount):
                if not images[image]:
                    continue
                slide_tag = soup.new_tag('div',  attrs={"class": "sp-slide"})
                slide_img_tag = soup.new_tag('img', attrs={
                    "class": "sp-image",
                    "src": "src/css/images/blank.gif",
                    "data-src": images[image],
                    "data-small": images[image],
                    "data-medium": images[image],
                    "data-large": images[image],
                    "data-retina": images[image],
                })
                slide_tag.append(slide_img_tag)
                slides_tag.append(slide_tag)
                thumb_img_tag = soup.new_tag('img', attrs={"class": "sp-thumbnail", "src": images[image]})
                thumb_tag.append(thumb_img_tag)
            div_tag.append(slides_tag)
            div_tag.append(thumb_tag)
            js = '	<script type="text/javascript" src="http://game-ali.com/templets/default/slipde/jquery-1.11.0.min.js"></script>' \
	        '<script type="text/javascript" src="http://game-ali.com/templets/default/slipde/jquery.sliderPro.min.js"></script>' \
	        '<link rel="stylesheet" type="text/css" href="http://game-ali.com/templets/default/slipde/slider-pro.min.css" media="screen"/>' \
	        '<script type="text/javascript">' \
		    '$( document ).ready(function( $ ) { $( "#example3" ).sliderPro({ width: 700, height: 500, fade: true, arrows: true, buttons: false, fullScreen: true, shuffle: true, smallSize: 500, mediumSize: 1000, largeSize: 3000, thumbnailArrows: true, autoplay: false }); });' \
	        '</script>'
            res = BeautifulSoup(str(div_tag) + js + bodyHtml)

            return res.prettify()
        else:
            res = BeautifulSoup(bodyHtml)
            return res.prettify()

# news = GetList("http://down.ali213.net/pcgame/", 5)
# news.main()
# detail = GetDetail("http://www.ali213.net/news/html/2018-9/382579.html", 5)
# detail.getHtml()
# html = '<li><a href="http://www.ali213.net" target="_blank">游侠网</a>&nbsp;&gt;&nbsp;</li>'
# aa = pq(html)
# print(aa('a').text())