from utils.commonUtils import login_get_cookies
from utils.driverUtils import FirefoxDriver

if __name__ == '__main__':
    driver = FirefoxDriver()
    login_get_cookies(driver, username='zhuxingli', password='zhuxingli')
