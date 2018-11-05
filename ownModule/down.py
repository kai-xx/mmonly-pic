# -*- coding: utf-8 -*
__author__ = 'double k'

from os import path as osPath
from os import mkdir as osMkdir
import datetime
from PIL import Image
from urllib.request import urlretrieve
from config import file

class DownLoadPicture:
    def __init__(self, url="", thumb=False, objectName=None):
        self.url = url
        objName = objectName if objectName else "mmonly-utf8"
        self.path = file.basePath + objName
        self.thumb = thumb

    def destFile(self, path, thumb=""):
        dirTime = datetime.datetime.now().strftime("%Y%m%d")
        returnDir = "/uploads/allimg/" + dirTime
        savePath = osPath.join(self.path , "uploads", "allimg", dirTime)
        if not osPath.exists(savePath):
            osMkdir(savePath)
        img = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + path.split('/')[-1]
        if thumb:
            returnDir = returnDir + "/" + thumb + img
        else:
            returnDir = returnDir + "/" + img

        return osPath.join(savePath, thumb + img), returnDir

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
            print("下载链接为：", self.url, "的图片信息为：", imgInfo)
            print("下载链接为：", self.url, "的图片缩略图为：", thumbInfo)
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
