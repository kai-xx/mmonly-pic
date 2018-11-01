# -*- coding: utf-8 -*
__author__ = 'double k'

from os import path as osPath
from os import mkdir as osMkdir
import datetime
from PIL import Image
from urllib.request import urlretrieve
from config import file

class DownLoadPicture:
    def __init__(self, url="", thumb=False):
        self.url = url
        self.path = file.basePath
        self.thumb = thumb

    def destFile(self, path, thumb=""):
        dir = "/uploads/allimg/" + datetime.datetime.now().strftime("%Y%m%d")
        savePath = osPath.join(self.path + dir)
        if not osPath.exists(savePath):
            osMkdir(savePath)
        img = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + path.split('/')[-1]
        return osPath.join(savePath, thumb + img), osPath.join(dir, thumb+img)

    def handleDown(self):
        try:
            filename, imgSavePath = self.destFile(self.url)
            urlretrieve(self.url, filename)
            if self.thumb:
                thumbInfo = self.handleThumb(path=filename)
            else:
                thumbInfo = {}
            img = Image.open(filename, "r")
            imgInfo = {
                "width": img.width,
                "height": img.height,
                "size": self.getSize(filename),
                "path": imgSavePath
            }
            img.close()
            return imgInfo, thumbInfo
        except Exception as e:
            print("下载图片失败，失败链接为：", self.url, ",错误信息为：", e)
            return {}, {}

    def handleThumb(self, path, width=400, height=400):
        try:
            img = Image.open(path, "r")
            img.thumbnail((width, height), Image.ANTIALIAS)
            thumb = str(width) + "*" + str(height) + "_"
            savePath, thumbSavePath = self.destFile(self.url, thumb)
            img.save(savePath)
            thumbInfo = {
                "width": img.width,
                "height": img.height,
                "size": self.getSize(savePath),
                "path": thumbSavePath
            }
            img.close()
            return thumbInfo
        except Exception as e:
            print("生成缩略图失败，失败链接为：", path, ",错误信息为：", e)
            return {}

    def getSize(self, filePath):
        return osPath.getsize(filePath)
