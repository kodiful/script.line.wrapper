# -*- coding: utf-8 -*-

import hashlib
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

from resources.lib.line import Line
from resources.lib.cache import Cache
from resources.lib.secret import Secret
from resources.lib.settings import Settings
from resources.lib.common import log, notify

class Monitor(xbmc.Monitor):

    def __init__(self, line):
        self.line = line
        xbmc.Monitor.__init__(self)

    def onSettingsChanged(self):
        addon = xbmcaddon.Addon()
        talk = addon.getSetting('talk')
        self.line.select(talk)
        folderpath = 'plugin://%s/' % addon.getAddonInfo('id')
        if xbmc.getInfoLabel('Container.FolderPath') == folderpath:
            xbmc.executebuiltin('Container.Update(%s)' % folderpath)

    def onScreensaverActivated(self):
        log('screensaver activated')

    def onScreensaverDeactivated(self):
        log('screensaver deactivated')

def service():
    # アドオン
    addon = xbmcaddon.Addon()
    # 設定ファイルを初期化
    settings = Settings()
    # キーを初期化
    secret = Secret(renew=True)
    # 設定
    executable_path = addon.getSetting('executable_path')
    extension_path = addon.getSetting('extension_path')
    app_id = addon.getSetting('app_id')
    email = addon.getSetting('email')
    password = addon.getSetting('password')
    talk = addon.getSetting('talk')
    if executable_path and extension_path and app_id and email and password:
        # LINEにログイン
        line = Line(executable_path, extension_path, app_id)
        if line.open(email, password):
            line.select(talk)
            # 着信を監視
            hash = ''
            monitor = Monitor(line)
            while not monitor.abortRequested():
                # 停止を待機
                if monitor.waitForAbort(5): break
                # キーをチェック
                if secret.check() == False: break
                # 表示されているメッセージを取得
                messages = line.watch()
                # 差分の有無をチェック
                talk1 = xbmcaddon.Addon().getSetting('talk')
                hash1 = hashlib.md5(str(messages)).hexdigest()
                # 差分があれば通知
                if hash != hash1 and Cache().write_json(messages):
                    # 画面切り替え
                    cec = xbmcaddon.Addon().getSetting('cec')
                    if cec == 'true':
                        xbmc.executebuiltin('CECActivateSource')
                    folderpath = 'plugin://%s/' % addon.getAddonInfo('id')
                    if xbmc.getInfoLabel('Container.FolderPath') == folderpath:
                        xbmc.executebuiltin('Container.Update(%s)' % folderpath)
                    elif cec == 'true':
                        xbmc.executebuiltin('RunAddon(%s)' % addon.getAddonInfo('id'))
                    # 通知
                    m = messages[-1]
                    if m['ttl']:
                        notify('%s > %s' %(m['ttl'],m['msg']))
                    else:
                        notify(m['msg'])
                # ハッシュを記録
                hash = hash1
        # LINEを終了
        line.close()
    # キーをクリア
    secret.clear()

if __name__ == "__main__": service()
