__author__ = 'double k'
import urllib.request
import os
import datetime
from PIL import Image
import re

basePath = r"../testImage/"

def destFile(path, thumb = ""):
    if not os.path.exists(basePath):
        os.mkdir(basePath)
    img = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + path.split('/')[-1]
    return os.path.join(basePath, thumb + img)
url = "http://t1.hxzdhn.com/uploads/tu/201709/9999/d333a20953.jpg"
filename = destFile(url)
urllib.request.urlretrieve(url, filename)
img = Image.open("/Users/carter/Documents/code/python3 object/20181030230515d333a20953.jpg", "r")
img.thumbnail((200, 200), Image.ANTIALIAS)
img.save(destFile(url,"200*200_"))
img.close()
print(img.size, img.format, img.mode)


