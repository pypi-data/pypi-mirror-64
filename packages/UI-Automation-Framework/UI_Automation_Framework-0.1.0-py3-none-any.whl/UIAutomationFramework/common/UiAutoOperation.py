import time

from UIAutomationFramework.common.UiAutoDriver import Driver
from error import check_error
class operation(object):
    def __init__(self,browser="chrome",caps=None):
        if caps != None:
            self.driver = Driver(caps).driver
        else:
            self.driver = Driver(browser).driver
        self.driver.implicitly_wait(15)

    @check_error
    def find_element(self,element):
        key,values = str(element).split("-")
        if key == "id":
            el = self.driver.find_element_by_id(values)
            return el
        elif key == "xpath":
            el = self.driver.find_element_by_xpath(values)
            return el

    @check_error
    def find_elements(self,element):
        key, values = str(element).split("-")
        if key == "id":
            el = self.driver.find_elements_by_id(values)
            return el
        elif key == "xpath":
            el = self.driver.find_elements_by_xpath(values)
            return el

    def click(self,element):
        el = self.find_element(element)
        if el != False:
            el.click()
        return el

    def clicks(self,element,n):
        el = self.find_elements(element)
        if el != False:
            el[n].click()
        return el

    def text(self,element):
        el = self.find_element(element)
        if el != False:
            return el.text
        return el

    def texts(self,element,n):
        el = self.find_elements(element)
        if el != False:
            return el[n].text
        return el

    def get(self,url):
        self.driver.get(url)
    def max_window(self):
        self.driver.maximize_window()

    def send_keys(self,element,text):
        el = self.find_element(element)
        if el != False:
            el.send_keys(text)
        return el

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    "id-kw ,su"
    browser = "safri"
    # browser = "chrome"
    # browser = "firefox"

    driver = operation(browser=browser)
    driver.get("http://baidu.com")
    driver.send_keys("id-kw","中国")
    driver.click("id-su")
    time.sleep(10)
    driver.close()
