from functions.DBconnet import DBconnect
from functions.Notification import Notification
import sys

class FriendCount: 
    def __init__(self):
        self.db = DBconnect()
        self.notification_fn = Notification()
        self.cursor = self.db.dbconnection()
    
    def close(self):
        self.db.close()  # デストラクタでデータベース接続を閉じる
        
    def updateCount(self, device_id):
        try:
            self.cursor.execute('UPDATE friend_counts SET count = count + 1 WHERE device_id = %s', (device_id,))
            self.db.conn.commit()  # 変更を永続化
            
        except Exception as e:
            self.notification_fn.send_error(e, "データベースの友達数更新に失敗しました、手動で更新してください。")
            print(f"An error occurred: {e}")
            sys.exit()
            
    def selectCount(self, device_id):
        self.cursor.execute('SELECT count FROM friend_counts WHERE device_id = %s', (device_id,))
        count_tuple = self.cursor.fetchone()
        if count_tuple:
            count = count_tuple[0]  # Extract the integer value from the tuple
            return int(count)  # Return as an integer
        else:
            return None  # or some default value, e.g., 0 if no count is found
    
            
        

        