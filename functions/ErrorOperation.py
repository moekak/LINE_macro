import time, os, sys
from functions.Notification import Notification


class ErrorOperation():
    
        
    # ユーザーネーム変更ボタン(鉛筆マーク)の要素が見つからないエラーが出た場合
    def restart_app(self,driver):
        try:
            notification_fn = Notification()
            # LINEアプリのパッケージ名とアクティビティ名を設定
            package_name = 'jp.naver.line.android'
            
            # アプリを停止
            driver.terminate_app(package_name)
            
            # 少し待機
            time.sleep(1)
            
            # アプリを再起動
            driver.activate_app(package_name)
            time.sleep(4)
            
            # スクリプトを再実行
            self.restart_script()
        except Exception as e:
             self.notification_fn.send_error2(e, "スクリプトの再実行に失敗しました。", "")
        
    def restart_script(self):
        print("Restarting script...")
        # pythonファイルの特定をする
        python = sys.executable
        # 現在のプロセスを終(os.execl)
        os.execl(python, python, *sys.argv)
        
        