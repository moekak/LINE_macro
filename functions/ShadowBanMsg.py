from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ShadowBanMsg:

    def sendMessageToAdmin(self, wait, driver, username, get_elements_fn):
        try:

            element  = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="0"]')))
            element.click()
            
            # トークボタンをクリックする(トーク画面が開く)
            get_elements_fn.click_talk_btn(wait, driver, username)

            # メッセージを送信する
            get_elements_fn.send_msg(wait, "シャードーバン確認メッセージ", driver, username)
            
            # メッセージ送信ボタンを押す
            get_elements_fn.click_send_msg_btn(wait, driver, username)

            # トーク画面を退出する
            get_elements_fn.click_leave_talk_btn(wait, driver, username)
            
            # ホームアイコンをクリックし、ホームに戻る
            get_elements_fn.click_home_btn(wait, driver, username)
            
            # 友達リストをクリックする
            get_elements_fn.click_friend_list_btn(wait, driver, username)
        except Exception as e:
            print(e)