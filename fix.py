from bs4 import BeautifulSoup
from ownModule.mysql import MySQLSingle

def getAllList():
    db1 = MySQLSingle()
    db1.get_conn('gameali')

    db2 = MySQLSingle()
    db2.get_conn('gameali')

def handleContent(self, html, tool, title):
    db = MySQLSingle()
    db.get_conn('gameali')
    sql = 'select * from game_sysconfig where varname="cfg_basehost"'
    config = db.getone(sql)
    if config:
        host = config['value']
    else:
        host = "http://127.0.0.1"
    body = html(".stl-l-g").html()
    body = tool.replace(body)
    imgSoap = BeautifulSoup(body, "lxml")
    for i in range(0, len(imgSoap.find_all('img'))):
        del imgSoap.find_all('img')[i]['onclick']
        del imgSoap.find_all('img')[i]['onmouseover']
        down = DownLoadPicture(imgSoap.find_all('img')[i].get('src'), objectName="gameali")
        imageInfo, thumbInfo = down.handleDown()
        path = host + imageInfo['path']
        imgSoap.find_all('img')[i]['src'] = path
        imgSoap.find_all('img')[i]['alt'] = title
    content = imgSoap.prettify()
    content = pseudoStatic.handleStatic(content)
    content = InnerChain(content=content).replace()
    return content