from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import StaleElementReferenceException




class RegistrationMsgFn:

    def sendMessageToNewFriends(self,username, wait, driver, device_id, get_elements_fn, notification_fn, error_operation,reg_msg_model,url_model, friend_model,hasMsg):
        count = 0

        while True:
            try:
            
                if count > 0:
                    is_sucess, error = get_elements_fn.retry_click(wait, By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="友だち"]')
                    if not is_sucess:
                        notification_fn.send_error2(error, f"友達リストの要素が見つかりませんでした。", username)
                      
                    
                time.sleep(3)
                elements_friend = driver.find_elements(By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="知り合いかも？"]')
            
                if elements_friend:
                  
                    # error
                    friend_count = friend_model.selectCount(device_id, driver, username)
                    if friend_count <= 9:
                        new_name = f"0{friend_count + 1}"
                    else:
                        new_name = f"{friend_count + 1}"
                        
                    print(f"新しいIDは{new_name}です")
                
   
                    # 知り合いかも？のユーザーを選択する
                    elements_friend[0].click()
        
                    # 知り合いかも？のリストの一番下までスクロールする
                    get_elements_fn.scroll_to_bottom(driver)
                    try:
                        elements = driver.find_elements(By.XPATH, '(//android.view.ViewGroup[@resource-id="jp.naver.line.android:id/bg"])')

                        elements[-1].click()

                    except StaleElementReferenceException:
    
                        notification_fn.send_error3("知り合いかも？のリストの一番下までスクロール失敗", username)
                        element = get_elements_fn.find_element_with_retry(driver, By.XPATH, '(//android.view.ViewGroup[@resource-id="jp.naver.line.android:id/bg"])[2]')
                        element.click()

                    # 追加ボタンを押す
                    is_sucess, error = get_elements_fn.retry_click(wait, By.XPATH, '//android.widget.LinearLayout[@resource-id="jp.naver.line.android:id/user_profile_button_area"]/android.view.ViewGroup[1]')
                    if not is_sucess:
                        notification_fn.send_error2(error, f"友達追加ボタンの要素が見つかりませんでした。{username}の新規友達追加に失敗しました。もう一度最初から実行し直してください。", username)
                        error_operation.restart_app(driver)

                    # データベースの友達の数を増やす
                    friend_model .updateCount(device_id, driver, username)
                    
                    # ユーザーの名前を取得する
                    element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/user_profile_name"]')))
                    
                    if element: 
                        username = element.get_attribute("text")
                    else:
                        username = ""
                    
                    #名前を変更するボタン(鉛筆マーク)をクリックする
                    is_sucess, error = get_elements_fn.retry_click(wait, By.XPATH, '//android.widget.ImageView[@content-desc="表示名の変更"]')
                    if not is_sucess:
                        
                        notification_fn.send_error2(error, f"ユーザーネーム変更ボタン(鉛筆マーク)の要素が見つかりませんでした。名前の更新ができていません。名前、{username}を{str(new_name)}へ手動で変更しメッセージを送ってください。", username)
                        error_operation.restart_app(driver)
                    
                    try:
                        element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.EditText[@resource-id="jp.naver.line.android:id/edit_name"]')))
                        element.click()
                    except Exception as e:
                        
                        notification_fn.send_error2(e, f"ユーザーネーム変更ボタンの要素が見つかりませんでした。名前の更新ができていません。名前、{username}を{str(new_name)}へ手動で変更しメッセージを送ってください。", username)
                        error_operation.restart_app(driver)

       
                    try:
                        # 既存の名前を削除する
                        element.send_keys(Keys.END)
                        # 名前を任意の番号に変更する
                        element.send_keys(str(new_name))
                
                        #名前を変更する(保存ボタンを押す)
                        element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/save_button"]')))
                        element.click()
                    except Exception as e:

                        
                        notification_fn.send_error2(e, f"ユーザーネーム変更ボタンの要素が見つかりませんでした。名前の更新ができていません。名前、{username}を{str(new_name)}へ手動で変更しメッセージを送ってください。", username)
                        error_operation.restart_app(driver)


                    #ユーザーのプロファイル画面からトークボタンをクリックする(トーク画面が開く) 
                    # todotodotodo
                    is_success, error = get_elements_fn.retry_click(wait, By.XPATH, '(//android.widget.ImageView[@resource-id="jp.naver.line.android:id/user_profile_button_icon"])[1]')
                    if not is_success:
                        
                        notification_fn.send_error2(error, f"トークボタンの要素が見つかりませんでした。メッセージが送信できていません。名前、{str(new_name)}へ手動でメッセージを送信してください。", username)
                        error_operation.restart_app(driver)
                        
              
                    message_url = url_model.selectURL(device_id, driver, username)
        
                    # メッセージ取得
                    messages = reg_msg_model.getMessage(device_id, driver, username)
                    message_template = ""
                    for msg in messages:
                        message_template = msg[0]
                        
           
                    
                    # 一つ目のメッセージを送信する
                    if username != "":
                        message_txt = message_template.replace('{Nickname}', username)
                    else:
                        message_txt = message_template.replace('{Nickname}', "")
                        message_txt = message_template.replace('様に', "")
                    is_success, error = get_elements_fn.retry_send_msg(wait, By.XPATH, '//android.widget.EditText[@content-desc="メッセージを入力"]', message_txt)
                    if not is_success:
                        
                        
                        notification_fn.send_error2(error, f"ユーザーにメッセージが送信できませんでした。名前、{str(new_name)}へ手動でメッセージを送信してください。", username)
                        error_operation.restart_app(driver)


                    # 送信ボタンをクリックする
                    is_success, error = get_elements_fn.retry_click(wait, By.XPATH, '//android.widget.ImageView[@content-desc="送信"]')
                    if not is_success:
                        
                        notification_fn.send_error2(error, f"ユーザーにメッセージが送信できませんでした。名前、{str(new_name)}へ手動でメッセージを送信してください。", username)
                        error_operation.restart_app(driver)


                    # 二つ目のメッセージを送信する
                    is_success, error = get_elements_fn.retry_send_msg(wait, By.XPATH, '//android.widget.EditText[@content-desc="メッセージを入力"]', message_url)
                    if not is_success:
                        
                        notification_fn.send_error2(error, f"ユーザーに二通目のメッセージが送信できませんでした。名前、{str(new_name)}へ手動で二通目のメッセージを送信してください。", username)
                        error_operation.restart_app(driver)
                    
                    # 送信ボタンをクリックする
                    is_success, error = get_elements_fn.retry_click(wait, By.XPATH, '//android.widget.ImageView[@content-desc="送信"]')
                    if not is_success:
                        
                        notification_fn.send_error2(error, f"ユーザーに二通目のメッセージが送信できませんでした。名前、{str(new_name)}へ手動で二通目のメッセージを送信してください。", username)
                        error_operation.restart_app(driver)

                    is_success, error = get_elements_fn.retry_click(wait, By.XPATH, '//android.widget.ImageView[@resource-id="jp.naver.line.android:id/header_up_button"]')
                    if not is_success:
                        
                        notification_fn.send_error2(error, f"トーク退出ボタンの要素が見つかりませんでした。新規ユーザーの追加、メッセージ送信は完了しています。", username)
                        error_operation.restart_app(driver)


                    
                    #ホームボタン押す
                    is_success, error = get_elements_fn.retry_click(wait, By.XPATH, '//android.view.View[@content-desc="ホームタブ"]')
                    if not is_success:
                        
                        notification_fn.send_error2(error, f"ホームタブの要素が見つかりませんでした。新規ユーザーの追加、メッセージ送信は完了しています。", username)
                        error_operation.restart_app(driver)
                    
                    count += 1

                else:
                    if hasMsg == True:
                        get_elements_fn.click_leave_talk_btn(wait, driver, username)
                    break
            except Exception as e:
                
                notification_fn.send_error2(e, "sendMessageToNewFriends()でエラーが発生しました。", username)
                error_operation.restart_app(driver)
                
           
    
    
    
    
                
           
            
        
        
            