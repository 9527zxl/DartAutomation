from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions


def FirefoxDriver():
    # 火狐浏览器驱动
    options = FirefoxOptions()
    # options.add_argument('--headless')  # 无头浏览器
    driver_path = 'D:\PythonWarehouse\DartAutomation\driver\geckodriver.exe'
    return Firefox(executable_path=driver_path, options=options)
