import pytest
import allure
import time,os
from selenium import webdriver

from login_Page.registerPage import RegPage

@pytest.fixture()
def start(driver):
    driver.get('http://127.0.0.1/index.php?m=user&c=public&a=reg')

@allure.story('正确的注册方式')
@allure.step('验证正确的注册')
def test_wer(driver,start):
    p=time.strftime('%H%M%S')
    driver = RegPage(driver)

    driver.send_userName("chen"+p)
    allure.attach('输入密码','123456')
    driver.send_password('123456')
    driver.send_confirmPassw('123456')
    driver.send_mobilePhone('18365'+p)
    driver.send_email('23%s@qq.com'%p)

    driver.click_regButton()
    time.sleep(5)
    result=driver.login_info()
    driver.logout_button()
    time.sleep(4)
    assert result=='您好 chen'+p


@allure.feature('注册模块')
@pytest.mark.usefixtures('start')
@pytest.mark.error
class Test_suti:
    # @pytest.mark.website


    @allure.story('验证已存在的用户名')
    @allure.step('验证错误的注册')

    def test_username_error(self,driver):
        driver = RegPage(driver)
        driver.send_userName('chen123')

        driver.send_password('123456')
        time.sleep(2)
        yonghu = driver.get_error_mage(1)
        assert yonghu=='用户名存在'

    @allure.story('验证用户名为空')

    def test_username_empty(self,driver):
        driver = RegPage(driver)
        driver.send_userName('')

        driver.send_password('123456')
        time.sleep(2)
        yonghu = driver.get_error_mage(1)
        assert yonghu == '请填写用户名'

    @allure.story('验证用户名长度')
    @allure.step('用户名不能低于3位')

    def test_username_len(self,driver):
        driver = RegPage(driver)
        driver.send_userName('2')

        driver.send_password('123456')
        time.sleep(2)
        yonghu = driver.get_error_mage(1)
        assert yonghu == '用户名不低于三位，使用中文、数字、字母皆可！'

@allure.feature('注册模块密码功能')
@pytest.mark.usefixtures('start')
@pytest.mark.error

class Test_passwored:
    @allure.story('密码为空')
    def test_pass_empty(self,driver):
        driver = RegPage(driver)
        driver.send_userName('wewrrwe')

        driver.send_password('')
        driver.send_confirmPassw('123456')
        time.sleep(2)
        
        yonghu = driver.get_error_mage(2)
        assert yonghu == '请填写密码'

    @allure.story('密码3位')
    def test_pass_sort(self, driver):
        driver = RegPage(driver)
        driver.send_userName('wewrrwe')

        driver.send_password('123')
        driver.send_confirmPassw('123456')
        time.sleep(2)

        yonghu = driver.get_error_mage(2)
        assert yonghu == '密码范围在6~15位之间！'

    @allure.story('密码超长')
    def test_pass_long(self, driver):
        driver = RegPage(driver)
        driver.send_userName('wewrrwe')

        driver.send_password('123wqertyu23456werty')
        driver.send_confirmPassw('123456')
        time.sleep(2)

        yonghu = driver.get_error_mage(2)
        assert yonghu == '密码范围在6~15位之间！'

@allure.feature('注册模块确认密码功能')
@pytest.mark.usefixtures('start')
@pytest.mark.error
@pytest.mark.parametrize("usuranme,password,password2,msg",
                         [
                             ('tytyew','1223456','','请确认密码'),
                             ('ytyweu','123456','425','您两次输入的账号密码不一致！'),
                             ('uewiiew','76237ew','qwertyuio2345678','您两次输入的账号密码不一致！')
                         ])

@allure.story('验证确认密码输入')
def test_passwordCon(driver,usuranme,password,password2,msg):
    driver = RegPage(driver)
    driver.send_userName(usuranme)

    driver.send_password(password)
    driver.send_confirmPassw(password2)
    driver.send_mobilePhone('123')
    time.sleep(2)

    yonghu = driver.get_error_mage(3)
    assert yonghu == msg


@allure.feature('注册模块手机功能')
@pytest.mark.usefixtures('start')
@pytest.mark.error
@pytest.mark.parametrize("usuranme,password,password2,phone,msg",
                         [
                             ('tytyew','1223456','1223456','','请填写手机号码'),
                             ('ytyweu','123456','1223456','123','手机号错误！'),
                             ('uewiiew','76237ew','76237ew','12345678901','手机号错误！')
                         ])

@allure.story('验证确认手机输入')
def test_phone(driver,usuranme,password,password2,phone,msg):
    driver = RegPage(driver)
    driver.send_userName(usuranme)

    driver.send_password(password)
    driver.send_confirmPassw(password2)
    driver.send_mobilePhone(phone)
    driver.send_email('23')
    time.sleep(2)

    yonghu = driver.get_error_mage(4)
    assert yonghu == msg

@allure.feature('注册模块邮箱功能')
@pytest.mark.usefixtures('start')
@pytest.mark.error
@pytest.mark.parametrize("usuranme,password,password2,phone,email,msg",
                         [
                             ('tytyew','1223456','1223456','18765326712','','请填写邮箱'),
                             ('ytyweu','123456','123456','18765326712','56','邮箱格式错误！'),
                             ('uewiiew','76237ew','76237ew','18765326712','432@123.com','通过信息验证')
                         ])

@allure.story('验证邮箱输入')
def test_email(driver,usuranme,password,password2,phone,email,msg):
    driver = RegPage(driver)
    driver.send_userName(usuranme)

    driver.send_password(password)
    driver.send_confirmPassw(password2)
    driver.send_mobilePhone(phone)
    driver.send_email(email)
    driver.send_mobilePhone(phone)
    time.sleep(2)

    yonghu = driver.get_error_mage(5)
    assert yonghu == msg


# if __name__ == '__main__':
#     os.system("pytest --alluredir ./result/")
    # pytest.main(['-s','test_reg.py'])
