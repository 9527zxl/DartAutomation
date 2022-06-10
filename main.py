import os

from utils.cnipaUtils import login_cnipa
from utils.commonUtils import login_get_cookies
from utils.driverUtils import FirefoxDriver

if __name__ == '__main__':
    driver = FirefoxDriver(path=os.path.abspath(os.curdir) + '\driver\geckodriver.exe')
    # login_get_cookies(driver, username='zhuxingli', password='zhuxingli')
    # login_cnipa(driver, username='15156052212', password='Zhixin888*')
    # driver.quit()
