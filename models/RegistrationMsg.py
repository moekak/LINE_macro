from functions.DBconnet import DBconnect

class RegistrationMsg: 
    def __init__(self):
        self.db = DBconnect()
        self.cursor = self.db.dbconnection()
        
    def getMessage(self, device_id):
        self.cursor.execute('SELECT message FROM registration_messages WHERE device_id = %s', (device_id,))
        data  = self.cursor.fetchall()
        return data
    
    def close(self):
        self.db.close()  # デストラクタでデータベース接続を閉じる
        

        
        