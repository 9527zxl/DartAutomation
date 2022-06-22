import os
import sys
from time import sleep

from tkinter_login import loginGui
from utils.cnipaUtils import login_cnipa, gain_cnipa_cookies, get_cookies
from utils.commonUtils import gain_feibiao_cookie, login_get_cookies
from utils.driverUtils import FirefoxDriver
from utils.requestsUtils import get_patent_number, patent_update, update_successfully, get_acquisition_patent_Number

# def main(driver, feibiaoCookie):
#     # # 登录查询网站
#     # sleep_state = True
#     # login_cnipa(driver, username='18755159622', password='123abcABC@*')
#     #
#     # while True:
#     #     update_number1 = update_successfully(feibiao_cookie=feibiaoCookie)
#     #     # 获取年费状态更新账号
#     #     patent_number = get_patent_number(feibiao_cookie=feibiaoCookie)
#     #     print('年费状态更新专利号:' + str(patent_number))
#     #     # 获取更新
#     #     token = gain_cnipa_cookies(driver, patent_number=patent_number)
#     #     if token == '查询次数已经耗尽':
#     #         sys.exit()
#     #     print('token:' + str(token))
#     #     # 获取更新cookie
#     #     cookie = get_cookies()
#     #     print('cookie:' + str(cookie))
#     #     # 年费状态更新
#     #     patent_update(feibiao_cookie=feibiaoCookie, update_cookie=cookie, update_token=token)
#     #
#     #     while sleep_state:
#     #         sleep(30)
#     #         update_number2 = update_successfully(feibiao_cookie=feibiaoCookie)
#     #
#     #         if update_number1 < update_number2:
#     #             sleep_state = False


if __name__ == '__main__':
    driver = FirefoxDriver(path=os.path.abspath(os.curdir) + '\driver\geckodriver.exe', state=False)
    # 登录飞镖网
    login_get_cookies(driver, username='zhuxingli', password='zhuxingli')
    # 获取飞镖cookie
    feibiao_cookie = gain_feibiao_cookie()
    # main(driver=driver, feibiaoCookie=feibiao_cookie)

    # login_cnipa(driver, username='18856414322', password='Zhixin888*')
    # patent_number = get_patent_number(feibiao_cookie=feibiao_cookie)
    # token = gain_cnipa_cookies(driver, patent_number='2018100197126')
    # if token == '查询次数已经耗尽': sys.exit()
    # print(token)
    # cookie = get_cookies()
    # # 年费状态更新
    # patent_update(feibiao_cookie=feibiao_cookie, update_cookie=cookie, update_token=token)
    # print('更新完成')

    # get_acquisition_patent_Number(feibiao_cookie=feibiao_cookie,state=False)
