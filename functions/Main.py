
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from models.RegistrationMsg import RegistrationMsg
from models.GroupMsg import GroupMsg
from models.MsgSendingTimes import MsgSendingTimes
from functions.RegistrationMsgFn import RegistrationMsgFn
from functions.GetElments import GetElements
from models.FriendCount import FriendCount
from datetime import datetime
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException



# ################################################################
#       データベースから取得したメッセージデータを成形
# ###############################################################

def main_fn(driver, wait, device_id):

    group_msg_model = GroupMsg()
    msg_time_model  = MsgSendingTimes()
    reg_msg_model   = RegistrationMsg()
    reg_msg_fn      = RegistrationMsgFn()
    get_elements_fn = GetElements()
    wait            = WebDriverWait(driver, 20)


    while True:
        try:
            
        
            # 今の時間を取得(ミリ秒は無視する)
            current_time    = datetime.now().replace(microsecond=0)
            group_msg_model = GroupMsg()
            # メッセージデータを取得
            messages_data   = group_msg_model.getMessage(device_id)
            # 一斉送信時間を取得(ミリ秒は無視する)
            sending_time =  group_msg_model.getMsgSendingTime(messages_data).replace(microsecond=0)
            # 送信フラグを取得
            flag = group_msg_model.checkFlag(messages_data)
            
            # ライン友達の総数を取得する
            friend_model = FriendCount()
            friend_count = friend_model.selectCount(device_id)
            
            
            # 自動送信メッセージを取得する
            messages = reg_msg_model.getMessage(device_id)
            # メッセージ
            message = ""
            for msg in messages:
                message = msg[0]
            
        
            print(f"Current time: {current_time}")
            print(f"Sending time: {sending_time}")
            


            element  = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="友だち"]')))
            element.click()

            # 新規追加登録がないか監視している(
            # 追加があった場合は、新規登録処理を優先で実行している
            reg_msg_fn.sendMessageToNewFriends(wait, message, driver, device_id, hasMsg = True)
                
                

            ###############################　一斉送信処理 ####################################
            
            # 送信時間と今の時間が同じ場合、もしくは送信時間が過ぎてしまっているがまだ送信が実行されていない場合に一斉送信を行う
            # 新規登録の処理が間に来た場合のことを考慮でフラグも見る
            if current_time == sending_time or (current_time > sending_time and flag == "0"):
                if int(friend_count) < 100:
                    for i in range(friend_count):
                        

                       
                        element  = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="友だち"]')))
                        element.click()

                        # 新規追加登録がないか監視している(
                        # 追加があった場合は、新規登録処理を優先で実行している
                        # 一斉送信するアカウントが多いと、その処理の間新規追加処理ができないため、for loopの処理で毎回監視処理を入れている
                        reg_msg_fn.sendMessageToNewFriends(wait, message, driver, device_id, hasMsg = False)

                        # 毎回のユーザーでランダムにメッセージを取得する(データべースのやり取りは最初の一回のみ)
                        message = group_msg_model.generateMessageList(messages_data)
                        # 友達リストを選択する
                        

                        try:
                            element_xpath = f'//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="{i+1}"]'
                            print(f"Generated XPath: {element_xpath}") 
    
                            time.sleep(3)
                            print("wowow")
                            # 要素が古くなる可能性があるため、再取得する
                            elements = driver.find_elements(By.XPATH, element_xpath)
                        except StaleElementReferenceException:
                            # 要素が古くなった場合、再取得して再試行する
                            elements = driver.find_elements(By.XPATH, element_xpath)
                        except TimeoutException as e:
                            driver.save_screenshot('screenshot.png')
                            print("Timeout occurred, trying again...")
                            print(e)
                        
                        
                        
                        

                        
                        if elements:
                            elements[0].click()
                            get_elements_fn.sendGroupMsg(wait,message)
                        else: 
                            print("skip!")
                            element  = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[@resource-id="jp.naver.line.android:id/header_up_button"]')))
                            element.click()
                            continue
                        
                        




                    # 送信時間の更新
                    print("finish")
                    group_msg_model = GroupMsg()
                    messages_data = group_msg_model.getMessage(device_id)
                    sending_time =  group_msg_model.getMsgSendingTime(messages_data).replace(microsecond=0)
                    msg_time_model.updateFlag(device_id)
                    
                    
                



            else:
                print("nay")
                continue

        except TimeoutException as e:
            driver.save_screenshot('screenshot.png')

            print("Timeout occurred, trying again...")
            print(e)
            
            continue  # タイムアウトが発生した場合、ループの次の反復に進む


def main_fn_test(driver, wait, device_id):

    group_msg_model = GroupMsg()
    msg_time_model  = MsgSendingTimes()
    reg_msg_model   = RegistrationMsg()
    reg_msg_fn      = RegistrationMsgFn()
    get_elements_fn = GetElements()
    wait            = WebDriverWait(driver, 20)


    while True:
        try:
            
        
            # 今の時間を取得(ミリ秒は無視する)
            current_time    = datetime.now().replace(microsecond=0)
            group_msg_model = GroupMsg()
            # メッセージデータを取得
            messages_data   = group_msg_model.getMessage(device_id)
            # 一斉送信時間を取得(ミリ秒は無視する)
            sending_time =  group_msg_model.getMsgSendingTime(messages_data).replace(microsecond=0)
            # 送信フラグを取得
            flag = group_msg_model.checkFlag(messages_data)
            
            # ライン友達の総数を取得する
            friend_model = FriendCount()
            friend_count = friend_model.selectCount(device_id)
            
            
            # 自動送信メッセージを取得する
            messages = reg_msg_model.getMessage(device_id)
            # メッセージ
            message = ""
            for msg in messages:
                message = msg[0]
            
        
            print(f"Current time: {current_time}")
            print(f"Sending time: {sending_time}")
            


            element  = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="友だち"]')))
            element.click()

            # 新規追加登録がないか監視している(
            # 追加があった場合は、新規登録処理を優先で実行している
            reg_msg_fn.sendMessageToNewFriends(wait, message, driver, device_id, hasMsg = True)
                
                

            ###############################　一斉送信処理 ####################################
            
            # 送信時間と今の時間が同じ場合、もしくは送信時間が過ぎてしまっているがまだ送信が実行されていない場合に一斉送信を行う
            # 新規登録の処理が間に来た場合のことを考慮でフラグも見る
            if current_time == sending_time or (current_time > sending_time and flag == "0"):
                if int(friend_count) <= 100:
                    start_time = time.time()

                    print(start_time)
                    
                    for i in range(500):
                        
                        print(i)

                       
                        element  = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="友だち"]')))
                        element.click()

                        # 新規追加登録がないか監視している(
                        # 追加があった場合は、新規登録処理を優先で実行している
                        # 一斉送信するアカウントが多いと、その処理の間新規追加処理ができないため、for loopの処理で毎回監視処理を入れている
                        reg_msg_fn.sendMessageToNewFriends(wait, message, driver, device_id, hasMsg = False)

                        # 毎回のユーザーでランダムにメッセージを取得する(データべースのやり取りは最初の一回のみ)
                        message = group_msg_model.generateMessageList(messages_data)
                        # 友達リストを選択する
                        
                        
                        
                        try:
                            element_xpath = f'//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="1"]'
                            element = wait.until(EC.presence_of_element_located((By.XPATH, element_xpath)))
                            
                            # 要素が古くなる可能性があるため、再取得する
                            time.sleep(3)
                            print("wowow")
                            elements = driver.find_elements(By.XPATH, element_xpath)
                        except StaleElementReferenceException:
                            # 要素が古くなった場合、再取得して再試行する
                            elements = driver.find_elements(By.XPATH, element_xpath)
                        except TimeoutException as e:
                            driver.save_screenshot('screenshot.png')
                            print("Timeout occurred, trying again...")
                            print(e)
                                        
                        
                        
                    
                        
                        if elements:
                            elements[0].click()
                            get_elements_fn.sendGroupMsg(wait,message)
                        else: 
                            print("skip!")
                            element  = wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ImageView[@resource-id="jp.naver.line.android:id/header_up_button"]')))
                            element.click()
                            continue
                        
                        




                    # 送信時間の更新
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    print(f"処理にかかった時間: {elapsed_time}秒")
                    print("finish")
                    group_msg_model = GroupMsg()
                    messages_data = group_msg_model.getMessage(device_id)
                    sending_time =  group_msg_model.getMsgSendingTime(messages_data).replace(microsecond=0)
                    msg_time_model.updateFlag(device_id)
                    
                    
                



            else:
                print("nay")
                break
            driver.quit()

        except TimeoutException as e:
            driver.save_screenshot('screenshot.png')

            print("Timeout occurred, trying again...")
            print(e)
            
            continue  # タイムアウトが発生した場合、ループの次の反復に進む