# -*- coding: utf-8 -*
__author__ = 'double k'
from ownModule.mysql import MySQLSingle
import time
from pypinyin import lazy_pinyin
import random

class CreateData:
    def __init__(self):
        self.db = MySQLSingle()
        self.db.get_conn()

    def checkAndInsertCate(self, cateName, pid, channeltype):

        sql = "select id from pic_arctype where typename='%s' and reid=%d" % (cateName, pid)
        cateInfo = self.db.getone(sql)
        if cateInfo:
            print("导航--", cateName, "--已经存在，导航ID为：", cateInfo['id'])
            return cateInfo['id']
        else:
            pinyin = "".join(lazy_pinyin(cateName))

            if pid > 0:
                sql = "select * from pic_arctype where id=%d" % (pid,)
                cateInfo = self.db.getone(sql)
                typedir = cateInfo['typedir'] + "/" + pinyin
            else:
                typedir = "{cmspath}/a/%s" % (pinyin,)

            if channeltype == 2:
                channelItem = "image"
            else:
                channelItem = "article"
            tempindex = "{style}/index_%s.htm" % (channelItem,)
            # templist = "{style}/list_%s.htm" % (channelItem,)
            temparticle = "{style}/article_%s.htm" % (channelItem,)
            sql = "INSERT INTO `pic_arctype` (`id`, `reid`, `topid`, `sortrank`, `typename`, `typedir`, " \
                  "`isdefault`, `defaultname`, `issend`, `channeltype`, `maxpage`, `corank`, `tempindex`, " \
                  "`templist`, `temparticle`, `namerule`, `namerule2`, `modname`, `description`, `keywords`, `seotitle`, " \
                  "`moresite`, `sitepath`, `siteurl`, `ishidden`, `cross`, `crossid`, `content`, `smalltypes`) VALUES " \
                  "(null, %d, %d, 0, '%s', '%s', " \
                  "0, 'index.html', 1, %d, -1, 0, '%s', " \
                  "'{style}/list_image.htm', '%s', '{typedir}/{Y}{M}{D}/{aid}.html', '{typedir}/list_{tid}_{page}.html', 'default', '', '', '%s'" \
                  ", 0, '', '', 0, 0, '0', '', '')" % (pid, pid, cateName, typedir, channeltype, tempindex, temparticle, cateName)
            id = self.db.add(sql)
            print("导航--", cateName, "--写入成功，导航ID为：", id)
            if not id:
                return 0
            return id

    def checkText(self, title):
        sql = "select id from pic_archives where title='%s'" % (title)
        textInfo = self.db.getone(sql)
        if textInfo:
            print("文章标题为--", title, "--已经存在，文章ID为：", textInfo['id'])
            return textInfo['id']
        else:
            return None

    def insertText(self, category1, category2, channel, detail, imgInfo, thumbInfo):
        if category2:
            cate = category2
        elif category1:
            cate = category1
        else:
            cate = 0

        senddate = int(time.time())
        # 第一步骤写入 表名 ：pic_arctiny
        sql1 = "INSERT INTO `pic_arctiny` (`typeid`, `typeid2`, `arcrank`, `channel`, `senddate`, `sortrank`, `mid`) " \
               "VALUES (%d, 0, 0, %d, %d, %d, 1)" % (category2, channel, senddate, senddate)
        aid = self.db.add(sql1)
        click = random.randint(70, 800)
        title = detail['title']
        thumb = thumbInfo[0]['path'] if thumbInfo[0]['path'] else ""
        description = detail['intro']
        body = detail['content']
        if aid:
            try:
                # 第二走写入 主档案表 表名：pic_archives
                sql2 = "INSERT INTO `pic_archives` (`id`, `typeid`, `typeid2`, `sortrank`, `flag`, `ismake`, " \
                       "`channel`, `arcrank`, `click`, `money`, `title`, `shorttitle`, `color`, " \
                       "`writer`, `source`, `litpic`, `pubdate`, `senddate`, `mid`, `keywords`, " \
                       "`lastpost`, `scores`, `goodpost`, `badpost`, `voteid`, `notpost`, `description`, " \
                       "`filename`, `dutyadmin`, `tackid`, `mtype`, `weight`) " \
                       "VALUES (%d, %d, 0, %d, 'p', -1, " \
                       "%d, 0, %d, 0, '%s', '%s', '', " \
                       "'admin', '未知', '%s', %d, %d, 1, '', " \
                       "0, 0, 0, 0, 0, 0, '%s', " \
                       "'', 1, 0, 0, 0)" % (aid, cate, senddate,
                                            channel, click, title, title,
                                            thumb, senddate, senddate,
                                            description)
                archives = self.db.add(sql2)
                print("第二走写入 主档案表 完成，等待后续处理")
                if type(archives) != int:
                    print("第二走写入 主档案表 异常 回退")
                    sqld1 = "delete from pic_arctiny where id = %d" % (aid,)
                    self.db.sql(sqld1)
                try:
                    # 第三步写入 附屬表表 表名：channel=2->pic_addonimages  channel=1->pic_addoninfos
                    if channel == 1:
                        sql3 = "INSERT INTO `pic_addonarticle` (`aid`, `typeid`, `body`, `redirecturl`, `templet`, `userip`) " \
                               "VALUES (%d, %d, '%s', '', '', '127.0.0.1')" % (aid, cate, body)
                    if channel == 2:
                        sql3 = "INSERT INTO `pic_addonimages` (`aid`, `typeid`, `pagestyle`, `maxwidth`, " \
                               "`imgurls`, `row`, `col`, `isrm`, `ddmaxwidth`, `pagepicnum`, " \
                               "`templet`, `userip`, `redirecturl`, `body`) " \
                               "VALUES (%d, %d, 2, 800, " \
                               "'%s', " \
                               "3, 4, 1, 200, 12, " \
                               "'', '127.0.0.1', '', '%s')" % (aid, cate,
                                                               self.handleImageUrls(imgInfo), body)
                    aux = self.db.add(sql3)
                    print("第三步写入 附屬表表完成，等待后续处理")
                    if type(aux) != int:
                        print("第三步写入 附屬表表 异常 回退")
                        sqld1 = "delete from pic_arctiny where id = %d" % (aid,)
                        sqld2 = "delete from pic_archives where id = %d" % (aid,)
                        self.db.sql(sqld1)
                        self.db.sql(sqld2)
                except Exception as e:
                    print("第三步写入 附屬表表 表名：channel=2->pic_addonimages  channel=1->pic_addoninfos", e)
                    sqld1 = "delete from pic_arctiny where id = %d" % (aid,)
                    sqld2 = "delete from pic_archives where id = %d" % (aid,)
                    self.db.sql(sqld1)
                    self.db.sql(sqld2)
            except Exception as e:
                print("第二走写入 主档案表 异常 表名：pic_archives", e)
                sqld1 = "delete from pic_arctiny where id = %d" % (aid,)
                self.db.sql(sqld1)

            # 第四步写入 图片表 表名：pic_uploads
            sql4 = "INSERT INTO `pic_uploads` (`arcid`, `title`, `url`, `mediatype`, `width`, `height`, " \
                   "`playtime`, `filesize`, `uptime`, `mid`) VALUES"
            sql4Value = ""
            for image in imgInfo:
                sql4Value += ",(%d, '%s', '%s', 0, '%s', '%s', '0', %d, %d, 1)" % (aid, title, image['path'],
                                                                                   str(image['width']), str(image['height']), image['size'], senddate)
            for image1 in thumbInfo:
                sql4Value += ",(%d, '%s', '%s', 0, '%s', '%s', '1', %d, %d, 1)" % (aid, title, image1['path'],
                                                                                   str(image1['width']),
                                                                                   str(image1['height']),
                                                                                   image1['size'], senddate)
            if sql4Value:
                self.db.add(sql4 + sql4Value.strip(','))
        else:
            print("标题为：", title, "的数据添加失败！")
            return None
        self.db.closeall()

    def handleImageUrls(self, images):
        imageUrls = '{dede:pagestyle maxwidth="800" pagepicnum="12" ddmaxwidth="200" row="3" col="4" value="2"/}\r\n'
        for image in images:
            path = image["path"]
            width = image["width"]
            height = image["height"]
            imageUrls += '{dede:img ddimg="%s" text="" width="%d" height="%d"} %s {/dede:img}\r\n' % (path, width, height, path)

        return imageUrls