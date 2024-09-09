from functions.DBconnect import DBconnect
from functions.Notification import Notification
from functions.ErrorOperation import ErrorOperation
from models.Device import Device

class RegistrationMsg: 
    def __init__(self):
        self.db = DBconnect()
        self.cursor = None
        self.notification_fn = Notification()
        self.error_operation = ErrorOperation()
        self.device_model = Device()
        self.cursor = self.db.dbconnection()
        
        
    def getMessage(self, device_id, driver):
        
        
            
        try:
            self.cursor.execute('SELECT message FROM registration_messages WHERE device_id = %s', (device_id,))
            data  = self.cursor.fetchall()
            return data
        
        except Exception as e:
            username = self.device_model.selectUsername(device_id)
            self.notification_fn.send_error2(e, "URLの取得に失敗しました。再度スクリプトを実行します。", username)
            self.error_operation.restart_app(driver)
            
    
    def close(self):
        self.db.close()  # デストラクタでデータベース接続を閉じる
        

        
        