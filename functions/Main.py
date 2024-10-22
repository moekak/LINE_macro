
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from models.GroupMsg import GroupMsg
from models.MsgSendingTimes import MsgSendingTimes
from functions.RegistrationMsgFn import RegistrationMsgFn
from functions.GetElments import GetElements
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from models.FriendCount import FriendCount
from models.RegistrationMsg import RegistrationMsg
from datetime import datetime,timedelta
from models.MsgUrl import MsgUrl
from functions.Notification import Notification
from functions.ShadowBanMsg import ShadowBanMsg
from models.Device import Device;
from functions.ErrorOperation import ErrorOperation





def main_fn(driver, wait, device_id):

    reg_msg_fn      = RegistrationMsgFn()
    get_elements_fn = GetElements()
    wait            = WebDriverWait(driver, 20)
    notification_fn = Notification()
    prevTime        = datetime.now()
    prevTime2       = datetime.now()
    shadowBan_fn    = ShadowBanMsg()
    error_operation = ErrorOperation()
    device_model    = Device()
    reg_msg_model   = RegistrationMsg()
    url_model       = MsgUrl()
    friend_model    = FriendCount()
    group_msg_model = GroupMsg()
    msg_time_model  = MsgSendingTimes()
    username        = device_model.selectUsername(device_id)



    while True:
        try:
        
            # 今の時間を取得
            now = datetime.now()
            
            try:
                home_btn = driver.find_elements(By.XPATH, '//android.view.View[@content-desc="ホームタブ"]')
                if home_btn:
                    get_elements_fn.click_home_btn(wait, driver, username)
            except Exception as e:
                notification_fn.send_error2(e, "ホームタブの要素取得の際にエラーが発生しました。", username)
                error_operation.restart_app(driver)
                
            # # 友達リストをクリックする
            get_elements_fn.click_friend_list_btn(wait, driver, username)
            


            # シャドウバン確認で30分ごとにメッセージを送信する
            if now - prevTime >= timedelta(minutes=30):
                shadowBan_fn.sendMessageToAdmin(wait, driver, username, get_elements_fn)
                prevTime = datetime.now()
                
            if now - prevTime2 >= timedelta(minutes=10):
                notification_fn.send_confirmation_msg()
                prevTime2 = datetime.now()


            # 新規追加登録がないか監視している
            # 追加があった場合は、新規登録処理を優先で実行している
            reg_msg_fn.sendMessageToNewFriends(username,wait, driver, device_id, get_elements_fn, notification_fn, error_operation,reg_msg_model, url_model, friend_model, hasMsg = True,)
            
            ###############################　一斉送信処理 ####################################
            
            
            # 一斉送信するメッセージデータを取得
            messages_data   = group_msg_model.getMessage(device_id, driver, username)
            
            # 送信フラグを取得
            flag = group_msg_model.checkFlag(messages_data)
            
            # 送信時間と今の時間が同じ場合、もしくは送信時間が過ぎてしまっているがまだ送信が実行されていない場合に一斉送信を行う
            # 新規登録の処理が間に来た場合のことを考慮でフラグも見る
            if (now.hour >= 10 and now.hour < 19) and flag == "0":
                while True:
                    
                    now = datetime.now()
                    # シャドウバン確認メッセージ
                    if now - prevTime >= timedelta(minutes=30):
                        shadowBan_fn.sendMessageToAdmin(wait, driver, username, get_elements_fn)
                        prevTime = datetime.now()
                        
                    if now - prevTime2 >= timedelta(minutes=10):
                        notification_fn.send_confirmation_msg()
                        prevTime2 = datetime.now()
                        
                        
                    end_id = msg_time_model.getEndId(device_id, driver, username)
 
                    
                    # メッセージを送信開始タイミングでラインに通知する
                    if int(end_id) == 0:
                        notification_fn.send_msg_sendingTime(username)

                    # 友達リストを選択する
                    get_elements_fn.click_friend_list_btn(wait, driver, username)

                    
                    # 新規追加登録がないか監視している(
                    # 追加があった場合は、新規登録処理を優先で実行している
                    # 一斉送信するアカウントが多いと、その処理の間新規追加処理ができないため、for loopの処理で毎回監視処理を入れている
                    reg_msg_fn.sendMessageToNewFriends(username, wait, driver, device_id, get_elements_fn, notification_fn, error_operation, reg_msg_model, url_model,friend_model, hasMsg = False)

                    
                    # 毎回のユーザーでランダムにメッセージを取得する()
                      # 一斉送信するメッセージデータを取得
    
                    messages_data   = group_msg_model.getMessage(device_id, driver, username)
                    message_url     = url_model.selectURL(device_id, driver, username)
                    
                    message         = group_msg_model.generateMessageList(messages_data)
                    # 友達リストを選択する
                   
                    # ライン友達の総数を取得する
                    friend_count = friend_model.selectCount(device_id, driver, username)
                    
                    # 全てのユーザーにデータ送信が終わった場合
                    if int(end_id) == friend_count:
                        msg_time_model.updateEndId(device_id, driver, username)
                        msg_time_model.updateFlag(device_id, driver, username)

                        get_elements_fn.click_leave_talk_btn(wait, driver, username)
                        
                        notification_fn.send_msg_emdTime(datetime.now().replace(microsecond=0), username)
                        break
                    
                    if int(end_id) <= 9:
                        end_count = f"0{int(end_id) + 1}"
                    else:
                        end_count = int(end_id + 1)
                        
                    print(end_count)
                    
                    get_elements_fn.clickFriendListInput(wait, driver, username, end_count)
                    
                    element_xpath = f'//android.widget.TextView[@resource-id="jp.naver.line.android:id/name" and @text="{end_count}"]'
                    element=  get_elements_fn.find_element_with_scroll(driver, By.XPATH, element_xpath, username)
                    
                    # もし友達リストにユーザがいたときにの場合
                    if element:
                        # ユーザーをクリック
                        element.click()
                        # 一斉送信メッセージを送信する
                        get_elements_fn.sendGroupMsg(wait, message, msg_time_model, device_id, message_url,  driver, username)
                    else:
                        # データベースend_idの更新をする
                        msg_time_model.IncreaseEndId(device_id, username)
                        get_elements_fn.click_leave_talk_btn(wait, driver, username)
                        print("increasing ID")
                        continue
                                   
            else:

                continue

        except TimeoutException as e:
            
            notification_fn.send_error2(e, "main_fn()でエラーが起こりました。", username)
            error_operation.restart_app(driver)

