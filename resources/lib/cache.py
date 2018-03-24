# -*- coding: utf-8 -*-

import os, json
import xbmc, xbmcaddon

from common import log, notify

class Cache:

    def __init__(self):
        # キャッシュディレクトリを作成
        addon = xbmcaddon.Addon()
        self.dirpath = os.path.join(xbmc.translatePath(addon.getAddonInfo('profile')), 'cache')
        if not os.path.isdir(self.dirpath):
            os.makedirs(self.dirpath)
        # ファイルパスを設定
        self.filepath = os.path.join(self.dirpath, 'messages.json')

    def clear(self):
        # キャッシュディレクトリをクリア
        file_list = os.listdir(self.dirpath)
        for file_path in file_list:
            os.remove(os.path.join(self.dirpath, file_path))

    def read(self):
        if os.path.isfile(self.filepath):
            try:
                f = open(self.filepath,'r')
                data = json.loads(f.read(), 'utf-8')
                f.close()
            except ValueError:
                log('broken json: %s' % self.filepath)
                data = []
        else:
            data = []
        return data

    def write(self, data):
        f = open(self.filepath,'w')
        f.write(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2))
        f.close()
