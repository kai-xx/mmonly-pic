# -*- coding: utf-8 -*
__author__ = 'double k'
import re
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import threading
from bs4 import BeautifulSoup
from ownModule.down import DownLoadPicture
from ownModule.tool import Tool
from ownModule import overTimeHandle
from endpoint.createData import CreateData
from ownModule.mysql import MySQLSingle

class GetNav:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.brower = None
        self.count = 0
        self.html = None

    def getHtml(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--headless")
        self.brower = webdriver.Chrome(chrome_options=chromeOptions)
        self.brower.get(self.baseUrl)
        self.html = pq(self.brower.page_source)
        items = self.html(".more").items()
        print("--------", "开始获取更多图文信息导航", "--------")
        moreUrls = []
        for item in items:
            url = item.attr.href
            moreUrls.append(url)
            print("获取到的图文更多链接为：", url)
            self.count += 1
        self.brower.quit()
        print("共获取", self.count, "条图文信息导航")
        print("--------", "结束获取更多图文信息导航", "--------")
        return moreUrls

class GetTextList:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.brower = None
        self.wait = None
        self.count = 0
        self.html = None
        self.isPaging = False

    def getData(self, url):
        print("开始---查询链接为：", url)
        self.isPaging = True
        self.brower.get(url)
        self.html = pq(self.brower.page_source)
        items = self.html(".listlbc_cont_l .Clbc_Game_l_a .gxnew-kc").items()
        for item in items:
            soup = BeautifulSoup(str(item), 'lxml')
            titleList = soup.select(".gxnew-bt > a")[0]
            title = titleList.string
            detailHref = titleList.attrs['href']
            thumbImg = soup.select("#imgshow img")[0].attrs['original']
            list = {
               "title": title,
               "detail-href": detailHref,
               "thumb-img": thumbImg
            }
            self.count += 1
            print("当前第", self.count, "获取的图文信息为：", list)
            detail = GetTextDetail(detailHref, list)
            detail.main()
        print("结束---查询链接为：", url)
    def waitForGetAllData(self):
        page = 2
        print("页码为", page, "，初始URL为", self.baseUrl)
        if self.html == None:
            return
        items = self.html("#pageNum").children()
        if not items:
            self.isPaging = False
            print("所有数据已经全部抓完，共抓取", self.count, "条数据")
        pageInfo = items.eq(len(items)-1)
        href = pageInfo.attr.href
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
                print("所有数据已经全部抓完，共抓取", self.count, "条数据")

    def getHtml(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        self.brower = webdriver.Chrome(chrome_options=chromeOptions)
        print("--------", "开始获取图文列表信息", "--------")
        self.getData(self.baseUrl)
        self.waitForGetAllData()
        self.brower.quit()
        print("--------", "结束获取图文列表信息，共获取到", self.count, "条数据--------")

class GetTextDetail:
    def __init__(self, baseUrl, listInfo):
        self.baseUrl = baseUrl
        self.browes = None
        self.html = None
        self.detailhtml = None
        self.count = 0
        self.listInfo = listInfo
    def getCategorys(self):
        soup = BeautifulSoup(self.detailhtml, 'lxml')
        catItems = soup.select(".show-gps a")
        categorys = []
        for item in catItems:
            category = item.string
            if category == "唯一图库":
                continue
            if category:
                categorys.append(category)
        return categorys

    def handleContent(self, tool):
        db = MySQLSingle()
        sql = 'select * from pic_sysconfig where varname="cfg_basehost"'
        config = db.getone(sql)
        if config:
            host = config['value']
        else:
            host = "http://127.0.0.1"
        html = tool.replace(self.html(".imgcont").html())
        soap = BeautifulSoup(html, "lxml")
        for i in range(0,len(soap.find_all('img'))):
            down = DownLoadPicture(soap.find_all('img')[i].get('original'))
            imageInfo, thumbInfo = down.handleDown()
            path = host + imageInfo['path']
            soap.find_all('img')[i]['original'] = path
            soap.find_all('img')[i]['src'] = path
        return str(soap)

    def main(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--headLess")
        self.browes = webdriver.Chrome(chrome_options=chromeOptions)
        self.browes.get(self.baseUrl)
        self.detailhtml = self.browes.page_source
        self.html = pq(self.detailhtml)
        tool = Tool()
        title = tool.replace(self.html(".show-cont-title").text())
        dateOrigin = re.findall(
            re.compile("更新时间：(.*?)\Z"),
            self.html(".show-cont-xxlist .updateTime").text()
        )
        if len(dateOrigin) > 0:
            date = dateOrigin[0]
        else:
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        viws = re.search(re.compile("(\d+)次"), self.html("#hits").text()).group(1)
        intro = tool.replace(self.html(".Arc_description").text())
        content = self.handleContent(tool)
        categorys = self.getCategorys()
        detail = {
            "title": title,
            "date": date,
            "viws": viws,
            "intro": intro,
            "content": content,
            "categorys": categorys
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
        self.browes.quit()

#         图片下载demo
# url = "http://t1.hxzdhn.com/uploads/tu/201706/9999/11df03cb01.jpg"
# url = "http://t1.hxzdhn.com/mmonly/2014/201409/084/1.jpg"
# url = "http://t1.hxzdhn.com/uploads/tu/201611/tt/2v3a1bcyckh.jpg"
# url = "http://t1.hxzdhn.com/mmonly/2011/201104/144/3.jpg"
# down = DownLoadPicture(url, True)
# a, b = down.handleDown()
# print(a)
# print(b)

# 数据库处理demo
# db = MySQLSingle()
# db.get_conn()
# list = db.getone("select * from pic_arctype where id = 1")
# print(list)
# quit()
#
overTimeHandle.main()
url = "http://www.mmonly.cc/tstx/"
navbar = GetNav(url)
navs = navbar.getHtml()
def worke(nav):
    listItem = GetTextList(nav)
    listItem.getHtml()
#  开启线程
thres = [threading.Thread(target=worke, args=(nav,))
            for nav in navs]
# 开始执行线程
[thr.start() for thr in thres]
# 等待线程执行结束
[thr.join() for thr in thres]

# 获取列表调试代码
# url = "http://www.mmonly.cc/tstx/dyyp/"
# listObj = GetTextList(url)
# listObj.getHtml()

# 获取详情信息调试代码
# url = "http://www.mmonly.cc/tstx/ylxw/192333.html"
# listInfo = {
#                "title": "盘点娱乐圈女星透视装，若隐约现，小孩都看了都脸红！",
#                "detail-href": "http://www.mmonly.cc/tstx/ylxw/192333.html",
#                "thumb-img": "http://t1.hxzdhn.com/uploads/tu/201709/9999/rn7706ea40ca.jpeg"
#             }
# detailObj = GetTextDetail(url, listInfo)
# detailObj.main()