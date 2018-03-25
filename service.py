# -*- coding: utf-8 -*-

import hashlib
import xbmc, xbmcaddon

from resources.lib.line import Line
from resources.lib.cache import Cache
from resources.lib.common import log, notify

class Monitor(xbmc.Monitor):

    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)

    def onSettingsChanged(self):
        log('settings changed')

    def onScreensaverActivated(self):
        log('screensaver activated')

    def onScreensaverDeactivated(self):
        log('screensaver deactivated')

if __name__ == "__main__":
    addon = xbmcaddon.Addon()
    executable_path = addon.getSetting('executable_path')
    extension_path = addon.getSetting('extension_path')
    app_id = addon.getSetting('app_id')
    email = addon.getSetting('email')
    password = addon.getSetting('password')
    talkroom = addon.getSetting('talkroom')
    if executable_path and extension_path and app_id and email and password and talkroom:
        # LINEにログイン
        line = Line(executable_path, extension_path, app_id)
        if line.open(email,password) and line.select(talkroom):
            # 着信を監視
            hash = ''
            monitor = Monitor()
            while not monitor.abortRequested():
                # 停止を待機
                if monitor.waitForAbort(5): break
                # 表示されているメッセージを取得
                messages = line.watch()
                # 差分の有無をチェック
                hash1 = hashlib.md5(str(messages)).hexdigest()
                # 差分があれば通知
                if hash != hash1:
                    # メッセージ書き出し
                    Cache().write(messages)
                    # 通知＆画面切り替え
                    if hash and len(messages)>0:
                        m = messages[-1]
                        # 通知
                        notify(m['msg'])
                        # 画面切り替え
                        if xbmcaddon.Addon().getSetting('cec') == 'true':
                            xbmc.executebuiltin('CECActivateSource')
                            xbmc.executebuiltin('RunAddon(%s)' % addon.getAddonInfo('id'))
                    # ハッシュを記録
                    hash = hash1
        # LINEを終了
        line.close()
