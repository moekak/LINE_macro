from functions.DBconnect import DBconnect
from functions.Notification import Notification

class Device: 
    def __init__(self):
        self.db = DBconnect()
        self.notification_fn = Notification()
        self.cursor = self.db.dbconnection()

    
    def close(self):
        self.db.close()  # デストラクタでデータベース接続を閉じる
        
    def selectUsername(self, device_id):
          
        try:
            # デバイスIDに基づいてアカウント名を取得
            self.cursor.execute('SELECT account_name FROM devices WHERE id = %s', (device_id,))
            name_data = self.cursor.fetchone()

            if name_data:
                name = name_data[0]  # Extract the name value from the tuple
                return name
            else:
                return None  # or some default value if no result is found
        except Exception as db_err:
            return None
            
                

    