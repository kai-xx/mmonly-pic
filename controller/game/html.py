# -*- coding: utf-8 -*
__author__ = 'double k'
from ownModule.mysql import MySQLSingle
import urllib.request
from urllib import request

def setHtml():
    databaseName = 'gameali'
    prefix = 'game_'
    db = MySQLSingle()
    db.get_conn(databaseName)
    sql1 = "select * from " + prefix + "sysconfig where varname='cfg_basehost'"
    config = db.getone(sql1)
    if config:
        host = config['value']
    else:
        host = "http://127.0.0.1"
    sql2 = "select id,title from " + prefix + "archives where ismake=-1 "
    list = db.getall(sql2)
    if len(list) == 0:
        return
    for one in list:
        sql3 = "UPDATE " + prefix + "archives SET `ismake` = '1' WHERE `id` = %d" % (one['id'],)
        id = db.save(sql3, one['id'])
        if id:
            print(one)
            setUrl = "%s/gamead/html.php?aid=%d" % (host, one['id'])
            print(setUrl)
            response = request.urlopen(setUrl)
            html = response.read()
            print(html)
