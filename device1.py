from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from appium.options.android import UiAutomator2Options

from functions.Main import main_fn


#Desired Capabilitiesの設定
capabilities = dict(
    platformName='Android', #操作対象のプラットフォームを指定します。
    automationName='UiAutomator2', #使用する自動化エンジンを指定します。
    deviceName='SH-01L', #操作対象のデバイス名を指定します。
    # udid='192.168.100.123:5555',
    udid='2bf20c78ee1c7ece',
    language='en', #デバイスの言語設定を指定します。
    # locale='US',
)
appium_server_url = 'http://localhost:4721' 

capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
driver = webdriver.Remote(command_executor=appium_server_url, options=capabilities_options)
driver.update_settings({"enforceXPath1": True})


wait = WebDriverWait(driver, 5)

device_id = 2
# main_fn_test(driver, wait, str(device_id))
main_fn(driver, wait, str(device_id))


