# -*- coding: utf-8 -*
__author__ = 'double k'
from ownModule.mysql import MySQLSingle
from re import sub

class InnerChain:
    def __init__(self, databaseName='jinrong', prefix="jr_", content=""):
        self.db = MySQLSingle()
        self.db.get_conn(databaseName)
        self.prefix = prefix
        self.content = content
        self.list = None
        self.one = None

    def getTypeList(self):
        sql = "select id,typename,typedir,namerule2 from %sarctype where reid=0" % (self.prefix,)
        self.list = self.db.getall(sql)
    def getHost(self):
        sql = 'select * from %ssysconfig where varname="cfg_basehost"' % (self.prefix,)
        config = self.db.getone(sql)
        if config:
            host = config['value']
        else:
            host = "http://127.0.0.1"
        return host
    def replace(self):
        if not self.content:
            return self.content
        try:
            self.getTypeList()
            print(self.list)

            if not self.list:
                return self.content
            if len(self.list) == 0:
                return self.content
            for one in self.list:
                dir = sub('{cmspath}', self.getHost(), one['typedir'])
                nameRule = sub('{typedir}', dir, one['namerule2'])
                nameRule = sub('{tid}', str(one['id']), nameRule)
                nameRule = sub('{page}', '1', nameRule)
                a = "<a href='%s'>%s</a>" % (nameRule, one['typename'])
                self.content = sub(one['typename'], a, self.content)
        except Exception as e:
            print("文章内容替换内链接发生错误，错误信息为：", e)
        finally:
            return self.content
# ''
# -------第二版关键词关联------------
#     游戏
#     游戏 ---首页
#     硬件 ---游戏硬件
#     资讯 ---资讯中心
#     攻略 ---攻略
#     单机游戏 ---单机游戏
#     VR --- VR频道
#     手机游戏 - --手机游戏
#     补丁 - --补丁
# ''
    def getOne(self, name=None):
        if name == None:
            return None
        sql = "select id,typename,typedir,namerule2 from %sarctype where reid=0 and typename='%s'" % (self.prefix, name)
        self.one = self.db.getone(sql)
    def replace2(self):
        if not self.content:
            return self.content
        try:
            navbars = {
                "游戏": "首页",
                "硬件": "游戏硬件",
                "资讯": "资讯中心",
                "攻略": "攻略",
                "单机游戏": "单机游戏",
                "VR": " VR频道",
                "手机游戏": "手机游戏",
                "补丁": "补丁"
            }
            print(navbars.items())
            for key, navbar in navbars.items():
                print(key)
                if key != "游戏":
                    self.getOne(navbar)
                    if not self.one:
                        continue
                    dir = sub('{cmspath}', self.getHost(), self.one['typedir'])
                    nameRule = sub('{typedir}', dir, self.one['namerule2'])
                    nameRule = sub('{tid}', str(self.one['id']), nameRule)
                    nameRule = sub('{page}', '1', nameRule)
                    a = '<a href="%s">%s</a>' % (nameRule, key)
                    self.content = sub(key, a, self.content)
                else:
                    a = '<a href="%s">%s</a>' % (self.getHost(), key,)
                    self.content = sub("(?<!手机|单机)游戏", a, self.content)

        except Exception as e:
            print("文章内容替换内链接发生错误，错误信息为：", e)
        finally:
            return self.content