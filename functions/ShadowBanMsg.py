from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from functions.Notification import Notification
from functions.GetElments import GetElements

class ShadowBanMsg:
    
    def __init__(self) -> None:
        self.notification_fn = Notification()
        self.get_elements_fn = GetElements()
    def sendMessageToAdmin(self, wait, driver):
        try:

            element  = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="0"]')))
            element.click()
            
            # トークボタンをクリックする(トーク画面が開く)
            self.get_elements_fn.click_talk_btn(wait, driver)

            # メッセージを送信する
            self.get_elements_fn.send_msg(wait, "シャードーバン確認メッセージ", driver)
            
            # メッセージ送信ボタンを押す
            self.get_elements_fn.click_send_msg_btn(wait, driver)

            # トーク画面を退出する
            self.get_elements_fn.click_leave_talk_btn(wait, driver)
            
            # ホームアイコンをクリックし、ホームに戻る
            self.get_elements_fn.click_home_btn(wait, driver)
            
            # 友達リストをクリックする
            self.get_elements_fn.click_friend_list_btn(wait, driver)
        except Exception as e:
            print(e)