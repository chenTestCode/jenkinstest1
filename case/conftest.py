import pytest
from selenium import webdriver
@pytest.fixture(scope='module')

def driver():
    dr=webdriver.Chrome()
    dr.implicitly_wait(8)
    dr.get('http://127.0.0.1/index.php')

    return dr