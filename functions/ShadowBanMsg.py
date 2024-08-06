from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from functions.Notification import Notification

class ShadowBanMsg:
    
    def __init__(self) -> None:
        self.notification_fn = Notification
    def sendMessageToAdmin(self,wait):
        try:
            element  = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="0"]')))
            element.click()
            
            # トークボタンをクリックする(トーク画面が開く)
            talk_btn_element = wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.ImageView[@resource-id="jp.naver.line.android:id/user_profile_button_icon"])[1]')))
            talk_btn_element.click()
            
            element_textarea = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.EditText[@content-desc="メッセージを入力"]')))
            element_textarea.send_keys("シャードーバン確認メッセージ")
            element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[@content-desc="送信"]')))
            element.click()
            # トーク画面を退出する
            leave_talk_element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[@resource-id="jp.naver.line.android:id/header_up_button"]')))
            leave_talk_element.click()
            

            # ホームアイコンをクリックし、ホームに戻る
            home_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="ホームタブ"]')))
            home_btn.click()
            
            element  = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="友だち"]')))
            element.click()
        except Exception as e:
            self.notification_fn(e, "")