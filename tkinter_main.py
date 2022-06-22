import os
import random
import tkinter
from time import sleep
from tkinter import HORIZONTAL, X
from tkinter.ttk import Separator
import tkinter.messagebox

from utils.cnipaUtils import login_cnipa, gain_cnipa_cookies, get_cookies
from utils.commonUtils import gain_feibiao_cookie
from utils.driverUtils import FirefoxDriver
from utils.requestsUtils import get_acquisition_patent_Number, annual_fee_to_update, get_patent_number, \
    update_successfully, patent_update, annual_update

on_state = True


# 年费状态更新按钮
def Annual_status_update():
    if account_frame.get() == '':
        tkinter.messagebox.showerror(title='error', message='账号不能为空!')
    elif password_frame.get() == '':
        tkinter.messagebox.showerror(title='error', message='密码不能为空!')
    elif account_frame.get() != '' and password_frame.get() != '':
        driver = FirefoxDriver(path=os.path.abspath(os.curdir) + '\driver\geckodriver.exe',
                               state=False if condition.get() == 1 else on_state)
        # 获取飞镖cookie
        feibiao_cookie = gain_feibiao_cookie()
        # 登录查询网站
        sleep_state = True
        login_cnipa(driver, username=account_frame.get(), password=password_frame.get())
        while True:
            update_number1 = update_successfully(feibiao_cookie=feibiao_cookie)
            # 获取年费状态更新账号以及捕获异常
            patent_number = ''
            try:
                patent_number = str(get_patent_number(feibiao_cookie=feibiao_cookie))
                print('年费状态更新专利号:' + str(patent_number))
            except IndexError:
                tkinter.messagebox.showerror(title='error', message='年费状态更新无数据!')
                driver.quit()
                break
            # 获取更新
            token = gain_cnipa_cookies(driver, patent_number=patent_number)
            if token == '查询次数已经耗尽':
                driver.quit()
                tkinter.messagebox.showinfo(title='error', message='查询次数已经耗尽!')
                break
            print('token:' + str(token))
            # 获取更新cookie
            cookie = get_cookies()
            print('cookie:' + str(cookie))
            # 年费状态更新
            patent_update(feibiao_cookie=feibiao_cookie, update_cookie=cookie, update_token=token)

            while sleep_state:
                sleep(30)
                update_number2 = update_successfully(feibiao_cookie=feibiao_cookie)
                print('update_number1=' + str(update_number1))
                print('update_number2=' + str(update_number2))
                print('等待中。。。')
                if update_number1 < update_number2:
                    sleep_state = False
                    break


# 年费采集按钮
def Annual_update_button():
    if account_frame.get() == '':
        tkinter.messagebox.showerror(title='error', message='账号不能为空!')
    elif password_frame.get() == '':
        tkinter.messagebox.showerror(title='error', message='密码不能为空!')
    elif account_frame.get() != '' and password_frame.get() != '':
        driver = FirefoxDriver(path=os.path.abspath(os.curdir) + '\driver\geckodriver.exe',
                               state=False if condition.get() == 1 else on_state)
        # 获取飞镖网cookie
        feibiao_cookie = gain_feibiao_cookie()
        # 登录查询网站
        login_cnipa(driver, username=account_frame.get(), password=password_frame.get())
        state = True
        while state:
            # 获取专利号
            patent_number = random.choice(get_acquisition_patent_Number(feibiao_cookie, state=False))
            # 获取token
            token = gain_cnipa_cookies(driver, patent_number=patent_number)
            if token == '查询次数已经耗尽':
                state = False
                tkinter.messagebox.showinfo(title='error', message='查询次数已经耗尽!')
                continue
            # 获取cookie
            cookie = get_cookies()
            # 获取id
            ids = get_acquisition_patent_Number(feibiao_cookie, state=True)
            # 更新 模式一
            # annual_fee_to_update(feibiao_cookie=feibiao_cookie, update_cookie=cookie, update_token=token, ids=ids)
            # sleep(10)

            # 模式二
            for id in ids:
                annual_update(feibiao_cookie=feibiao_cookie, update_cookie=cookie, update_token=token, id=id)


main = tkinter.Tk()
main.title('欢迎您，开始今天的工作')
main.geometry('300x240+500+300')
# 设置图标
main.iconbitmap('./tempFiles/favicon.ico')
# 专利查询网标题
patent_text = tkinter.Label(main, text='中国及多国专利审查信息查询', font=('宋体', 16))
patent_text.pack()
# 分割线
sep = Separator(main, orient=HORIZONTAL)  # VERTICAL为竖的分割线
sep.pack(padx=10, fill=X)

# 账号
account = tkinter.Label(main, text='账号:', font=('宋体', 12), width=10, height=2)
account.place(x=22, y=52, width=50, height=20)
account_frame = tkinter.Entry(main, width=20)
account_frame.place(x=112, y=52, width=120, height=23)

# 密码
password = tkinter.Label(main, text='密码:', font=('宋体', 12), width=10, height=2)
password.place(x=22, y=102, width=50, height=20)
password_frame = tkinter.Entry(main, show='*', width=20)
password_frame.place(x=112, y=102, width=120, height=23)

# 勾选框
condition = tkinter.IntVar()
condition.set(0)
Checkbutton = tkinter.Checkbutton(main, text='显示浏览器窗口', font=('宋体', 8), variable=condition, onvalue=1, offvalue=0)
Checkbutton.place(x=35, y=140)

# 状态更新
update_the_state = tkinter.Button(main, text='状态更新', font=('宋体', 9), command=Annual_status_update)
update_the_state.place(x=32, y=172, width=70, height=30)
# 年费采集
annual_fee_collection = tkinter.Button(main, text='年费采集', font=('宋体', 9), command=Annual_update_button)
annual_fee_collection.place(x=182, y=172, width=70, height=30)

main.mainloop()
