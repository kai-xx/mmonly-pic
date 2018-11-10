# -*- coding: utf-8 -*
__author__ = 'double k'
from selenium import webdriver
class Brower:
    def __init__(self):
        self.brower = None
    def exem(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        chromeOptions.add_argument('--window-size=1024,768')
        self.brower = webdriver.Chrome(chrome_options=chromeOptions)
        # self.brower = webdriver.Chrome()
        return self.brower
    def close(self):
        self.brower.quit()
        return
