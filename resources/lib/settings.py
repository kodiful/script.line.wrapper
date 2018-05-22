# -*- coding: utf-8 -*-

import os
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

from common import log, notify

class Settings:

    def __init__(self):
        # アドオン
        self.addon = xbmcaddon.Addon()
        path = xbmc.translatePath(self.addon.getAddonInfo('path'))
        # テンプレートファイル
        self.template_file = os.path.join(path, 'resources', 'data', 'settings.xml')
        # 設定ファイル
        self.settings_file = os.path.join(path, 'resources', 'settings.xml')
        # 設定ファイルがない場合は初期化
        if not os.path.isfile(self.settings_file): self.update()

    def update(self, chatlist=None):
        # テンプレート読み込み
        f = open(self.template_file, 'r')
        template = f.read()
        f.close()
        # トークリストを更新
        if chatlist:
            source = template.format(chatlist='|'.join(chatlist))
            if self.addon.getSetting('talk') == 'default':
                self.addon.setSetting('talk', chatlist[0])
        else:
            # 未設定の場合
            source = template.format(chatlist='default')
            self.addon.setSetting('talk', 'default')
        # ファイル書き込み
        f = open(self.settings_file, 'w')
        f.write(source)
        f.close()
