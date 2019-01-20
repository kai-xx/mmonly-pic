# -*- coding: utf-8 -*
__author__ = 'double k'

import datetime
from os import rmdir
from ownModule.mysql import MySQLSingle
from config import file


def main(check=True, objectName=None, year=2019, month=1, day=1, days=40):
    if check == False:
        return None
    else:
        objName = objectName if objectName else "mmonly-pic"
        objectDir = file.objectPath + objName

        now = datetime.datetime.now()
        overTime = now - datetime.datetime(year, month, day)
        overTime = overTime.days

        if overTime > days:
            db = MySQLSingle()
            db.get_conn()
            if objName == "mmonly-pic":
                databaseName = 'picmmonly'
            elif objName == 'jinrong':
                databaseName = 'jinrong'
            else:
                databaseName = 'gameali'
            sql = "drop database " + databaseName
            print(db.sql(sql))
            # db.closeall()
            rmdir(objectDir)
            return 100200
        else:
            return None

