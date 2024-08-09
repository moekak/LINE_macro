from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from models.FriendCount import FriendCount
from selenium.common.exceptions import StaleElementReferenceException
from functions.Notification import Notification
from functions.GetElments import GetElements
import sys


class RegistrationMsgFn:
    def __init__(self) -> None:
        self.notification_fn = Notification()
        self.get_elements_fn = GetElements()
    
    
    def sendMessageToNewFriends(self, wait, driver, device_id, fn, message_url, fn2, hasMsg):
        count = 0
        
        # メッセージ取得
        messages = fn.getMessage(device_id)
        message = ""
        for msg in messages:
            message = msg[0]
            
        while True:
            try:
            
                if count > 0:
                    is_sucess, error = self.get_elements_fn.retry_click(wait, By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="友だち"]')
                    if not is_sucess:
                        self.notification_fn.send_error(error, f"友達リストの要素が見つかりませんでした。")
                        print("no")
                        break
                    
                time.sleep(2)
                elements = driver.find_elements(By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="知り合いかも？"]')
            
                if elements:
                    
                    friend_model = FriendCount()
                    friend_count = friend_model.selectCount(device_id)
                    new_name = friend_count + 1
                    print("find friend")
                    
                    # 知り合いかも？のユーザーを選択する
                    elements[0].click()
        
                    # 知り合いかも？のリストの一番下までスクロールする
                    fn2.scroll_to_bottom(driver)
                    try:
                        elements = driver.find_elements(By.XPATH, '(//android.view.ViewGroup[@resource-id="jp.naver.line.android:id/bg"])')
                        print(len(elements))
                        
                        elements[-1].click()

                    except StaleElementReferenceException:
                        element = fn2.find_element_with_retry(driver, By.XPATH, '(//android.view.ViewGroup[@resource-id="jp.naver.line.android:id/bg"])[2]')
                        element.click()

                    # ユーザーの名前を取得する
                    element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/user_profile_name"]')))
                    username = element.get_attribute("text")
                    print(username)
                        
                    # 追加ボタンを押す
                    is_sucess, error = self.get_elements_fn.retry_click(wait, By.XPATH, '//android.widget.LinearLayout[@resource-id="jp.naver.line.android:id/user_profile_button_area"]/android.view.ViewGroup[1]')
                    if not is_sucess:
                        self.notification_fn.send_error(error, f"友達追加ボタンの要素が見つかりませんでした。{username}の新規友達追加に失敗しました。もう一度最初から実行し直してください。")
                        sys.exit()

                    # データベースの友達の数を増やす
                    friend_model.updateCount(device_id)
                    
                    #名前を変更するボタン(鉛筆マーク)をクリックする
                    is_sucess, error = self.get_elements_fn.retry_click(wait, By.XPATH, '//android.widget.ImageView[@content-desc="表示名の変更"]')
                    if not is_sucess:
                        self.notification_fn.send_error(error, f"ユーザーネーム変更ボタンの要素が見つかりませんでした。名前の更新ができていません。名前、{username}を{str(new_name)}へ手動で変更しメッセージを送ってください。")
                        sys.exit()
                    
                    try:
                        element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.EditText[@resource-id="jp.naver.line.android:id/edit_name"]')))
                        element.click()
                    except Exception as e:
                        self.notification_fn.send_error(e, f"ユーザーネーム変更ボタンの要素が見つかりませんでした。名前の更新ができていません。名前、{username}を{str(new_name)}へ手動で変更しメッセージを送ってください。")
                        sys.exit()

       
                    try:
                        # 既存の名前を削除する
                        element.send_keys(Keys.END)
                        # 名前を任意の番号に変更する
                        element.send_keys(str(new_name))
                
                        #名前を変更する(保存ボタンを押す)
                        element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/save_buttonnn"]')))
                        element.click()
                    except Exception as e:
                        self.notification_fn.send_error(e, f"ユーザーネーム変更ボタンの要素が見つかりませんでした。名前の更新ができていません。名前、{username}を{str(new_name)}へ手動で変更しメッセージを送ってください。")
                        sys.exit()


                    #ユーザーのプロファイル画面からトークボタンをクリックする(トーク画面が開く) 
                    is_success, error = self.get_elements_fn.retry_click(wait, By.XPATH, '(//android.widget.ImageView[@resource-id="jp.naver.line.android:id/user_profile_button_icon"])[1]')
                    if not is_success:
                        self.notification_fn.send_error(error, f"トークボタンの要素が見つかりませんでした。メッセージが送信できていません。名前、{str(new_name)}へ手動でメッセージを送信してください。")
                        sys.exit()
                    
                    
                    # 一つ目のメッセージを送信する
                    message_txt = f"{username}さん\n\n {message}"
                    is_success, error = self.get_elements_fn.retry_send_msg(wait, By.XPATH, '//android.widget.EditText[@content-desc="メッセージを入力"]', message_txt)
                    if not is_success:
                        self.notification_fn.send_error(error, f"ユーザーにメッセージが送信できませんでした。名前、{str(new_name)}へ手動でメッセージを送信してください。")
                        sys.exit()


                    # 送信ボタンをクリックする
                    is_success, error = self.get_elements_fn.retry_click(wait, By.XPATH, '//android.widget.ImageView[@content-desc="送信"]')
                    if not is_success:
                        self.notification_fn.send_error(error, f"ユーザーにメッセージが送信できませんでした。名前、{str(new_name)}へ手動でメッセージを送信してください。")
                        sys.exit()


                    # 二つ目のメッセージを送信する
                    is_success, error = self.get_elements_fn.retry_send_msg(wait, By.XPATH, '//android.widget.EditText[@content-desc="メッセージを入力"]', message_url)
                    if not is_success:
                        self.notification_fn.send_error(error, f"ユーザーに二通目のメッセージが送信できませんでした。名前、{str(new_name)}へ手動で二通目のメッセージを送信してください。")
                        sys.exit()
                    
                    # 送信ボタンをクリックする
                    is_success, error = self.get_elements_fn.retry_click(wait, By.XPATH, '//android.widget.ImageView[@content-desc="送信"]')
                    if not is_success:
                        self.notification_fn.send_error(error, f"ユーザーに二通目のメッセージが送信できませんでした。名前、{str(new_name)}へ手動で二通目のメッセージを送信してください。")
                        sys.exit()

                    is_success, error = self.get_elements_fn.retry_click(wait, By.XPATH, '//android.widget.ImageView[@resource-id="jp.naver.line.android:id/header_up_button"]')
                    if not is_success:
                        self.notification_fn.send_error(error, f"トーク退出ボタンの要素が見つかりませんでした。新規ユーザーの追加、メッセージ送信は完了しています。")
                        sys.exit()


                    
                    #ホームボタン押す
                    is_success, error = self.get_elements_fn.retry_click(wait, By.XPATH, '//android.view.View[@content-desc="ホームタブ"]')
                    if not is_success:
                        self.notification_fn.send_error(error, f"ホームタブの要素が見つかりませんでした。新規ユーザーの追加、メッセージ送信は完了しています。")
                        sys.exit()
                    
                    count += 1

                else:
                    print("no new friend")
                    if hasMsg == True:
                        self.get_elements_fn.click_leave_talk_btn(wait, driver)
                    break
            except Exception as e:
                self.notification_fn.send_error(e, "")
                
           
    
    
    
    
                
           
            
        
        
            