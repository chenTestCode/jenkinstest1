import time



from selenium import webdriver

from common.selenium_driver import SeleniumDriver


class LoginPage(SeleniumDriver):
    def __init__(self,driver):
        super().__init__(driver)
        self.driver=driver
    def send_username(self,name):
        self.element_send_keys("#username",name)
        # self.element_send_keys(locator="username",data="chen123",locator_type="id")

    def send_pwd(self,pwd):
        self.element_send_keys("#password",pwd)

    def click_LoginBtn(self):
        self.element_click(locator='.login_btn')

    def click_shop(self):
        self.element_click(locator=".dealing>dd:nth-child(2) a")

    def handle(self,name,pwd):

        self.send_username(name)
        self.send_pwd(pwd)
        self.click_LoginBtn()


    def click_img(self,locator=".catalogue-pro>div:nth-child(1)> a"):
        self.element_click(locator)

    def get_loginbuttonText(self):
        return self.element_get_text('.site-nav-right.fr>a:nth-child(1)')

    def click_login(self):
        self.element_click('.site-nav-right.fr>a:nth-child(1)')

    def logout_button(self):
        self.element_click('.site-nav-right.fr>a:nth-child(2)')

# https://www.jianshu.com/p/e31c54bf15ee
# if __name__ == '__main__':
#     driver=webdriver.Chrome()
#     driver.implicitly_wait(8)
#     driver.get("http://127.0.0.1/index.php?m=user&c=public&a=login")
#     l=LoginPage(driver)
#     l.send_username("chen123")
#     l.send_pwd("123456")
#     l.click_LoginBtn()
#     time.sleep(3)
#     t=driver.find_element_by_css_selector('.site-nav-right.fr>a:nth-child(1)').text
#     print(t)


    # if l.element_is_present("username","id"):
    #     l.send_username("chen123")
    # l.element_wait_for("password").send_keys("123456")
    # l.click_LoginBtn()
    # # l.send_pwd("123456")
    # k=l.element_visibility_wait_for(locator=".btn1",locator_type="css")
    #
    # # if k:
    # #     l.element_visibility_wait_for("password").send_keys("1234")
    # text=l.element_get_text(locator=".loginbar>div:nth-child(1)>div:nth-child(2)>a:nth-child(1)",locator_type="css")
    # print(text)
    # # #