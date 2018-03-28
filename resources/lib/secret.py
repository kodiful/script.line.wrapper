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
        self.data = datetime.datetime.now().strftime('%s')
        f = open(self.filepath, 'w')
        f.write(self.data)
        f.close()

    def read(self):
        if os.path.isfile(self.filepath):
            f = open(self.filepath, 'r')
            data = f.read()
            f.close()
        else:
            data = ''
        return data

    def check(self):
        data = self.read()
        log(data)
        log(self.data)
        return data and data == self.data

    def clear(self):
        if self.check():
            os.remove(self.filepath)
