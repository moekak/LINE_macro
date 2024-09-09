from functions.DBconnect import DBconnect
from functions.ErrorOperation import ErrorOperation
from functions.Notification import Notification
from models.Device import Device

class MsgUrl: 
    def __init__(self):
        self.db = DBconnect()
        self.cursor = None
        self.error_operation = ErrorOperation()
        self.notification_fn = Notification()
        self.device_model = Device()
        self.cursor = self.db.dbconnection()
    
    def close(self):
        self.db.close()  # デストラクタでデータベース接続を閉じる
        
            
    def selectURL(self, device_id, driver):
                
        try:
                
            self.cursor.execute('SELECT url FROM message_urls WHERE device_id = %s', (device_id,))
            url_tuple = self.cursor.fetchone()
            if url_tuple:
                url = url_tuple[0]  # Extract the integer value from the tuple
                return url  # Return as an integer
            else:
                return None  # or some default value, e.g., 0 if no count is found
        
        except Exception as e:
            username = self.device_model.selectUsername(device_id)
            self.notification_fn.send_error2(e, "URLの取得に失敗しました。再度スクリプトを実行します。", username)
            self.error_operation.restart_app(driver)
    
            
        

        