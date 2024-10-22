import os
from dotenv import load_dotenv
import mysql.connector
from functions.Notification import Notification
from functions.ErrorOperation import ErrorOperation

# .env ファイルを読み込む
load_dotenv()

class DBconnect: 
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.notification = Notification()
        self.error_operation = ErrorOperation()

    def dbconnection(self): 
        try:
            self.conn = mysql.connector.connect(
                host=os.getenv('HOST'),
                user=os.getenv('USER'),
                password=os.getenv('PASSWORD'),
                database=os.getenv('DATABASE'),
                connection_timeout=28800
            )
            
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            self.conn.ping(reconnect=True)
            return self.cursor
        except mysql.connector.Error as err:
            self.notification.send_error2(err, "データベース接続でエラーが起こりました。マクロが止まっています", "未取得")
            
            self.close() 

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
