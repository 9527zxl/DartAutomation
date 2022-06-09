import json
import re
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.commonUtils import explicitWaiting, verification_code, calculate_code

from utils.driverUtils import FirefoxDriver


def login_gain_cookies(driver, username, password, patent_number, status):
    driver.get('http://cpquery.cnipa.gov.cn/')
    # 全局等待
    driver.implicitly_wait(40)
    # 窗口最大化
    driver.maximize_window()
    driver.refresh()

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
    verification_code(driver=driver, image_location='../tempFiles/patent_inquire_login.png')

    # 处理验证码点击错误进行重新加载
    while driver.find_element(By.XPATH, '//*[@id="selectyzm_text"]').text != '验证成功':
        element = driver.find_element(By.XPATH, '//*[@class="img_reload"]')
        driver.execute_script("arguments[0].click();", element)
        sleep(1)
        verification_code(driver, image_location='../tempFiles/patent_inquire_login.png')
    else:
        element = driver.find_element(By.XPATH, '//input[@id="publiclogin"]')
        driver.execute_script("arguments[0].click();", element)
    # 等待登录加载完成
    WebDriverWait(driver, 40).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="tittle_box"]'), '使用声明'))

    # 跳过使用声明，进入查询页面
    driver.get('http://cpquery.cnipa.gov.cn/txnPantentInfoList.do?')
    # 等待元素加载完成
    explicitWaiting(driver, 20, xpath='//*[@class="tab_top_on"]/p')
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
    # 等待元素加载完成
    explicitWaiting(driver, 20, xpath='/html/body/div[2]/div[1]/div[2]/div[2]/div/ul/li[1]/a')
    # 处理计算验证码失效或超时处理
    while not driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/div/ul/li[1]/a').is_displayed():
        code = calculate_code(driver)
        driver.get(
            'http://cpquery.cnipa.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=' + (str(
                patent_number)).replace(' ', '') + '&verycode=' + str(code))

    # 点击进入专利详情页
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div/ul/li[1]/a').click()
    # 等待元素加载完成
    explicitWaiting(driver, 20, xpath='//*[@id="jbxx"]/p')

    # 通过正则获取token
    if status == 'token':
        token = re.findall('token=(.*?)&', driver.current_url)
        return token

    # 获取cookie值
    cookie = ''
    cookies_json = json.dumps(driver.get_cookies())
    cookies_list = json.loads(cookies_json)
    if status == 'cookie':
        for cookies in cookies_list:
            cookie += cookies['name'] + '=' + cookies['value'] + ';'
        return cookie


driver = FirefoxDriver()
login_gain_cookies(driver, username='15156052212', password='Zhixin888*', patent_number='2015108746518', status='')
