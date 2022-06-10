import gc
import json
import os
from io import BytesIO
from time import sleep

import ddddocr
from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

ocr = ddddocr.DdddOcr(show_ad=False)
xy_ocr = ddddocr.DdddOcr(det=True, show_ad=False)


#  显示等待 等待某个元素加载完成
def explicitWaiting(driver, waiting_time: int, xpath: str):
    """

    :param driver:  浏览器驱动对象
    :param waiting_time: 等待时间
    :param xpath: xpath路径
    """
    WebDriverWait(driver, waiting_time).until(EC.presence_of_all_elements_located((By.XPATH, xpath)), message='超时啦!')


# 截取验证码
def interceptPicture(driver, image_location, xpath):
    """
    :param driver: 浏览器驱动对象
    :param image_location: 图片地址路径以.png结尾
    :param xpath: 验证码定位xpath
    :return: 验证码字节
    """
    driver.save_screenshot(image_location)
    location_code = driver.find_element(By.XPATH, xpath)  # 定位验证码
    location = location_code.location  # 获取验证码x,y轴坐标
    size = location_code.size  # 获取验证码的长宽
    coord = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
             int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    i = Image.open(image_location)  # 打开截图
    frame4 = i.crop(coord)  # 使用Image的crop函数，从截图中再次截取需要的区域
    img_byte = BytesIO()  # 转成Bytes数据存储在内存中
    frame4.save(img_byte, 'png')  # 保存接下来的验证码图片 进行打码
    os.remove(image_location)  # 删除全屏截图图片
    return img_byte


# 对于计算验证码的处理
def calculate_code(driver):
    """
    :param driver: 浏览器驱动对象
    :return: 计算验证码结果
    """
    calculate_code_bytes = interceptPicture(driver, image_location='./tempFiles/calculate_code.png',
                                            xpath='//*[@id="authImg"]')
    word = ocr.classification(calculate_code_bytes.getvalue())
    # 对ocr识别后的字符串进行处理
    number = list(word)
    code = 0
    if number[1] == '-':
        code = int(number[0]) - int(number[2])
    elif number[1] == '+':
        code = int(number[0]) + int(number[2])

    gc.collect()  # 释放内存
    return code


# 截取登录验证码图片并点击
def verification_code(driver, image_location):
    """
    :param driver: 浏览器驱动对象
    :param image_location: 图片地址路径以.png结尾
    """
    # 获取验证码图片
    img_byte = interceptPicture(driver, image_location, xpath='//*[@id="jcaptchaimage"]')

    img = Image.open(img_byte)
    img = img.crop((0, 0, 280, 220))  # 裁剪图片
    img_byte = BytesIO()  # 转成Bytes数据存储在内存中
    img.save(img_byte, 'png')
    content = img_byte.getvalue()
    xy_list = xy_ocr.detection(content)  # 识别验证码获取坐标

    # 处理坐标数据
    img_xy = []
    for row in xy_list:
        x1, y1, x2, y2 = row
        # 裁剪出单个字
        corp = img.crop(row)
        img_byte = BytesIO()
        corp.save(img_byte, 'png')
        # 识别出单个字
        word = ocr.classification(img_byte.getvalue())
        a = dict(code=word, X=int((x1 + x2) / 2), Y=int((y1 + y2) / 2))
        img_xy.append(a)

    # 等待验证码文字加载完成
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="selectyzm_text"]')),
                                    message='超时啦!')
    # 获取验证码文字
    code_text = driver.find_element(By.XPATH, '//*[@id="selectyzm_text"]').text
    data = code_text.split('"')
    sleep(2)

    location_code = driver.find_element(By.XPATH, '//*[@id="jcaptchaimage"]')  # 定位验证码
    # 根据坐标点击验证码
    for ss in data:
        for coord_id in img_xy:
            if ss == coord_id['code']:
                try:
                    ActionChains(driver).move_to_element_with_offset(location_code, coord_id['X'],
                                                                     coord_id['Y']).click().perform()
                    sleep(0.5)
                except Exception:
                    pass

    gc.collect()


# 登录飞镖网获取cookies
def login_get_cookies(driver, username, password):
    """
    :param driver:  浏览器驱动对象
    :param username:  飞镖网账号
    :param password:  飞镖网密码
    """
    driver.get('http://www.ipfeibiao.com/manager/frame/index')
    driver.maximize_window()

    # 定位元素输入账号密码
    driver.find_element(By.XPATH, "//input[@name='user_name']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)

    # 获取验证码
    code_byte = interceptPicture(driver, image_location='./tempFiles/feibiao_print_screen.png',
                                 xpath='//*[@id="img_captcha"]')
    code = ocr.classification(code_byte.getvalue())

    # 输入验证码
    driver.find_element(By.XPATH, "//input[@name='captcha']").send_keys(code)

    # 点击登录按钮
    driver.find_element(By.XPATH, "//input[@class='loginin']").click()

    # 判断文字元素存不存在
    def error(xpath, text):
        try:
            WebDriverWait(driver, 2).until(
                EC.text_to_be_present_in_element((By.XPATH, xpath), text))
            return True
        except:
            return False

    # 处理验证码识别错误
    while error(xpath="//div[@class='layui-layer-content']", text='验证码不正确'):
        login_get_cookies(driver, username, password)
    # 输入账号密码错误场景
    if error(xpath="//div[@class='layui-layer-content']", text='登录失败，用户名或密码不正确！'):
        driver.quit()
        return '登录失败，用户名或密码不正确！'

    # 等待登录完成
    explicitWaiting(driver, waiting_time=20, xpath='//*[@id="LAY_app"]/div[1]/div[2]/div/div/span')

    # 获取cookies
    cookies_list = json.dumps(driver.get_cookies())
    # 持久化cookies
    with open('./tempFiles/feibiao_cookies.json', 'w') as f:
        f.write(cookies_list)

    driver.quit()


# 获取飞镖网cookie
def gain_feibiao_cookie():
    """
    :return: 返回飞镖网cookie
    """
    with open('../tempFiles/feibiao_cookies.json', 'r') as f:
        cookies_list = json.load(f)
        cookie = cookies_list[0]['name'] + '=' + cookies_list[0]['value'] + ';' + cookies_list[1]['name'] + '=' + \
                 cookies_list[1]['value']

    return cookie
