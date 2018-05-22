# -*- coding: utf-8 -*-

import sys, os
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
    addon_path = xbmc.translatePath(addon.getAddonInfo('path'))
    executable_path = addon.getSetting('executable_path')
    extension_path = addon.getSetting('extension_path')
    email = addon.getSetting('email')
    password = addon.getSetting('password')
    # 必要なアドオン設定が揃っていたらメインの処理を実行
    if executable_path and extension_path and email and password:
        if action:
            if action[0] == 'reset':
                # 再ログイン
                threading.Thread(target=service).start()
            elif action[0] == 'submit':
                # メッセージをファイルに書き出し送信はserviceにまかせる
                message = addon.getSetting('message')
                Cache('submit','message.txt').write(message)
        else:
            # トークルームが未設定の場合
            if xbmcaddon.Addon().getSetting('talk') == 'default':
                # 再ログイン
                threading.Thread(target=service).start()
                # トークルーム設定が終わるまで最大10秒待つ
                wait = 0
                while wait < 60:
                    if xbmcaddon.Addon().getSetting('talk') != 'default': break
                    xbmc.sleep(1000)
                    wait += 1
                else:
                    sys.exit()
            # 送信メッセージのファイルをクリア
            Cache('submit').clear()
            # メッセージ読み込み
            messages = Cache('json').read_json()
            # デフォルトイメージ
            default_image = os.path.join(addon_path, 'resources', 'data', 'image', 'icons8-contacts-filled-500.png')
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
                image = m['img'] or default_image
                item = xbmcgui.ListItem('%s %s' % (date,message), iconImage=image, thumbnailImage=image)
                item.addContextMenuItems(menu, replaceItems=True)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), '', item, False)
            xbmcplugin.endOfDirectory(int(sys.argv[1]), True)
    else:
        addon.openSettings()
