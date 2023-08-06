from selenium import webdriver
from appium import webdriver as appiumServer
class Driver(object):
    def __init__(self,browser="chrome"):
        if browser == "chrome":
            self.driver = webdriver.Chrome(executable_path="/Users/zhenghong/work/gitee/AutomationFramework/conf/chromedriver")
        elif browser == "safri":
            self.driver = webdriver.Safari()
            pass
        elif browser == "firefox":
            self.driver = webdriver.Firefox(executable_path="/Users/zhenghong/work/gitee/AutomationFramework/conf/geckodriver")
        elif browser == "edge":
            self.driver = webdriver.Firefox(executable_path="")

        elif browser == "android":
            self.driver = appiumServer.Remote(url,caps)
            pass
        elif browser == "iOS":
            self.driver = appiumServer.Remote(url, caps)

    @staticmethod
    def android_caps():
        pass
    @staticmethod
    def iOS_caps():
        pass

if __name__ == '__main__':
    driver = Driver("safri").driver

