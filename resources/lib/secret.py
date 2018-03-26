# -*- coding: utf-8 -*-

import os
import hashlib, datetime
import xbmc, xbmcaddon

from common import log, notify

class Secret:

    def __init__(self, filename='secret.txt'):
        # キャッシュディレクトリを作成
        addon = xbmcaddon.Addon()
        self.dirpath = xbmc.translatePath(addon.getAddonInfo('profile'))
        if not os.path.isdir(self.dirpath):
            os.makedirs(self.dirpath)
        self.filepath = os.path.join(self.dirpath, filename)
        # データを設定
        self.data = datetime.datetime.now().strftime('%s')
        f = open(self.filepath, 'w')
        f.write(self.data)
        f.close()

    def check(self):
        if os.path.isfile(self.filepath):
            f = open(self.filepath, 'r')
            data = f.read()
            f.close()
            # データを比較
            return data == self.data
        else:
            self.data = ''
            return False

    def clear(self):
        if self.read(): os.remove(self.filepath)
