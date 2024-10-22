from functions.DBconnect import DBconnect
from functions.ErrorOperation import ErrorOperation
from functions.Notification import Notification
from models.Device import Device
import random

class GroupMsg: 
    def __init__(self):
        self.db = DBconnect()
        self.error_operation = ErrorOperation()
        self.notification_fn = Notification()
        self.device_model  = Device()
        self.cursor = self.db.dbconnection()
        
    def getMessage(self, device_id, driver, username):
       
        try:
            self.cursor.execute('SELECT group_messages.message, message_sending_times.is_sent FROM group_messages INNER JOIN message_sending_times ON message_sending_times.id = group_messages.time_id WHERE message_sending_times.device_id = %s', (device_id,))
            data  = self.cursor.fetchall()
            
            return data
        
        except Exception as e:
            self.notification_fn.send_error2(e, "一斉配信のメッセージの取得に失敗しました。再度スクリプトを実行します。", username)
            self.error_operation.restart_app(driver)
    
    def close(self):
        self.db.close()  # デストラクタでデータベース接続を閉じる

    # ランダムで一斉送信のメッセージを抽出する
    def generateMessageList(self, messages_data):
        
        # すべてのメッセージをリスト化
        msgs = [msg[0] for msg in messages_data]
        # ランダムでメッセージを取り出す
        random_msg = random.choice(msgs)

        return random_msg
    
    # 一斉送信の時間を取得する
    def getMsgSendingTime(self, messages_data):
          # メッセージ送信時間
        sending_time = [time[1] for time in messages_data][0]
        return sending_time
    
    # 一斉送信のフラグのチェック
    def checkFlag(self, messages_data):
        
        if len(messages_data) > 0:
            flag = [flag[1] for flag in messages_data][0]
            return flag
        else:
            return 1
        
 
        
      