from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from models.FriendCount import FriendCount
from selenium.common.exceptions import StaleElementReferenceException
from functions.Notification import Notification


class RegistrationMsgFn:
    def __init__(self) -> None:
        self.notification_fn = Notification()
    
    
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
                    element  = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="友だち"]')))
                    element.click()
                    
                time.sleep(2)
                elements = driver.find_elements(By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="知り合いかも？"]')
            
                if elements:
                    
                    friend_model = FriendCount()
                    friend_count = friend_model.selectCount(device_id)
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
                        
                    # 追加ボタンを押す
                    element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.LinearLayout[@resource-id="jp.naver.line.android:id/user_profile_button_area"]/android.view.ViewGroup[1]')))
                    element.click()
                    
                    #名前を変更するボタン(鉛筆マーク)をクリックする
                    element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[@content-desc="表示名の変更"]')))
                    element.click()
                    
                    
                    # 既存の名前を消す
                    element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.EditText[@resource-id="jp.naver.line.android:id/edit_name"]')))
                    element.click()
                    
                    existing_text = element.get_attribute("text")
                    
                    print(existing_text)
                    # 既存の名前を削除
                    element.send_keys(Keys.END)
                    
                    new_name = friend_count + 1
                    element.send_keys(str(new_name))
            
                    #名前を変更する(保存ボタンを押す)
                    element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/save_button"]')))
                    element.click()
                    
                    
                    
                    # メッセージ送信ボタンを押す
                    element = wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.ImageView[@resource-id="jp.naver.line.android:id/user_profile_button_icon"])[1]')))
                    element.click()
                    
                    txtarea = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.EditText[@content-desc="メッセージを入力"]')))
                    
                    message_txt = f"{existing_text}さん\n\n {message}"
                    txtarea.send_keys(message_txt)
                    
                    submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[@content-desc="送信"]')))
                    submit_btn.click()
                    
                    txtarea.send_keys(message_url)
                    submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[@content-desc="送信"]')))
                    submit_btn.click()
                    
                    #メッセージ送信完了したときに戻るボタン
                    element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[@resource-id="jp.naver.line.android:id/header_up_button"]')))
                    element.click()
                    
                    #ホームボタン押す
                    element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="ホームタブ"]')))
                    element.click()
                    
                    friend_model.updateCount(device_id)
                    
                    time.sleep(5)

                    #  # 新規友達追加した人がいるかの確認
                    # element = wait.until(EC.presence_of_element_located((By.ID, 'jp.naver.line.android:id/layout')))
                    # element.click()
                    # # 知り合いかも？のユーザーがいるか探す
                    
                    count += 1
                else:
                    print("no new friend")
                    if hasMsg == True:
                        element  = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[@resource-id="jp.naver.line.android:id/header_up_button"]')))
                        element.click()
                    break
            except Exception as e:
                self.notification_fn.send_error(e, "")
                
           
    
    
    
    
                
           
            
        
        
            