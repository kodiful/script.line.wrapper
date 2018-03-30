# -*- coding: utf-8 -*-

import sys
import urlparse
import threading
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

from service import service
from resources.lib.cache import Cache
from resources.lib.smartdate import smartdate
from resources.lib.common import log, notify

#-------------------------------------------------------------------------------
if __name__  == '__main__':
    # 引数
    args = urlparse.parse_qs(sys.argv[2][1:])
    action = args.get('action')
    # アドオン設定
    addon = xbmcaddon.Addon()
    executable_path = addon.getSetting('executable_path')
    extension_path = addon.getSetting('extension_path')
    app_id = addon.getSetting('app_id')
    email = addon.getSetting('email')
    password = addon.getSetting('password')
    talk = addon.getSetting('talk')
    # 必要なアドオン設定が揃っていたらメインの処理を実行
    if executable_path and extension_path and app_id and email and password and talk:
        # リセット
        if action:
            if action[0] == 'reset':
                threading.Thread(target=service).start()
            elif action[0] == 'submit':
                # メッセージをファイルに書き出し送信はserviceにまかせる
                message = addon.getSetting('message')
                Cache('submit','message.txt').write(message)
        else:
            # 送信メッセージのファイルをクリア
            Cache('submit').clear()
            # メッセージ読み込み
            messages = Cache('json').read_json()
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
                image = m['img'] or 'DefaultArtist.png'
                item = xbmcgui.ListItem('%s %s' % (date,message), iconImage=image, thumbnailImage=image)
                item.addContextMenuItems(menu, replaceItems=True)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), '', item, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]), True)
    else:
        addon.openSettings()
