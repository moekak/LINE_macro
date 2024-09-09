import requests
from requests.exceptions import RequestException

class LineNotify:
      def send_line_notify(self, notification_message):
            """
            LINEに通知する
            """
            line_notify_token = 'dWo5BJdQBgxWzdaSm9bAL3QKTCF0zzlkzt8NaVcoGsX'  # アクセストークンをここに入力
            line_notify_api = 'https://notify-api.line.me/api/notify'
            headers = {'Authorization': f'Bearer {line_notify_token}'}
            data = {'message': notification_message}
            try:
                  response = requests.post(line_notify_api, headers=headers, data=data, timeout=10 )
                  return response.status_code, response.text
            except ConnectionError:
                  print("接続に失敗しました。ネットワーク接続を確認してください。")
            except requests.exceptions.Timeout:
                  print("リクエストがタイムアウトしました。")
            except Exception as e:
                  print(e)
      
      def send_line_notify2(self, notification_message):
            """
            LINEに通知する
            """
            line_notify_token = '66bnOmQT9jDtvHm64EIG4hXQAANqQWa5hvyvtedNu76'  # アクセストークンをここに入力
            line_notify_api = 'https://notify-api.line.me/api/notify'
            headers = {'Authorization': f'Bearer {line_notify_token}'}
            data = {'message': notification_message}
            try:
                  response = requests.post(line_notify_api, headers=headers, data=data, timeout=10 )
                  return response.status_code, response.text
            except ConnectionError:
                  print("接続に失敗しました。ネットワーク接続を確認してください。")
            except requests.exceptions.Timeout:
                  print("リクエストがタイムアウトしました。")
            except Exception as e:
                  print(e)
      
      
      def send_line_notify3(self, notification_message):
            """
            LINEに通知する
            """
            line_notify_token = 'srCfbctFc0JawlxfsALOyDqexqgZ48a9BtiqGB2VVkW'  # アクセストークンをここに入力
            line_notify_api = 'https://notify-api.line.me/api/notify'
            headers = {'Authorization': f'Bearer {line_notify_token}'}
            data = {'message': notification_message}
            try:
                  response = requests.post(line_notify_api, headers=headers, data=data, timeout=10 )
                  return response.status_code, response.text
            except ConnectionError:
                  print("接続に失敗しました。ネットワーク接続を確認してください。")
            except requests.exceptions.Timeout:
                  print("リクエストがタイムアウトしました。")
            except Exception as e:
                  print(e)
      
            
