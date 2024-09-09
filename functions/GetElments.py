
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time
from functions.Notification import Notification
import os
import sys
from models.Device import Device
from functions.ErrorOperation import ErrorOperation



class GetElements:
    def __init__(self) -> None:
        self.notification_fn = Notification()
        self.device_model = Device()
        self.error_operation = ErrorOperation()

    # トーク画面でメッセージを送信する処理
    def sendMessage(self, wait, msg, url, driver, device_id):
        for _ in range(5):  # リトライ回数
            try:
                # 一斉配信一通目を送信
                self.send_msg(wait, msg, driver, device_id)
                self.click_send_msg_btn(wait, driver, device_id)
                
                # 一斉配信二通目を送信
                self.send_msg(wait, url, driver, device_id)
                self.click_send_msg_btn(wait, driver, device_id)

                break
            except StaleElementReferenceException:
                print("Element is stale, retrying...")
            except Exception as e:
                self.error_operation.restart_app(driver)


    def sendGroupMsg(self, wait, msg, fn, device_id, url, id, driver):
        
        # トークボタンをクリックする(トーク画面が開く)
        self.click_talk_btn(wait, driver, device_id)

        # メッセージを送信する
        self.sendMessage(wait, msg, url, driver, device_id)
        # end_idを更新する
        fn.IncreaseEndId(device_id)
        # トーク画面を退出する
        self.click_leave_talk_btn(wait, driver, device_id)

        # ホームアイコンをクリックし、ホームに戻る
        self.click_home_btn(wait, driver, device_id)



    def swipe_up(self,driver):
        size = driver.get_window_size()
        start_y = size['height'] * 0.8  # 画面の下部80%の位置
        end_y = size['height'] * 0.2    # 画面の上部20%の位置
        start_x = size['width'] * 0.5   # 画面の中央
        driver.swipe(start_x, start_y, start_x, end_y, 800)  # スワイプ時間は800ms（1秒）

    def find_element_with_retry(driver, by, value, retries=5):
        for _ in range(retries):
            try:
                element = driver.find_element(by, value)
                return element
            except StaleElementReferenceException:
                time.sleep(1)
        
    def find_element_with_scroll(self, driver, by, value, device_id):
        previous_page_source = ''
        while True:
            try:
                element = driver.find_element(by, value)
                return element
            except NoSuchElementException:
                current_page_source = driver.page_source
                if current_page_source == previous_page_source:
                    return None
                previous_page_source = current_page_source
                self.swipe_up(driver)
                time.sleep(0.5)
                print("Scrolled up and retrying to find the element.")
            except Exception as e:
                username = self.device_model.selectUsername(device_id)
                self.notification_fn.send_error2(e, "友達リストスクロール中にエラーが発生しました。", username)
                self.error_operation.restart_app(driver)

    def scroll_to_bottom(self, driver):
        size = driver.get_window_size()
        start_y = size['height'] * 0.8  # スクリーンの下から80%の位置
        end_y = size['height'] * 0.2    # スクリーンの上から20%の位置
        start_x = size['width'] * 0.5   # スクリーンの横方向中央

        previous_page_source = ''
        while True:
            current_page_source = driver.page_source
            if current_page_source == previous_page_source:
                break  # これ以上スクロールできない場合
            previous_page_source = current_page_source
            driver.swipe(start_x, start_y, start_x, end_y, 200)  # スワイプ時間は1000ms（1秒）


    def retry_click(self,wait, by, value, retries=2, delay=1):
        for attempt in range(retries):
            try:
                element = wait.until(EC.presence_of_element_located((by, value)))
                element.click()
                return True, None
            except (TimeoutException, Exception) as e:
                if attempt < retries - 1:
                    print(f"Retry {attempt + 1}/{retries} failed: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print("All retries failed.")
                    return False, e

    def retry_find_element(self,wait, by, value, retries=2, delay=1):
        for attempt in range(retries):
            try:
                element = wait.until(EC.presence_of_element_located((by, value)))
                return element
            except (TimeoutException, Exception) as e:
                if attempt < retries - 1:
                    print(f"Retry {attempt + 1}/{retries} failed: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print("All retries failed.")
                    return None

    def retry_send_msg(self,wait, by, value, message, retries=2, delay=2):
        for attempt in range(retries):
            try:
                element = wait.until(EC.presence_of_element_located((by, value)))
                element.send_keys(message)
                
                return True, None
            except (TimeoutException, Exception) as e:
                if attempt < retries - 1:
                    print(f"Retry {attempt + 1}/{retries} failed: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print("All retries failed.")
                    return [False, e]
                
    
    def clickFriendListInput(self, wait, driver, device_id, userId):
        print(f"userId{userId}")
        input_field = self.retry_find_element(wait, By.XPATH, '//android.widget.EditText[@resource-id="jp.naver.line.android:id/searchbar_input_text"]')

        if input_field:
            input_field.send_keys(userId)
        else:
            username = self.device_model.selectUsername(device_id)
            self.notification_fn.send_error3(f"名前で検索するinput fieldが見つかりませんでした。アプリを再起動して再度スクリプトを実行します。", username)
            self.error_operation.restart_app(driver)

        



    #ユーザーのプロファイル画面からトークボタンをクリックする(トーク画面が開く) 
    def click_talk_btn(self, wait, driver, device_id):
        is_success, error = self.retry_click(wait, By.XPATH, '(//android.widget.ImageView[@resource-id="jp.naver.line.android:id/user_profile_button_icon"])[1]')
        if not is_success:
            username = self.device_model.selectUsername(device_id)
            self.notification_fn.send_error2(error, f"トークボタンの要素が見つかりませんでした。アプリを再起動して再度スクリプトを実行します。", username)
            self.error_operation.restart_app(driver)

    # トーク画面でメッセージを送信する
    def send_msg(self,wait, msg, driver, device_id):


        is_success, error = self.retry_send_msg(wait, By.XPATH, '//android.widget.EditText[@content-desc="メッセージを入力"]', msg)

        if not is_success:
            username = self.device_model.selectUsername(device_id)
            self.notification_fn(error, f"ユーザーにメッセージが送信できませんでした。アプリを再起動して再度スクリプトを実行します。", username)
            self.error_operation.restart_app(driver)

    #メッセージ送信ボタンをクリックする
    def click_send_msg_btn(self,wait, driver, device_id):
        is_success, error = self.retry_click(wait, By.XPATH, '//android.widget.ImageView[@content-desc="送信"]')
        if not is_success:
            username = self.device_model.selectUsername(device_id)
            self.notification_fn.send_error2(error, f"メッセージ送信ボタンの要素が見つかりませんでした。アプリを再起動して再度スクリプトを実行します。", username)
            self.error_operation.restart_app(driver)

    # トーク画面を退出する
    def click_leave_talk_btn(self,wait, driver, device_id):
        is_success, error = self.retry_click(wait, By.XPATH, '//android.widget.ImageView[@resource-id="jp.naver.line.android:id/header_up_button"]')
        if not is_success:
            username = self.device_model.selectUsername(device_id)
            self.notification_fn.send_error2(error, f"トーク退出ボタンの要素が見つかりませんでした。アプリを再起動して再度スクリプトを実行します。", username)
            self.error_operation.restart_app(driver)

    #ホームアイコンをクリックする
    def click_home_btn(self,wait, driver, device_id):
        is_success, error = self.retry_click(wait, By.XPATH, '//android.view.View[@content-desc="ホームタブ"]')
        if not is_success:
            username = self.device_model.selectUsername(device_id)
            self.notification_fn.send_error2(error, f"ホームタブの要素が見つかりませんでした。アプリを再起動して再度スクリプトを実行します。", username)
            self.error_operation.restart_app(driver)
    
    #友達リストのボタンをクリックする
    def click_friend_list_btn(self,wait, driver, device_id):
        is_sucess, error = self.retry_click(wait, By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="友だち"]')
        if not is_sucess:
            username = self.device_model.selectUsername(device_id)
            self.notification_fn.send_error2(error, f"友達リストの要素が見つかりませんでした。アプリを再起動して再度スクリプトを実行します。", username)
            self.error_operation.restart_app(driver)
            
    # profile画面で閉じるボタンを押す
    def click_close_btn(self, wait, device_id, driver):
        is_sucess, error = self.retry_click(wait, By.XPATH, '//android.widget.ImageView[@content-desc="閉じる"]')
        if not is_sucess:
            username = self.device_model.selectUsername(device_id)
            self.notification_fn.send_error2(error, f"プロファイル画面の閉じるボタンの要素が見つかりませんでした。。アプリを再起動して再度スクリプトを実行します。", username)
            self.error_operation.restart_app(driver)
                    
   


    # def restart_app(self,driver):
    #     # LINEアプリのパッケージ名とアクティビティ名を設定
    #     package_name = 'jp.naver.line.android'
        
    #     # アプリを停止
    #     driver.terminate_app(package_name)
        
    #     # 少し待機
    #     time.sleep(1)
        
    #     # アプリを再起動
    #     driver.activate_app(package_name)
    #     time.sleep(4)
        
    #      # スクリプトを再実行
    #     self.restart_script()
        
    # def restart_script(self):
    #     print("Restarting script...")
    #     # pythonファイルの特定をする
    #     python = sys.executable
    #     # 現在のプロセスを終(os.execl)
    #     os.execl(python, python, *sys.argv)