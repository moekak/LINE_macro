
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time
from functions.Notification import Notification
import os
import sys



class GetElements:
    def __init__(self) -> None:
        self.notification_fn = Notification()

    # トーク画面でメッセージを送信する処理
    def sendMessage(self, wait, msg, url, driver):
        for _ in range(5):  # リトライ回数
            try:
                # 一斉配信一通目を送信
                self.send_msg(wait, msg, driver)
                self.click_send_msg_btn(wait, driver)
                
                # 一斉配信二通目を送信
                self.send_msg(wait, url, driver)
                self.click_send_msg_btn(wait, driver)

                break
            except StaleElementReferenceException:
                print("Element is stale, retrying...")
            except Exception as e:
                self.restart_app(driver)


    def sendGroupMsg(self, wait, msg, fn, device_id, url, id, driver):
        
        print(url)
   

        # トークボタンをクリックする(トーク画面が開く)
        self.click_talk_btn(wait, driver)

        # メッセージを送信する
        self.sendMessage(wait, msg, url, driver)
        # end_idを更新する
        fn.IncreaseEndId(device_id)

        # トーク画面を退出する
        self.click_leave_talk_btn(wait, driver)

        # ホームアイコンをクリックし、ホームに戻る
        self.click_home_btn(wait, driver)



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
        
    def find_element_with_scroll(self, driver, by, value):
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
                self.notification_fn.send_error(e, "友達リストスクロール中にエラーが発生しました。")

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


    def retry_click(self,wait, by, value, retries=3, delay=2):
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
                    print(value)
                    return False, e
                
    def retry_send_msg(self,wait, by, value, message, retries=3, delay=2):
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


    #ユーザーのプロファイル画面からトークボタンをクリックする(トーク画面が開く) 
    def click_talk_btn(self, wait, driver):
        is_success, error = self.retry_click(wait, By.XPATH, '(//android.widget.ImageView[@resource-id="jp.naver.line.android:id/user_profile_button_icon"])[1]')
        if not is_success:
            self.notification_fn.send_error(error, f"トークボタンの要素が見つかりませんでした。アプリを再起動して再度スクリプトを実行します。")
            self.restart_app(driver)

    # トーク画面でメッセージを送信する
    def send_msg(self,wait, msg, driver):


        is_success, error = self.retry_send_msg(wait, By.XPATH, '//android.widget.EditText[@content-desc="メッセージを入力"]', msg)

        if not is_success:
            self.notification_fn.send_error(error, f"ユーザーにメッセージが送信できませんでした。アプリを再起動して再度スクリプトを実行します。")
            self.restart_app(driver)

    #メッセージ送信ボタンをクリックする
    def click_send_msg_btn(self,wait, driver):
        is_success, error = self.retry_click(wait, By.XPATH, '//android.widget.ImageView[@content-desc="送信"]')
        if not is_success:
            self.notification_fn.send_error(error, f"メッセージ送信ボタンの要素が見つかりませんでした。アプリを再起動して再度スクリプトを実行します。")
            self.restart_app(driver)

    # トーク画面を退出する
    def click_leave_talk_btn(self,wait, driver):
        is_success, error = self.retry_click(wait, By.XPATH, '//android.widget.ImageView[@resource-id="jp.naver.line.android:id/header_up_button"]')
        if not is_success:
            self.notification_fn.send_error(error, f"トーク退出ボタンの要素が見つかりませんでした。アプリを再起動して再度スクリプトを実行します。")
            self.restart_app(driver)

    #ホームアイコンをクリックする
    def click_home_btn(self,wait, driver):
        is_success, error = self.retry_click(wait, By.XPATH, '//android.view.View[@content-desc="ホームタブ"]')
        if not is_success:
            self.notification_fn.send_error(error, f"ホームタブの要素が見つかりませんでした。アプリを再起動して再度スクリプトを実行します。")
            self.restart_app(driver)
    
    #友達リストのボタンをクリックする
    def click_friend_list_btn(self,wait, driver):
        is_sucess, error = self.retry_click(wait, By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="友だち"]')
        if not is_sucess:
            self.notification_fn.send_error(error, f"友達リストの要素が見つかりませんでした。アプリを再起動して再度スクリプトを実行します。")
            self.restart_app(driver)
            
            
   


    def restart_app(self,driver):
        # LINEアプリのパッケージ名とアクティビティ名を設定
        package_name = 'jp.naver.line.android'
        
        # アプリを停止
        driver.terminate_app(package_name)
        
        # 少し待機
        time.sleep(2)
        
        # アプリを再起動
        driver.activate_app(package_name)
        time.sleep(4)
        
         # スクリプトを再実行
        self.restart_script()
        
    def restart_script(self):
        print("Restarting script...")
        python = sys.executable
        os.execl(python, python, *sys.argv)