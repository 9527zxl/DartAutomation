from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions


def FirefoxDriver(path, state):
    """
    :param state: 状态
    :param path: driver浏览器驱动位置
    :return: 浏览器驱动
    """
    # 火狐浏览器驱动
    options = FirefoxOptions()
    # if state:
    #     options.add_argument('--headless')  # 无头浏览器
    # 页面加载策略
    options.page_load_strategy = 'eager'
    driver_path = path
    return Firefox(executable_path=driver_path, options=options)
