from login_Page.loginpage import LoginPage
import pytest,os

@pytest.fixture()
def startlogin(driver):
    driver.get('http://127.0.0.1/index.php?m=user&c=public&a=login')

@pytest.mark.usefixtures('startlogin')
class TestLogin:
    @pytest.mark.parametrize("name,pwd,msg",[
        ('chen123','','登录'),
        ('','','登录'),
        ('chen123','123456','您好 chen123')
    ])
    def test_loginRe(self,driver,name,pwd,msg):
        l=LoginPage(driver)
        l.handle(name,pwd)

        result=l.get_loginbuttonText()
        l.logout_button()
        assert result==msg

if __name__ == '__main__':
    os.system('pytest -s')