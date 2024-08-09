from functions.DBconnet import DBconnect
import random

class GroupMsg: 
    def __init__(self):
        self.db = DBconnect()
        self.cursor = self.db.dbconnection()
        
    def getMessage(self, device_id):
        self.cursor.execute('SELECT group_messages.message,  message_sending_times.is_sent FROM group_messages INNER JOIN message_sending_times ON message_sending_times.id = group_messages.time_id WHERE message_sending_times.device_id = %s', (device_id,))
        data  = self.cursor.fetchall()
        return data
    
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
    
    def checkFlag(self, messages_data):
        print(messages_data)
        input("wait")
        flag = [flag[1] for flag in messages_data][0]
        return flag
      