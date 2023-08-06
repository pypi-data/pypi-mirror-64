#-*-coding:utf-8 -*-
import os
import random
import subprocess
import time
from selenium import webdriver
from appium import webdriver as appiumServer

class Driver(object):
    def __init__(self,browser="chrome",udid=None,app=None,executable_path_dict=None):
        self.executable_path_dict = executable_path_dict
        if browser == "chrome":
            self.driver = webdriver.Chrome(executable_path=self.executable_path_dict["chromedriver"])
        elif browser == "safri":
            self.driver = webdriver.Safari()
        elif browser == "edge":
            self.driver = webdriver.Ie(executable_path=self.executable_path_dict["iedriver"])
        elif browser == "firefox":
            self.driver = webdriver.Firefox(executable_path=self.executable_path_dict["firefoxdriver"])
        elif browser == "edge":
            self.driver = webdriver.Firefox(executable_path=self.executable_path_dict["edgedriver"])
        elif browser == "android":
            self.udid = udid
            self.app = app
            self.port,self.bp = self.productrandom()
            caps = self.android_caps(udid,app)
            url = 'http://127.0.0.1:%s/wd/hub' % (self.port)
            self.driver = appiumServer.Remote(url,caps)

        elif browser == "iOS":
            self.port, self.bp = self.productrandom()
            caps = self.iOS_caps(udid, app)
            url = 'http://127.0.0.1:%s/wd/hub' % (self.port)
            self.driver = appiumServer.Remote(url, caps)

    def productrandom(self):
        port = random.randint(1111, 5555)
        bp = random.randint(11111, 33333)
        return port,bp

    def isPort(self):
        if os.name == "posix":
            pid = os.popen("lsof -i:%s|grep node|awk '{print $2}'" % str(self.port)).read()
        elif os.name == "nt":
            pid = os.popen("netstat -ano|findStr %s" % str(self.port)).read()[-8:].strip()
        if len(pid) != 0:
            return True

    def AppiumServer(self):
        # port,bp = self.productrandom()
        cmd = "appium -a 127.0.0.1 -U %s -p %s -bp %s --command-timeout 100000 --session-override" % (self.udid, self.port, self.bp)
        # url = 'http://127.0.0.1:%s/wd/hub' % (port)
        subprocess.Popen(cmd, shell=True)
        print("正在启动appium服务，请稍等.....")
        n = 0
        while True:
            isPort = self.isPort()
            if isPort == True:
                 break
            else:
                time.sleep(5)
                n+=1
            if n > 5:

                raise RuntimeError("appium server is error, please reconnect appiumse!!!")
        print("成功启动appium服务，请稍等.....")


    def android_caps( self,udid, app_path, adb_path="adb", aapt_path="aapt", isApp=False, isResetKeyboard=False):
        if self.executable_path_dict != None:
            if "app_path" in executable_path_dict.keys():
                app_path = executable_path_dict["app_path"]
            if "aapt_path" in executable_path_dict.keys():
                aapt_path = executable_path_dict["aapt_path"]

        if os.name == "posix":
            aapt_dump = "%s dump badging %s |grep %s|awk '{print $2}'"
            appPackage = str(os.popen(aapt_dump % (aapt_path, app_path, "package")).read()).strip()[6:-1]
            # print(aapt_dump % (aapt_path,app_path, "launchable-activity"))
            try:
                appActivity = str(
                    os.popen(aapt_dump % (aapt_path, app_path, "launchable-activity")).read()).split()[
                                  0].strip()[6:-1]
            except Exception as e:
                appActivity = appPackage + ".main.MainActivity"

        elif os.name == "nt":
            appPackage = os.popen('aapt dump badging  %s |findStr "package:" ' % (app_path)).read().split(" ")[
                             1].strip()[6:-1]
            try:
                appActivity = \
                os.popen('aapt dump badging %s |findStr "launchable-activity"' % (app_path)).read().split(" ")[
                    1].strip()[
                6:-1]
            except:
                appActivity = appPackage + ".main.MainActivity"

            # udids = str(os.popen("%s devices|grep -v devices|awk '{print $1}'" % (self.adb_path)).read()).split("\n")
            # udids = list(filter(None, udids))
        android_version = os.popen(
            "%s -s %s shell getprop ro.build.version.release" % (adb_path, udid)).read().strip()
        android_name = os.popen("%s -s %s shell getprop ro.product.name" % (adb_path, udid)).read().strip()
        if int(android_version[0]) <= 4:
            error = "Android Version must be greater than 4 !"
            raise RuntimeError(error)

        caps = {"platformName": "android",
                "platformVersion": android_version,
                "app": app_path,
                "udid": udid,
                # "newCommandTimeout":100000,
                "deviceName": android_name,
                "appPackage": appPackage,
                "appActivity": appActivity}
        if isResetKeyboard == True:
            caps.update({'unicodeKeyboard': True,
                         'resetKeyboard': True})
        if isApp == True:
            caps.update({"noReset": True})
        return caps

    def iOS_caps(self,udid, app):
        pass

if __name__ == '__main__':
    #config
    executable_path_dict = {"adb_path": "/Users/zhenghong/Library/Android/sdk/platform-tools/adb",
                            "aapt_path": "/Users/zhenghong/Library/Android/sdk/build-tools/29.0.3/aapt",
                            "firefoxdriver": "/Users/zhenghong/work/gitee/AutomationFramework/conf/geckodriver",
                            "chromedriver": "/Users/zhenghong/work/gitee/AutomationFramework/conf/chromedriver"}

    driver = Driver("chrome",executable_path_dict=executable_path_dict).driver #启动Chrome浏览器
    driver = Driver("safri",executable_path_dict=executable_path_dict).driver #启动safri浏览器
    driver = Driver("firefox",executable_path_dict=executable_path_dict).driver #启动firefox浏览器
