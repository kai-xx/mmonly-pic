# -*- coding: utf-8 -*
__author__ = 'double k'

import requests


def handleStatic(content):
    try:
        url = 'http://www.naipan.com/open/weiyuanchuang/towei.html'
        postData = {
            # 'regname': "402202330@qq.com",
            # 'regsn': "9Neqm72/zIWkhlmFO5pvKZCdh0XB2UF+W56B1uFRcZQ=",
            'regname': "1218763958@qq.com",
            'regsn': "x0vSrtcxdI77+6/5tXEpqNj+whMkwSFc4Hmq0NfguQk=",
            'content': content
        }
        print("处理伪原创，链接为：%s，内容为：%s" % (url, postData))
        r = requests.post(url, data=postData)
        result = r.json()
        print("处理伪原创,返回信息为：%s" % result)
        if result['result'] == 1:
            content = result['content']
    except Exception as e:
        print("处理伪原创失败，错误信息为：", e)
    finally:
        return content
