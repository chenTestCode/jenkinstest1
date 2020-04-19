import logging
import os


from selenium import webdriver
from datetime import datetime
from traceback import print_stack
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys

from log import custom_logger


class SeleniumDriver:
    log = custom_logger.MyLog()

    def __init__(self,driver):
        self.driver=driver

    def take_screen(self,resultMessage):
        '''
         当def错误是截图  
        :param resultMessage: 
        :param folder_name: 
        :param run_id: 
        :return: 
        '''
        date=datetime.strftime(datetime.now(),"%Y-%m-%d-%H-%M-%S")
        dir_name=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"screenshots")
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        file_name=resultMessage+"_"+date+".png"
        destination=os.path.join(dir_name,file_name)
        self.driver.get_screenshot_as_file(destination)

    def get_by_type(self,locator_type):
        '''
        生成定位器类型
        :param locator_type: 
        :return: 
        '''
        locator_type==locator_type.lower()
        if locator_type=="id":
            return By.ID
        elif locator_type=="name":
            return By.NAME
        elif locator_type=="xpath":
            return By.XPATH
        elif locator_type=="css":
            return By.CSS_SELECTOR
        elif locator_type=="class":
            return By.CLASS_NAME
        elif locator_type=="tag":
            return By.TAG_NAME
        else:
            self.log.info("Locator_type"+locator_type+"not correct/supported")
        return False

    def open(self,project,path=''):
        '''
        打开浏览器页面
        :param project: 
        :param path: 
        :return: 
        '''
        self.driver.get(project+path)
        self.log.info("open page with url %s" % project+path)

    def element_get(self, locator, locator_type='css', web_element=None):
        """
        find element on dom tree of web page
        :param locator: str from page class ex LoginPage
        :param locator_type: str from page class ex LoginPage
        :param web_element: WebElement returned by method ex element_get
        :return: WebElement
        """
        element = web_element
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            if element:
                element = web_element.find_element(by_type, locator)
                self.log.info("Element descendant Found with locator: " + locator + " locator_type " + locator_type)
            else:
                element = self.driver.find_element(by_type, locator)
                self.log.info("Element Found with locator: " + locator + " locator_type " + locator_type)
        except:
            self.log.error("Element not found")
        return element



    def elements_get(self, locator, locator_type='css'):
        ''''''
        elements = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            elements = self.driver.find_elements(by_type, locator)
            self.log.info("Elements Found")
        except:
            self.log.info("Elements not found")
        return elements

    def element_attribute(self, attr_name, locator='', locator_type='css', element=None):
        '''找到属性值并返回它'''
        name = None
        if element is not None:
            try:
                name = element.get_attribute(attr_name)
                self.log.info("Element Not Found with attribute %s" % attr_name)
            except:
                self.log.info("Element Not Found with attribute %s" % attr_name)
        else:
            try:
                locator_type = locator_type.lower()
                by_type = self.get_by_type(locator_type)
                result = self.driver.find_element(by_type, locator)
                name = result.get_attribute(attr_name)
                self.log.info("Elements Found")
            except:
                self.log.info("Elements not found")
        return name

    def elements_get_in_dict(self, locator, locator_type='css'):

        elements = {}
        try:
            by_type = self.get_by_type(locator_type.lower())
            elements = {element.get_attribute('href'): element for element in
                        self.driver.find_elements(by_type, locator)}
        except:
            self.log.info('Elements not found')
        return elements

    def element_click(self, locator='', locator_type='css', web_element=None):

        try:
            if web_element:
                web_element.click()
                self.log.info("Clicked on element")
            else:
                element = self.element_get(locator, locator_type)
                element.click()
                self.log.info("Clicked on element with locator: " + locator + " locator_type: " + locator_type)
        except:
            self.log.info("Cannot click on the element with locator: " + locator + " locator_type: " + locator_type)

    def element_send_keys(self, locator, data, locator_type='css', element=None):

        try:
            if element is not None:
                element.send_keys(data)
            else:
                element = self.element_get(locator, locator_type)
                element.send_keys(data)
            self.log.info("Send data on element with locator: " + locator + " locator_type: " + locator_type)
        except:
            self.log.info("Cannot send data on the element with locator: " + locator + " locator_type: " + locator_type)


    def element_is_present(self, locator, locator_type='id'):


        try:
            element = self.element_get(locator, locator_type)
            if element is not None:
                return True
            else:
                self.log.info("Element not found")
                return False
        except:
            self.log.info("Element not found")
            return False

    def element_presence_check(self, locator, locator_type='id'):
        try:
            elementList = self.elements_get(locator, locator_type)
            if len(elementList) > 0:
                self.log.info("Element not found")
                return True
            else:
                self.log.info("Element not found")
                return False
        except:
            self.log.info("Element not found")
            return False

    def element_wait_for(self, locator, locator_type='id', timeout=10, poll_frequency=0.5):
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((by_type, locator)))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element not appeared on the web page")
            print_stack()
        return element


    def element_visibility_wait_for(self, locator, locator_type='id', timeout=10, poll_frequency=0.5):
        """
        wait while element to be visible
        :param locator: str from page class ex LoginPage
        :param locator_type: str from page class ex LoginPage
        :param timeout: int timeout
        :param poll_frequency: int query per second to element
        :return: WebElement
        """
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((by_type, locator)))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element not appeared on the web page")
            print_stack()
        return element

    def element_is_displayed(self, locator="", locator_type="id", element=None):

        is_displayed = False
        try:
            if locator:  # This means if locator is not empty
                element = self.element_get(locator, locator_type)
            if element is not None:
                is_displayed = element.is_displayed()
                self.log.info("Element is displayed")
            else:
                self.log.info("Element not displayed")
            return is_displayed
        except:
            print("Element not found")
            return False

    def element_is_clickable(self, locator, locator_type='id', timeout=20, poll_frequency=0.5):

        element = None
        try:
            by_type = self.get_by_type(locator_type)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException,
                                                     ElementClickInterceptedException])
            element = wait.until(EC.element_to_be_clickable((by_type, locator)))
            self.log.info("Element is ready for click")
        except:
            self.log.info("Element is not clickable")
            print_stack()
        return element

    def element_get_text(self, locator="", locator_type="css", element=None, info=""):
        try:

            if locator:
                element = self.element_get(locator, locator_type)
            text = element.text

            if len(text) == 0:
                text = element.get_attribute('InnerText')
            if len(text) != 0:
                self.log.info("Getting text on element :: " + info)
                self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def get_url(self):
        current_url = None
        try:
            current_url = self.driver.current_url
            self.log.info('Current URL is :: ' + current_url)
        except:
            self.log.error('Failed to get current URL ' + current_url)
            print_stack()
        return current_url

    def get_title(self):

        title = None
        try:
            title = self.driver.title
            self.log.info('Current title is :: ' + title)
        except:
            self.log.error('Failed to get title ' + title)
            print_stack()
        return title

    def open_new_tab(self, locator="", locator_type="id", timeout=10):
        handles_before = self.driver.window_handles
        self.element_click(locator=locator, locator_type=locator_type)
        handles_after = None
        try:
            WebDriverWait(self, timeout).until(lambda windows: len(handles_before) != len(self.driver.window_handles))
            handles_after = self.driver.window_handles
            self.log.info('New window is opened :: ' + self.get_title())
            return handles_after
        except:
            self.log.error('No new window opened')
        return handles_after

    def switch_window(self, window_number):
        """
        Switch to another tab
        :param window_number: int window tab number
        :return: bool
        """
        try:
            self.driver.switch_to.window(self.driver.window_handles[window_number])
            self.log.info('Switched on new windows :: ' + self.get_title())
            return True
        except:
            self.log.error('Can`t switched to the window :: ' + str(window_number))
            return False

    def element_clear(self, locator, locator_type='id'):
        """
        Clear element field
        :param locator: str from page class ex LoginPage
        :param locator_type: str from page class ex LoginPage
        :return: None
        """
        try:
            element = self.element_get(locator, locator_type)
            element.clear()
            self.log.info("Cleared on element with locator: " + locator + " locator_type: " + locator_type)
        except:
            self.log.info("Cannot clear on the element with locator: " + locator + " locator_type: " + locator_type)

    def element_clear_by_keys(self, locator, locator_type='id', attribute='value'):
        """
        Clear field with sending Keys_BACKSPACE to field
        :param locator: str from page class ex LoginPage
        :param locator_type: str from page class ex LoginPage
        :param attribute: attribute by which determines how much keys sending
        :return: None
        """
        try:
            element = self.element_get(locator, locator_type)
            value = element.get_attribute(attribute)
            for i in range(len(value)):
                element.send_keys(Keys.BACKSPACE)
            self.log.info("Cleared on element with locator: " + locator + " locator_type: " + locator_type)
        except:
            self.log.info("Cannot clear on the element with locator: " + locator + " locator_type: " + locator_type)






if __name__ == '__main__':
   # dir_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots/")
   # print(dir_name)
   p=SeleniumDriver("l").take_screen("test1","test2","test3")
   print(p)
   # data = datetime.strftime(datetime.now(),"%d/%m/%Y")
   # print(data)

