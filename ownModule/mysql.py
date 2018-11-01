# -*- coding: utf-8 -*
__author__ = 'double k'

from functools import wraps
import pymysql
from config import db

def singleton(cls):
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return get_instance

# 数据库连接实例
@singleton
class MySQLSingle(object):
    def __init__(self):
        self.conn = None
        self.cursor = None

    def get_conn(self):
        host = db.host
        username = db.username
        password = db.password
        database = db.database
        try:
            self.conn = pymysql.connect(host, username, password, database)
        except Exception as e:
            print('File to connect database: %s' % e)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.getName()
        return self.conn
    def getName(self):
        try:
            sql = "SET NAMES utf8"
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            # 如果发生错误则回滚
            self.conn.rollback()


    def add(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return self.cursor.lastrowid()
        except:
            # 如果发生错误则回滚
            self.conn.rollback()
            return False

    def save(self, sql, id):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return id
        except:
            # 如果发生错误则回滚
            self.conn.rollback()
            return False
    def getone(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchone()
            return results
        except:
            return False
    def getall(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()

            return results
        except Exception as e:
            print('File to connect database: %s' % e)
            return False
    def closeall(self):
        if self.cursor != None and self.conn != None:
            self.cursor.close()
            self.conn.close()
    def sql(self, sql):
        try:
            return self.cursor.execute(sql)
        except:
            return False

