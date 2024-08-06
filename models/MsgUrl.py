from functions.DBconnet import DBconnect

class MsgUrl: 
    def __init__(self):
        self.db = DBconnect()
        self.cursor = self.db.dbconnection()
    
    def close(self):
        self.db.close()  # デストラクタでデータベース接続を閉じる
        
            
    def selectURL(self, device_id):
        self.cursor.execute('SELECT url FROM message_urls WHERE device_id = %s', (device_id,))
        url_tuple = self.cursor.fetchone()
        if url_tuple:
            url = url_tuple[0]  # Extract the integer value from the tuple
            return url  # Return as an integer
        else:
            return None  # or some default value, e.g., 0 if no count is found
    
            
        

        