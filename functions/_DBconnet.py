import os, time
from dotenv import load_dotenv
import mysql.connector
from functions.Notification import Notification

# .env ファイルを読み込む
load_dotenv()

class DBconnect: 
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.notification_fn = Notification()

    def dbconnection(self): 
        max_retries = 3  # 最大リトライ回数
        retry_count = 0
        while retry_count < max_retries:
            try:
                self.conn = mysql.connector.connect(
                    host=os.getenv('HOST'),
                    user=os.getenv('USER'),
                    password=os.getenv('PASSWORD'),
                    database=os.getenv('DATABASE'),
                    connection_timeout=10000  # タイムアウト時間（ミリ秒）
                )
                self.conn.autocommit = True
                self.conn.ping(reconnect=True, attempts=3, delay=2)
                self.cursor = self.conn.cursor()
                return True
            except mysql.connector.Error as db_err:
                retry_count += 1
                error_message = f"データベース接続エラー: {db_err.msg} (エラーコード: {db_err.errno})"
                self.notification_fn.send_error2(db_err, error_message, f"リトライ {retry_count}/{max_retries} - {error_message}")

                if retry_count >= max_retries:
                    self.notification_fn.send_error2(db_err, error_message, "")
                    return False
                time.sleep(1)  # 5秒間待機してから再試行
            except Exception as e:
                # その他の未知のエラーの場合の処理
                error_message = f"未知のエラーが発生しました: {str(e)}"
                self.notification_fn.send_error2(e, error_message, "")
                return False
        
        
    # # DB接続がされているか確認し、接続が切れていたら再接続する
    def ensure_connection(self):
        try:
            # もし接続が存在していて、切れていない場合
            if self.conn is not None and self.conn.is_connected():
                # 接続が生きているか確認し、もし切れていたら再接続する
                self.conn.ping(reconnect=True, attempts=3, delay=2)
            else:
                if not self.dbconnection():
                    return False  # 再接続失敗
            return True  # 再接続成功または既に接続されている
        except mysql.connector.Error as db_err:
            # 再接続の際にエラーが発生した場合、エラーログを通知
            error_message = f"接続維持エラー: {db_err.msg} (エラーコード: {db_err.errno})"
            self.notification_fn.send_error2(db_err, error_message, "")
            return False
        except Exception as e:
            # その他の未知のエラー処理
            error_message = f"未知のエラーが発生しました: {str(e)}"
            self.notification_fn.send_error2(e, error_message, "")
            return False
