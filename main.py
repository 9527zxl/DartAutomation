import os
from time import sleep

from utils.cnipaUtils import login_cnipa, gain_cnipa_cookies
from utils.commonUtils import login_get_cookies, gain_feibiao_cookie
from utils.driverUtils import FirefoxDriver
from utils.requestsUtils import get_patent_number, patent_update, update_successfully


def main():
    # 登录查询网站
    login_cnipa(driver, username='', password='')

    update_number1 = 0
    update_number2 = 0
    state = True

    while state:
        update_number1 = update_successfully(feibiao_cookie=feibiao_cookie)
        # 获取年费状态更新账号
        patent_number = get_patent_number(feibiao_cookie=feibiao_cookie)
        # 获取更新cookie
        cookie = gain_cnipa_cookies(driver, patent_number=patent_number, status='cookie')
        # 获取更新
        token = gain_cnipa_cookies(driver, patent_number='', status='token')
        # 年费状态更新
        patent_update(feibiao_cookie=feibiao_cookie, update_cookie=cookie, update_token=token)
        # 等待30s
        sleep(30)

        while update_number1 >= update_number2:
            update_number2 = update_successfully(feibiao_cookie=feibiao_cookie)
            sleep(30)

            if update_number1 < update_number2:
                state = False


if __name__ == '__main__':
    driver = FirefoxDriver(path=os.path.abspath(os.curdir) + '\driver\geckodriver.exe')
    # 登录飞镖网
    login_get_cookies(driver, username='', password='')
    # 获取飞镖cookie
    feibiao_cookie = gain_feibiao_cookie()
