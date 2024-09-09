import os
from dotenv import load_dotenv
import mysql.connector

# .env ファイルを読み込む
load_dotenv()

class DBconnect: 
    def __init__(self):
        self.conn = None
        self.cursor = None

    def dbconnection(self): 
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

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
