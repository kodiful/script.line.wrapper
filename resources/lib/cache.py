# -*- coding: utf-8 -*-

import os, json
import hashlib
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
        talk = addon.getSetting('talk')
        self.filepath = os.path.join(self.dirpath, '%s.json' % hashlib.md5(talk).hexdigest())

    def clear(self):
        # キャッシュディレクトリをクリア
        file_list = os.listdir(self.dirpath)
        for file_path in file_list:
            os.remove(os.path.join(self.dirpath, file_path))

    def read(self):
        if os.path.isfile(self.filepath):
            f = open(self.filepath, 'r')
            data = f.read()
            f.close()
        else:
            data = ''
        return data

    def write(self, data):
        f = open(self.filepath, 'w')
        f.write(data)
        f.close()

    def read_json(self):
        cur_data = self.read()
        if cur_data:
            try:
                data = json.loads(cur_data, 'utf-8')
            except ValueError:
                log('broken json: %s' % self.filepath)
                data = []
        else:
            data = []
        return data

    def write_json(self, data):
        # 既存データ
        cur_data = self.read()
        # 書き込みデータ
        new_data = json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2)
        if new_data != cur_data:
            self.write(new_data)
            return True
        else:
            return False
