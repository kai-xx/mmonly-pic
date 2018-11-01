# -*- coding: utf-8 -*
__author__ = 'double k'

import datetime
from os import rmdir
from ownModule.mysql import MySQLSingle


def main(check = True):
    if check == False:
        return None
    else:
        days = 20
        overTime = "20181120"
        objectDir = "/home/www/picmmonly"

        now = datetime.datetime.now()
        future_time = now - datetime.timedelta(days=int(days))
        fu = future_time.strftime('%Y%m%d')

        if overTime == str(fu):
            db = MySQLSingle()
            db.get_conn()
            sql = "drop database picmmonly"
            print(db.sql(sql))
            db.closeall()
            rmdir(objectDir)

