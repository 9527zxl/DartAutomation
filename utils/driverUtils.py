from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions


def FirefoxDriver(path):
    """
    :param path: driver浏览器驱动位置
    :return: 浏览器驱动
    """
    # 火狐浏览器驱动
    options = FirefoxOptions()
    # options.add_argument('--headless')  # 无头浏览器
    driver_path = path
    return Firefox(executable_path=driver_path, options=options)
