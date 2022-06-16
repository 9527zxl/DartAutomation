import os
import sys
from time import sleep

from tkinterMain import mainGUi
from utils.cnipaUtils import login_cnipa, gain_cnipa_cookies, get_cookies
from utils.commonUtils import gain_feibiao_cookie
from utils.driverUtils import FirefoxDriver
from utils.requestsUtils import get_patent_number, patent_update, update_successfully


def main(driver, feibiaoCookie):
    # 登录查询网站
    global sleep_state
    login_cnipa(driver, username='18455156272', password='Zhixin888*')

    while True:
        update_number1 = update_successfully(feibiao_cookie=feibiaoCookie)
        # 获取年费状态更新账号
        patent_number = get_patent_number(feibiao_cookie=feibiaoCookie)
        print('年费状态更新专利号:' + str(patent_number))
        # 获取更新
        token = gain_cnipa_cookies(driver, patent_number=patent_number)
        if token == '查询次数已经耗尽':
            sys.exit()
        print('token:' + str(token))
        # 获取更新cookie
        cookie = get_cookies()
        print('cookie:' + str(cookie))
        # 年费状态更新
        patent_update(feibiao_cookie=feibiaoCookie, update_cookie=cookie, update_token=token)

        while sleep_state:
            sleep(30)
            update_number2 = update_successfully(feibiao_cookie=feibiaoCookie)

            if update_number1 > update_number2:
                sleep_state = True


if __name__ == '__main__':
    # driver = FirefoxDriver(path=os.path.abspath(os.curdir) + '\driver\geckodriver.exe')
    # 登录飞镖网
    # login_get_cookies(driver, username='zhuxingli', password='zhuxingli')
    # 获取飞镖cookie
    # feibiao_cookie = gain_feibiao_cookie()
    # print('飞镖网cookie:' + str(feibiao_cookie))
    # main(driver=driver, feibiaoCookie=feibiao_cookie)

    mainGUi()
