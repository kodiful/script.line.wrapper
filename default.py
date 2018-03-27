# -*- coding: utf-8 -*-

import sys
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

from resources.lib.cache import Cache
from resources.lib.smartdate import smartdate
from resources.lib.common import log, notify

#-------------------------------------------------------------------------------
if __name__  == '__main__':
    addon = xbmcaddon.Addon()
    executable_path = addon.getSetting('executable_path')
    extension_path = addon.getSetting('extension_path')
    app_id = addon.getSetting('app_id')
    email = addon.getSetting('email')
    password = addon.getSetting('password')
    talk = addon.getSetting('talk')
    if executable_path and extension_path and app_id and email and password and talk:
        # メッセージ読み込み
        messages = Cache().read_json()
        # メッセージ表示
    	for m in reversed(messages):
            # 日時
            date = smartdate(m['year'],m['month'],m['day'],m['hour'],m['minute'])
            # メッセージ
            if m['ttl']:
                message = '[COLOR yellow]%s[/COLOR] %s' % (m['ttl'], m['msg'])
            else:
                message = '%s' % (m['msg'])
            # コンテクストメニュー
            menu = []
            menu.append((addon.getLocalizedString(32801), 'Addon.OpenSettings(%s)' % addon.getAddonInfo('id')))
            # メニュー
            item = xbmcgui.ListItem('%s %s' % (date,message))
            item.addContextMenuItems(menu, replaceItems=True)
    	    xbmcplugin.addDirectoryItem(int(sys.argv[1]), '', item, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]), True)
    else:
        addon.openSettings()
