import traceback
from functions.LineNotify import LineNotify
from datetime import datetime
class Notification:

      def __init__(self):
            self.line_notify = LineNotify()
     
      def send_error(self, e, message, username):
            tb = traceback.extract_tb(e.__traceback__)
            # 最後のコールスタックを取得
            last_call_stack = tb[-1]
            file_name = last_call_stack.filename
            line_number = last_call_stack.lineno
            func_name = last_call_stack.name
            self.line_notify.send_line_notify(f"{message}.\n\n アカウント名: {username} \n\n An error occurred in file '{file_name}', line {line_number}, in function '{func_name}'.\nError message: {e}")
      
      def send_error2(self, e, message, username):

            tb = traceback.extract_tb(e.__traceback__)
            # 最後のコールスタックを取得
            last_call_stack = tb[-1]
            file_name = last_call_stack.filename
            line_number = last_call_stack.lineno
            func_name = last_call_stack.name
            self.line_notify.send_line_notify2(f"{message}.\n\n アカウント名: {username} \n\n An error occurred in file '{file_name}', line {line_number}, in function '{func_name}'.\nError message: {e}")

      
      def send_error3(self,message, username):
            self.line_notify.send_line_notify2(f"{message}.\n\n アカウント名: {username}")


      def send_msg_sendingTime(self, username):
            start = datetime.now().replace(microsecond=0)
            message = f"一斉メッセージ送信を開始します。\n\n 開始時間：({start})\n\n アカウント名: {username}"
            self.line_notify.send_line_notify(message)

      def send_msg_emdTime(self, end, username):
            message = f"一斉メッセージ送信が完了しました。\n\n 開始時間：({end})\n\n アカウント名: {username}"
            self.line_notify.send_line_notify(message)
            
      def send_confirmation_msg(self):
            try:
                  self.line_notify.send_line_notify3("確認メッセージ")
            except Exception as e:
                  print(f"マクロ確認メッセージが送れませんでした。{e}")
      

      

