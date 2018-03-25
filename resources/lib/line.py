# -*- coding: utf-8 -*-

import sys, os
import datetime, re, hashlib
import socket
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

from common import log, notify

# import selenium
sys.path.append(os.path.join(xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')), 'resources', 'lib', 'selenium-3.9.0'))
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Line:

    def __init__(self, executable_path, extension_path, app_id):
        # ウェブドライバを設定
        chrome_options = Options()
        chrome_options.add_extension(extension_path)
        self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
        self.app_id = app_id
        # HTTP接続におけるタイムアウト(秒)
        socket.setdefaulttimeout(60)

    def open(self, email, password):
        try:
            # ページ読み込み
            self.driver.implicitly_wait(10)
            self.driver.get('chrome-extension://%s/index.html' % self.app_id)
            # メールアドレス
            elem = self.driver.find_element_by_id('line_login_email')
            elem.send_keys(email)
            # パスワード
            elem = self.driver.find_element_by_id('line_login_pwd')
            elem.send_keys(password)
            # ログイン
            elem = self.driver.find_element_by_id('login_btn')
            elem.click()
            # 本人確認コードを通知
            elem = self.driver.find_element_by_xpath("//div[@class='mdCMN01Code']")
            notify('Enter %s to Mobile LINE' % elem.text)
            return 1
        except:
            notify('Login failed', error=True, time=3000)
            return 0

    def select(self, talkroom):
        try:
            # トークルーム
            self.driver.implicitly_wait(60)
            elem = self.driver.find_element_by_xpath("//li[@title='%s']" % talkroom)
            elem.click()
            return 1
        except:
            notify('Login failed', error=True, time=3000)
            return 0

    def close(self):
        # 終了
        self.driver.close()

    def watch(self):
        # メッセージ
        messages = []
        self.driver.implicitly_wait(10)
        elems = self.driver.find_elements_by_xpath("//div[@class='mdRGT07Msg mdRGT07Text' or @class='MdRGT10Notice mdRGT07Other mdRGT10Date']")
        for elem in elems:
            date = elem.get_attribute('data-local-id')
            if date:
                # 日付
                d = datetime.datetime.fromtimestamp(int(date)/1000)
            else:
                # メッセージ
                elem1 = elem.find_element_by_xpath(".//span[@class='mdRGT07MsgTextInner']")
                msg = elem1.text.replace('\n', ' ')
                # 時刻
                elem2 = elem.find_element_by_xpath(".//p[@class='mdRGT07Date']")
                match = re.match(r'(AM|PM) (1?[0-9])\:([0-9][0-9])', elem2.text)
                hour = int(match.group(2))
                minute = int(match.group(3))
                if match.group(1) == 'PM': hour += 12
                # 親エレメント
                elem3 = elem1.find_element_by_xpath("../../../..")
                cls = elem3.get_attribute('class')
                if cls == 'MdRGT07Cont mdRGT07Own':
                    src = '<'
                elif cls == 'MdRGT07Cont mdRGT07Other':
                    src = '>'
                else:
                    src = ''
                # 格納
                message = {
                    'year': d.year,
                    'month': d.month,
                    'day': d.day,
                    'hour': hour,
                    'minute': minute,
                    'src': src,
                    'msg': msg.encode('utf-8')
                }
                messages.append(message)
                #log('%04d-%02d-%02d %02d:%02d %s %s' % (d.year,d.month,d.day,hour,minute,src,msg))
        return messages
