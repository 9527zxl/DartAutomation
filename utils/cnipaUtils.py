import json
import re
import sys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.commonUtils import explicitWaiting, verification_code, calculate_code, element_exist


def login_cnipa(driver, username, password):
    """
    :param driver: 浏览器驱动对象
    :param username: 查询网站账号
    :param password: 查询网站密码
    """
    driver.get('http://cpquery.cnipa.gov.cn/')
    driver.refresh()
    # 全局等待
    # driver.implicitly_wait(10)
    # 窗口最大化
    driver.maximize_window()

    # 等待元素加载完成
    explicitWaiting(driver, 20, xpath='//input[@id="username1"]')
    # 输入账号
    username_move = driver.find_element(By.XPATH, '//input[@id="username1"]')
    js = 'arguments[0].value= ' + '"' + username + '"' + ';'
    driver.execute_script(js, username_move)
    sleep(0.5)
    # 等待元素加载完成
    explicitWaiting(driver, 20, xpath='//input[@id="password1"]')
    # 输入密码
    password_move = driver.find_element(By.XPATH, '//input[@id="password1"]')
    js = 'arguments[0].value= ' + '"' + password + '"' + ';'
    driver.execute_script(js, password_move)

    # 等待验证码元素加载完成
    explicitWaiting(driver, 20, xpath='//*[@id="jcaptchaimage"]')
    # 悬浮验证码图片
    img = driver.find_element(By.XPATH, '//*[@id="imgyzm"]')
    reload = driver.find_element(By.XPATH, '//*[@id="reload"]')
    driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", reload, 'style',
                          'position: absolute; bottom: 230px; left: 275px; height: 0px;')
    driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", img, 'class', 'requestYzm')
    driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", reload, 'class', 'refresh')

    sleep(0.5)
    #  验证码识别并点击
    verification_code(driver=driver, image_location='./tempFiles/patent_inquire_login.png')

    # 处理验证码点击错误进行重新加载
    while driver.find_element(By.XPATH, '//*[@id="selectyzm_text"]').text != '验证成功':
        element = driver.find_element(By.XPATH, '//*[@class="img_reload"]')
        driver.execute_script("arguments[0].click();", element)
        sleep(1)
        verification_code(driver, image_location='./tempFiles/patent_inquire_login.png')
    else:
        element = driver.find_element(By.XPATH, '//input[@id="publiclogin"]')
        driver.execute_script("arguments[0].click();", element)
        # 处理账号或密码错误
        if element_exist(driver, time=5, xpath_path='//span[@class="noty_text"]'):
            return '用户名或密码不正确！'
    # 等待登录加载完成
    WebDriverWait(driver, 40).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="tittle_box"]'), '使用声明'))


# 获取所查询专利号的cookie和token
def gain_cnipa_cookies(driver, patent_number, username, password):
    # 进入查询页面
    driver.get('http://cpquery.cnipa.gov.cn/txnPantentInfoList.do?')
    # 防止cookies失效导致返回登录界面
    if element_exist(driver=driver, time=5, xpath_path='//*[@id="slogo"]'):
        login_cnipa(driver, username=username, password=password)
        gain_cnipa_cookies(driver, patent_number, username, password)
    # 等待元素加载完成
    # explicitWaiting(driver, 20, xpath='//*[@class="tab_top_on"]/p')
    # 等待计算验证码加载完成
    explicitWaiting(driver, 20, xpath='//*[@id="authImg"]')
    # 获取计算验证码结果并处理验证码发生错误
    try:
        code = calculate_code(driver)
    except Exception:
        driver.refresh()
        code = calculate_code(driver)
    # 请求输入过专利号和验证码页面
    driver.get('http://cpquery.cnipa.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=' + (str(
        patent_number)).replace(' ', '') + '&verycode=' + str(code))
    # 防止cookies失效导致返回登录界面
    if element_exist(driver=driver, time=5, xpath_path='//*[@id="slogo"]'):
        login_cnipa(driver, username=username, password=password)
        gain_cnipa_cookies(driver, patent_number, username, password)
    # 处理查询次数使用完了的场景
    if element_exist(driver=driver, xpath_path='//*[@class="binding"]/img', time=0):
        driver.quit()
        return '查询次数已经耗尽'
    # 处理计算验证码失效或超时处理
    while not element_exist(driver=driver, xpath_path='//*[@class="bi_icon"]', time=0):
        code = calculate_code(driver)
        driver.get(
            'http://cpquery.cnipa.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=' + (str(
                patent_number)).replace(' ', '') + '&verycode=' + str(code))

    # 点击进入专利详情页
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div/ul/li[1]/a').click()
    # 等待元素加载完成
    explicitWaiting(driver, 20, xpath='//*[@id="jbxx"]/p')

    # 通过正则获取token
    token = re.findall('token=(.*?)&', driver.current_url)

    # 将cookies持久化保存
    with open('./tempFiles/cookies.json', 'w') as f:
        # 将cookies保存为json格式
        f.write(json.dumps(driver.get_cookies()))

    # 返回token值
    return token[0]


# 根据持久化cookies文件获取cookie
def get_cookies():
    cookie = ''
    with open('./tempFiles/cookies.json', 'r') as f:
        cookies_list = json.load(f)
        for cookies in cookies_list:
            cookie += cookies['name'] + '=' + cookies['value'] + ';'

    return cookie


# 获取专利年费采集cookie
def get_gather_cookies():
    cookie = ''
    with open('./tempFiles/cookies.json', 'r') as f:
        cookies_list = json.load(f)

        for cookies in cookies_list:
            if cookies['name'] == 'UR3ZMlLdcLIES' or cookies['name'] == 'bg78' or cookies['name'] == 'UR3ZMlLdcLIET':
                cookie += cookies['name'] + '=' + cookies['value'] + '; '

        for cookies in cookies_list:
            if cookies['name'] == 'JSESSIONID':
                cookie = cookie + cookies['name'] + '=' + cookies['value']

    return cookie
