from functions.DBconnect import DBconnect
from functions.Notification import Notification
import sys
from models.Device import Device
from functions.ErrorOperation import ErrorOperation


class MsgSendingTimes: 
      def __init__(self):
            self.db = DBconnect()
            self.cursor = None
            self.notification_fn = Notification()
            self.device_model = Device()
            self.error_operation = ErrorOperation()
            self.cursor = self.db.dbconnection()
     
      def close(self):
            self.db.close()  # デストラクタでデータベース接続を閉じる
            
      def updateFlag(self, device_id, driver):
      
            try:
                  self.cursor.execute('UPDATE message_sending_times SET is_sent = "1" WHERE device_id = %s', (device_id,))
                  self.db.conn.commit()  # 変更を永続化
                  
            except Exception as e:
                  username = self.device_model.selectUsername(device_id)
                  self.notification_fn.send_error2(e, "一斉配信のフラグの更新に失敗しました。再度スクリプトを実行します。", username)
                  self.error_operation.restart_app(driver)

      def selectStartAndEndId(self, device_id, driver):
            
      
            try:
                  self.cursor.execute('SELECT start_id, end_id  FROM message_sending_times WHERE device_id = %s', (device_id,))
                  data  = self.cursor.fetchall()
                  return data
            
            except Exception as e:
                  username = self.device_model.selectUsername(device_id)
                  self.notification_fn.send_error2(e, "スタートIDとエンドIDの取得に失敗しました。再度スクリプトを実行します。", username)
                  self.error_operation.restart_app(driver)
                  

      
      
      def getEndId(self,device_id, driver):
      
       
            data = self.selectStartAndEndId(device_id, driver)
            end_id = ""
            
            if data:
                  end_id = data[0][1]
                  
            return end_id
      
      def IncreaseEndId(self, device_id):
      
            try:
                  self.cursor.execute('UPDATE message_sending_times SET end_id = end_id + 1 WHERE device_id = %s', (device_id,))
                  self.db.conn.commit()  # 変更を永続化
                  
            except Exception as e:
                  username = self.device_model.selectUsername(device_id)
                  self.notification_fn.send_error(e, f"end_idの更新に失敗しました。手動でデータベースの値を更新しもう一度スクリプトを実行してください。device_id: {device_id}", username)
                  sys.exit()  
        
      def updateEndId(self, device_id, driver):
            
      
            try:
                  self.cursor.execute('UPDATE message_sending_times SET end_id = 0 WHERE device_id = %s', (device_id,))
                  self.db.conn.commit()  # 変更を永続化
                  
            except Exception as e:
                  username = self.device_model.selectUsername(device_id)
                  self.notification_fn.send_error2(e, "エンドIDの更新に失敗しました。再度スクリプトを実行します。", username)
                  self.error_operation.restart_app(driver)
        