from functions.DBconnet import DBconnect
from functions.Notification import Notification

class MsgSendingTimes: 
      def __init__(self):
            self.db = DBconnect()
            self.cursor = self.db.dbconnection()
     
      def close(self):
            self.db.close()  # デストラクタでデータベース接続を閉じる
            
      def updateFlag(self, device_id):
        try:
            self.cursor.execute('UPDATE message_sending_times SET is_sent = "1" WHERE device_id = %s', (device_id,))
            self.db.conn.commit()  # 変更を永続化
            
        except Exception as e:
            print(f"An error occurred: {e}")

      def selectStartAndEndId(self, device_id):
            try:
                  self.cursor.execute('SELECT start_id, end_id  FROM message_sending_times WHERE device_id = %s', (device_id,))
                  data  = self.cursor.fetchall()
                  return data
            
            except Exception as e:
                  print(f"An error occurred: {e}")
                  

            
      def getStartId(self,device_id):
            data = self.selectStartAndEndId(device_id)
            start_id = ""
            
            if data:
                  start_id = data[0][0]
                  
            return start_id
      
      def getEndId(self,device_id):
            data = self.selectStartAndEndId(device_id)
            end_id = ""
            
            if data:
                  end_id = data[0][1]
                  
            return end_id
      
      def IncreaseEndId(self, device_id):
        try:
            self.cursor.execute('UPDATE message_sending_times SET end_id = end_id + 1 WHERE device_id = %s', (device_id,))
            self.db.conn.commit()  # 変更を永続化
            
        except Exception as e:
              
            print(f"An error occurred: {e}")
        
      def updateEndId(self, device_id):
        try:
            self.cursor.execute('UPDATE message_sending_times SET end_id = 0 WHERE device_id = %s', (device_id,))
            self.db.conn.commit()  # 変更を永続化
            
        except Exception as e:
            print(f"An error occurred: {e}")
        