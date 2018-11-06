# -*- coding: utf-8 -*
__author__ = 'double k'
from ownModule.mysql import MySQLSingle
import time
from pypinyin import lazy_pinyin
import random

class CreateData:
    def __init__(self, databaseName=None, prefix="pic_"):
        self.db = MySQLSingle()
        self.db.get_conn(databaseName)
        self.prefix = prefix
    def checkAndInsertCate(self, cateName, pid, channeltype):

        sql = "select id from "+ self.prefix +"arctype where typename='%s' and reid=%d" % (cateName, pid)
        cateInfo = self.db.getone(sql)
        if cateInfo:
            print("导航--", cateName, "--已经存在，导航ID为：", cateInfo['id'])
            return cateInfo['id']
        else:
            pinyin = "".join(lazy_pinyin(cateName))

            if pid > 0:
                sql = "select * from "+ self.prefix +"arctype where id=%d" % (pid,)
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
            sql = "INSERT INTO `"+ self.prefix +"arctype` (`id`, `reid`, `topid`, `sortrank`, `typename`, `typedir`, " \
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
        sql = "select id from "+ self.prefix +"archives where title='%s'" % (title)
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
        if detail['date']:
            senddate = int(time.mktime(time.strptime(detail['date'], '%Y-%m-%d %H:%M')))
        else:
            senddate = int(time.time())
        # 第一步骤写入 表名 ："+ self.prefix +"arctiny
        sql1 = "INSERT INTO `"+ self.prefix +"arctiny` (`typeid`, `typeid2`, `arcrank`, `channel`, `senddate`, `sortrank`, `mid`) " \
               "VALUES (%d, 0, 0, %d, %d, %d, 1)" % (category2, channel, senddate, senddate)
        aid = self.db.add(sql1)
        click = random.randint(70, 800)
        title = detail['title']
        thumb = thumbInfo[0]['path'] if thumbInfo[0]['path'] else ""
        description = detail['intro']
        body = detail['content']
        if aid:
            try:
                # 第二走写入 主档案表 表名："+ self.prefix +"archives
                sql2 = "INSERT INTO `"+ self.prefix +"archives` (`id`, `typeid`, `typeid2`, `sortrank`, `flag`, `ismake`, " \
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
                    sqld1 = "delete from "+ self.prefix +"arctiny where id = %d" % (aid,)
                    self.db.sql(sqld1)
                try:
                    # 第三步写入 附屬表表 表名：channel=2->"+ self.prefix +"addonimages  channel=1->"+ self.prefix +"addoninfos
                    if channel == 1:
                        sql3 = "INSERT INTO `"+ self.prefix +"addonarticle` (`aid`, `typeid`, `body`, `redirecturl`, `templet`, `userip`) " \
                               "VALUES (%d, %d, '%s', '', '', '127.0.0.1')" % (aid, cate, body)
                    if channel == 2:
                        sql3 = "INSERT INTO `"+ self.prefix +"addonimages` (`aid`, `typeid`, `pagestyle`, `maxwidth`, " \
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
                        sqld1 = "delete from "+ self.prefix +"arctiny where id = %d" % (aid,)
                        sqld2 = "delete from "+ self.prefix +"archives where id = %d" % (aid,)
                        self.db.sql(sqld1)
                        self.db.sql(sqld2)
                    else:
                        self.addTags(detail, aid, cate, senddate)
                except Exception as e:
                    print("第三步写入 附屬表表 表名：channel=2->"+ self.prefix +"addonimages  channel=1->"+ self.prefix +"addoninfos", e)
                    sqld1 = "delete from "+ self.prefix +"arctiny where id = %d" % (aid,)
                    sqld2 = "delete from "+ self.prefix +"archives where id = %d" % (aid,)
                    self.db.sql(sqld1)
                    self.db.sql(sqld2)
            except Exception as e:
                print("第二走写入 主档案表 异常 表名："+ self.prefix +"archives", e)
                sqld1 = "delete from "+ self.prefix +"arctiny where id = %d" % (aid,)
                self.db.sql(sqld1)

            # 第四步写入 图片表 表名："+ self.prefix +"uploads
            sql4 = "INSERT INTO `"+ self.prefix +"uploads` (`arcid`, `title`, `url`, `mediatype`, `width`, `height`, " \
                   "`playtime`, `filesize`, `uptime`, `mid`) VALUES"
            sql4Value = ""
            for image in imgInfo:
                try:
                    sql4Value += ",(%d, '%s', '%s', 0, '%s', '%s', '0', %d, %d, 1)" % (aid, title, image['path'],
                                                                                   str(image['width']), str(image['height']), image['size'], senddate)
                except Exception as e:
                    print("第四步图片处理出现异常(主图)，错误信息为：", e)
                    continue
            for image1 in thumbInfo:
                try:
                    sql4Value += ",(%d, '%s', '%s', 0, '%s', '%s', '1', %d, %d, 1)" % (aid, title, image1['path'],
                                                                                   str(image1['width']),
                                                                                   str(image1['height']),
                                                                                   image1['size'], senddate)
                except Exception as e:
                    print("第四步图片处理出现异常(缩略图)，错误信息为：", e)
                    continue
            if sql4Value:
                self.db.add(sql4 + sql4Value.strip(','))
        else:
            print("标题为：", title, "的数据添加失败！")
            return None
        # self.db.closeall()

    def handleImageUrls(self, images):
        imageUrls = '{dede:pagestyle maxwidth="800" pagepicnum="12" ddmaxwidth="200" row="3" col="4" value="2"/}\r\n'
        for image in images:
            path = image["path"]
            width = image["width"]
            height = image["height"]
            imageUrls += '{dede:img ddimg="%s" text="" width="%d" height="%d"} %s {/dede:img}\r\n' % (path, width, height, path)

        return imageUrls

    def addTags(self, detail, aid, typeid, sendate):
        if 'tags' in detail:
            print("开始添加标签信息")
            for tagName in detail['tags']:
                if self.checkTag(tagName) != None:
                    continue
                try:
                    sql1 = "insert into `"+ self.prefix +"tagindex` (tag, typeid, count, total, weekcc, monthcc, weekup, monthup, addtime) values " \
                           "('%s','%d',0,1,0,0,'%d','%d','%d')" % (tagName, typeid, sendate, sendate, sendate)
                    tag = self.db.add(sql1)
                    if tag:
                        sql2 = "insert into `"+ self.prefix +"taglist` (tid, aid, arcrank, typeid, tag) VALUES ('%d','%d',0,'%d','%s')" % (
                        tag, aid, typeid, tagName)
                        tagList = self.db.add(sql2)
                except:
                    print("标签添加失败，文章ID：", aid)
                    return
                finally:
                    print("标签信息添加结束")
                    return
        else:
            print("没有传标签信息，不处理标签添加")
            return
    def checkTag(self, tagName):
        sql = "select id from `"+ self.prefix +"tagindex` where tag='%s'" % (tagName,)
        tag = self.db.getone(sql)
        if tag:
            print("名称为：%s 的标签已存在，标签ID为：%d" % (tagName, tag['id']))
            sql1 = "update `"+ self.prefix +"tagindex` set  total=total+1 where tag='%s" % (tagName)
            self.db.save(sql1, tag['id'])
            return tag['id']
        else:
            return None