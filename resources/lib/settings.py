# -*- coding: utf-8 -*-

import os
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

from common import log, notify

class Settings:

    def __init__(self):
        # アドオン
        addon = xbmcaddon.Addon()
        # テンプレートファイル
        self.template_file = os.path.join(xbmc.translatePath(addon.getAddonInfo('path')), 'resources', 'data', 'settings.xml')
        # 設定ファイル
        self.settings_file = os.path.join(xbmc.translatePath(addon.getAddonInfo('path')), 'resources', 'settings.xml')
        # 設定ファイルがない場合は初期化
        if not os.path.isfile(self.settings_file): self.update()

    def update(self, chatlist=[]):
        # テンプレート読み込み
        f = open(self.template_file, 'r')
        template = f.read()
        f.close()
        # トークリストを更新
        source = template.format(chatlist='|'.join(chatlist))
        # ファイル書き込み
        f = open(self.settings_file, 'w')
        f.write(source)
        f.close()
