from functions.DBconnect import DBconnect
from functions.Notification import Notification
from functions.ErrorOperation import ErrorOperation
import sys, datetime
from models.Device import Device

class FriendCount: 
    def __init__(self):
        self.db = DBconnect()
        self.notification_fn = Notification()
        self.device_model = Device()
        self.cursor = self.db.dbconnection()
        self.error_operation = ErrorOperation()
    
    def close(self):
        self.db.close()  # デストラクタでデータベース接続を閉じる
        
    def updateCount(self, device_id, driver, username):
          
        try:
            today = datetime.date.today()
            if self.hasFriendCount(device_id,today, driver, username) == False:
                self.cursor.execute('INSERT INTO friend_counts (device_id, count) VALUES (%s, %s)', (device_id, 1))
                self.db.conn.commit()  # 変更を永続化
            else:
                self.cursor.execute('UPDATE friend_counts SET count = count + 1 WHERE device_id = %s AND DATE(created_at) = %s', (device_id, today))
                self.db.conn.commit()  # 変更を永続化
            
        except Exception as e:
            self.notification_fn.send_error2(e, "データベースの友達数更新に失敗しました、手動で更新してください。マクロは停止されています。", username)
            print(f"An error occurred: {e}")
            sys.exit()
            
    def selectCount(self, device_id, driver, username):
             
        try:
            self.cursor.execute('SELECT SUM(count) total_count FROM friend_counts WHERE device_id = %s', (device_id,))
            count_tuple = self.cursor.fetchone()
            if count_tuple:
                count = count_tuple[0]  
                return int(count) 
            else:
                return None 
        
        except Exception as e:
            self.notification_fn.send_error2(e, self.cursor, username)
            self.notification_fn.send_error2(e, "友達の数の取得に失敗しました。再度スクリプトを実行します。", username)
            self.error_operation.restart_app(driver)

    def getDate(self, device_id, driver, username):
        
        try:
            
            self.cursor.execute('SELECT created_at FROM friend_counts WHERE device_id = %s', (device_id,))
            dates = self.cursor.fetchall() # 全ての結果を取得
            
            date_list = []

            # 取得した日付部分をリストに追加
            for record in dates:
                created_at = record[0].date()
                date_list.append(created_at)

            if not date_list:
                print("no new friend")
            

            return date_list
       
            
        except Exception as e:
            self.notification_fn.send_error2(e, "日付の取得に失敗しました。再度スクリプトを実行します。", username)
            self.error_operation.restart_app(driver)
            

    def hasFriendCount(self, device_id, today, driver, username):
        
        date_list = self.getDate(device_id, driver, username)

        for date in date_list:
            if date == today:
                return True
        
        return False
            


    
    