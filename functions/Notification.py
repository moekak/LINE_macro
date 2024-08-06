import traceback
from functions.LineNotify import LineNotify
from datetime import datetime
class Notification:

      def __init__(self):
            self.line_notify = LineNotify()
     
      def send_error(self, e, message):
            tb = traceback.extract_tb(e.__traceback__)
            # 最後のコールスタックを取得
            last_call_stack = tb[-1]
            file_name = last_call_stack.filename
            line_number = last_call_stack.lineno
            func_name = last_call_stack.name

            self.line_notify.send_line_notify(f"{message}.\n\nAn error occurred in file '{file_name}', line {line_number}, in function '{func_name}'.\nError message: {e}")

      def send_msg_sendingTime(self):
            start = datetime.now().replace(microsecond=0)
            message = f"一斉メッセージ送信を開始します。\n\n 開始時間：({start})"
            self.line_notify.send_line_notify(message)


      def send_msg_emdTime(self, end):
            message = f"一斉メッセージ送信が完了しました。\n\n 開始時間：({end})"
            self.line_notify.send_line_notify(message)

      

