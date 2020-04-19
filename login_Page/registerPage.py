from common.selenium_driver import SeleniumDriver

from selenium import webdriver
class RegPage(SeleniumDriver):
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver

    def send_userName(self,userName):
        self.element_send_keys('username',userName,'name')

    def send_password(self,password):
        self.element_send_keys('password',password,'name')

    def send_confirmPassw(self,confinrmpass):
        self.element_send_keys('userpassword2',confinrmpass,'name')

    def send_mobilePhone(self,numbre):
        self.element_send_keys('mobile_phone',numbre,'name')

    def send_email(self,email):
        """

        :param email: 
        """
        self.element_send_keys('email',email,'name')

    def click_regButton(self):
        self.element_click('.reg_btn')

    def get_error_mage(self,num):
        """
        nth-child(1):用户名,nth-child(2),密码.....
        

        :return: 
        """
        return self.element_get_text('.registerform>ul>li:nth-child(%s)>div>span.Validform_checktip'%num)

    def login_info(self):
        return self.element_get_text('.site-nav-right.fr>a:nth-child(1)')

    def logout_button(self):
        self.element_click('.site-nav-right.fr>a:nth-child(2)')

    def click_reg(self):
        self.element_click('.site-nav-right.fr>a:nth-child(2)')



# if __name__ == '__main__':
#     driver = webdriver.Chrome()
#     driver.implicitly_wait(8)
#     driver.get("http://127.0.0.1/index.php?m=user&c=public&a=reg")
#     l = RegPage(driver)
#     # l.send_userName('chen123')
#     # l.send_password('1234567')
#     # # m=driver.find_element_by_css_selector('.registerform>ul>li:nth-child(1) .Validform_wrong').text
#     # m=l.get_error_mage(1)
#     # print(m)
#     # l.send_confirmPassw('67892')
#     # m = l.get_error_mage(2)
#     # print(m)
#     #
#     # l.send_mobilePhone('12345678')
#     # m = l.get_error_mage(3)
#     test=l.get_loginbuttonText()
#     print(test)
#     # l.send_email('673287@qq.com')