# -*- coding: utf-8 -*
__author__ = 'double k'
from ownModule.mysql import MySQLSingle
from re import sub

class InnerChain:
    def __init__(self, databaseName=None, prefix="pic_", content=""):
        self.db = MySQLSingle()
        self.db.get_conn(databaseName)
        self.prefix = prefix
        self.content = content
        self.list = None

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

