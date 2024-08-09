
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
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from models.FriendCount import FriendCount
from datetime import datetime,timedelta
from models.MsgUrl import MsgUrl
from functions.Notification import Notification
from functions.ShadowBanMsg import ShadowBanMsg





def main_fn(driver, wait, device_id):

    group_msg_model = GroupMsg()
    msg_time_model  = MsgSendingTimes()
    reg_msg_model   = RegistrationMsg()
    url_model       = MsgUrl()
    reg_msg_fn      = RegistrationMsgFn()
    get_elements_fn = GetElements()
    wait            = WebDriverWait(driver, 20)
    notification_fn = Notification()
    prevTime = datetime.now()
    shadowBan_fn = ShadowBanMsg()

    while True:
        try:
        
            # 今の時間を取得
            now = datetime.now()
            group_msg_model = GroupMsg()
            
            # 一斉送信するメッセージデータを取得
            messages_data   = group_msg_model.getMessage(device_id)
            message_url = url_model.selectURL(device_id)

            # 送信フラグを取得
            flag = group_msg_model.checkFlag(messages_data)

            # 友達リストをクリックする
            get_elements_fn.click_friend_list_btn(wait, driver)
            

            if now - prevTime >= timedelta(minutes=1):
                shadowBan_fn.sendMessageToAdmin(wait, driver)
                prevTime = datetime.now()
                

            # 新規追加登録がないか監視している
            # 追加があった場合は、新規登録処理を優先で実行している
            reg_msg_fn.sendMessageToNewFriends(wait, driver, device_id, reg_msg_model,message_url,get_elements_fn, hasMsg = True)
            
            friend_model = FriendCount()
            friend_count = friend_model.selectCount(device_id)
            
            
            ###############################　一斉送信処理 ####################################
            
            # 送信時間と今の時間が同じ場合、もしくは送信時間が過ぎてしまっているがまだ送信が実行されていない場合に一斉送信を行う
            # 新規登録の処理が間に来た場合のことを考慮でフラグも見る
            if (now.hour >= 9 and now.hour < 21) and flag == "0" and friend_count > 0:
                while True:
                    now = datetime.now()
                    msg_time_model  = MsgSendingTimes()
                    end_id = msg_time_model.getEndId(device_id)
                    
                    # メッセージを送信開始タイミングでラインに通知する
                    if int(end_id) == 0:
                        notification_fn.send_msg_sendingTime()

                    # 友達リストを選択する
                    get_elements_fn.click_friend_list_btn(wait, driver)
                    print(now)
                    print(prevTime)

                    if now - prevTime >= timedelta(minutes=30):
                        shadowBan_fn.sendMessageToAdmin(wait, driver)
                        prevTime = datetime.now()
                    # 新規追加登録がないか監視している(
                    # 追加があった場合は、新規登録処理を優先で実行している
                    # 一斉送信するアカウントが多いと、その処理の間新規追加処理ができないため、for loopの処理で毎回監視処理を入れている
                    reg_msg_fn.sendMessageToNewFriends(wait, driver, device_id,reg_msg_model, message_url,get_elements_fn, hasMsg = False)

                    
                    # 毎回のユーザーでランダムにメッセージを取得する(データべースのやり取りは最初の一回のみ)
                    message = group_msg_model.generateMessageList(messages_data)
                    # 友達リストを選択する
                   
                    # ライン友達の総数を取得する
                    friend_model = FriendCount()
                    friend_count = friend_model.selectCount(device_id)
                    
                    
                    # 全てのユーザーにデータ送信が終わった場合
                    if int(end_id) == friend_count:
                        msg_time_model.updateEndId(device_id)
                        msg_time_model.updateFlag(device_id)
                        print("end")
                        get_elements_fn.click_leave_talk_btn(wait, driver)
                        notification_fn.send_msg_emdTime(datetime.now().replace(microsecond=0))
                        break
                    
                    
                    # 用検討
                    try:
                        element_xpath = f'//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="{int(end_id) + 1}"]'
                        
                        # 要素が古くなる可能性があるため、再取得する
                        time.sleep(1)
                        elements = driver.find_elements(By.XPATH, element_xpath)
                    except StaleElementReferenceException:
                        # 要素が古くなった場合、再取得して再試行する
                        elements = driver.find_elements(By.XPATH, element_xpath)
                    except TimeoutException as e:
                        notification_fn.send_error(e, f"一斉配信中にエラーが発生しました。名前:{int(end_id) + 1}に一斉送信できていません。LINEを再起動して再度メッセージ送信を試みます。")
                        get_elements_fn.restart_app(driver)
                                        
                    if elements:
                        elements[0].click()
                        get_elements_fn.sendGroupMsg(wait, message, msg_time_model, device_id, message_url, int(end_id) +1, driver)
                    else: 
                        print("scroll")
                        element = get_elements_fn.find_element_with_scroll(driver, By.XPATH, element_xpath)
                        if element:
                            element.click()
                            get_elements_fn.sendGroupMsg(wait, message, msg_time_model, device_id, message_url, int(end_id) +1, driver)
                        else:
                            print("skip!")
                            try:
                                # データベースend_idの更新をする
                                msg_time_model.IncreaseEndId(device_id)
                                get_elements_fn.click_leave_talk_btn(wait, driver)
                            except TimeoutException as e:
                                get_elements_fn.restart_app(driver)
                        
                        
            else:
                print("nay")
                continue

        except TimeoutException as e:
            notification_fn.send_error(e, "")
            driver.save_screenshot('screenshot.png')

            print("Timeout occurred, trying again...")
            print(e)
            
            continue  # タイムアウトが発生した場合、ループの次の反復に進む
