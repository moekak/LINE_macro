
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from functions.Notification import Notification


class GetElements:
    def __init__(self) -> None:
        self.notification_fn = Notification()

    # トーク画面でメッセージを送信する処理
    def sendMessage(self, wait, msg, url):
        for _ in range(5):  # リトライ回数
            try:
                element_textarea = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.EditText[@content-desc="メッセージを入力"]')))
                element_textarea.clear()  # テキストエリアのクリア
                element_textarea.send_keys(msg)
                element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[@content-desc="送信"]')))
                element.click()
                element_textarea.send_keys(url)
                element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[@content-desc="送信"]')))
                element.click()
                break
            except StaleElementReferenceException:
                print("Element is stale, retrying...")
            except Exception as e:
                self.notification_fn(e, "")


    def sendGroupMsg(self, wait, msg, fn, device_id, url, id):
        
        print(url)
        try:

            # トークボタンをクリックする(トーク画面が開く)
            talk_btn_element = wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.ImageView[@resource-id="jp.naver.line.android:id/user_profile_button_icon"])[1]')))
            talk_btn_element.click()
        except Exception as e:
            self.notification_fn.send_error(e, f"一斉配信中にエラーが発生しました。友達: {id}にメッセージが送れていません。")

        try:
            self.sendMessage(wait, msg, url)

            # トーク画面を退出する
            leave_talk_element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[@resource-id="jp.naver.line.android:id/header_up_button"]')))
            leave_talk_element.click()
        except Exception as e:
            self.notification_fn.send_error(e, f"一斉配信中にエラーが発生しました。友達: {id}にメッセージが送れていない可能性があります。")
            
        
        # end idの更新
        try:
            fn.IncreaseEndId(device_id)
        except Exception as e:
            self.notification_fn.send_error(e, f"一斉配信中にエラーが発生しました。友達: {id}にメッセージは遅れていますが、データーベースのカウントが更新されていません。手動で更新してください。")

        # ホームアイコンをクリックし、ホームに戻る
        home_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="ホームタブ"]')))
        home_btn.click()

    def getFriendsCount(self, wait):
        # element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/count" and @text="5"]')))
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/count"]')))

        return element.text
            

    def swipe_up(self,driver):
        size = driver.get_window_size()
        start_y = size['height'] * 0.8  # 画面の下部80%の位置
        end_y = size['height'] * 0.2    # 画面の上部20%の位置
        start_x = size['width'] * 0.5   # 画面の中央
        driver.swipe(start_x, start_y, start_x, end_y, 1000)  # スワイプ時間は1000ms（1秒）

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
                time.sleep(1)
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
