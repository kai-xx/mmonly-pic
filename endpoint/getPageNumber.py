# -*- coding: utf-8 -*
__author__ = 'double k'
import datetime
"""
如果发布超过发布日期15天以上
则每天抓取20页，否则抓取所有
"""
def main():
    days = 15
    now = datetime.datetime.now()
    overTime = now - datetime.datetime(2018, 11, 20)
    overTime = overTime.days

    if overTime > days:
        return 20
    else:
        return 0