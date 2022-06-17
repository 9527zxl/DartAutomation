import os
import sys
import tkinter
import tkinter.messagebox
from tkinter import scrolledtext, END, X, HORIZONTAL
from tkinter.ttk import Separator

from utils.commonUtils import login_get_cookies

from utils.driverUtils import FirefoxDriver


# 退出程序
def quitGui():
    sys.exit()


# 登录
def loginGui():
    if account_input.get() == '':
        tkinter.messagebox.showinfo(title='error', message='账号不能为空!')
    elif password_input.get() == '':
        tkinter.messagebox.showinfo(title='error', message='密码不能为空!')
    elif account_input.get() != '' and password_input.get() != '':
        # 登录飞镖网后台
        # driver = FirefoxDriver(path=os.path.abspath(os.curdir) + '\driver\geckodriver.exe')
        # login_return = login_get_cookies(driver, username=account_input.get(), password=password_input.get())
        login_return = '登录成功'
        if login_return == '登录成功':
            window.destroy()  # 关闭登录窗口
            mainGUi()
        elif login_return == '登录失败，用户名或密码不正确！':
            tkinter.messagebox.showinfo(title='error', message=login_return)


# 修改按钮
def amendGui(account, password):
    account.configure(state='normal')
    password.configure(state='normal')


# 保存按钮
def saveGui(account, password):
    account.configure(state='disable')
    password.configure(state='disable')

    # 获取文本框内容
    account_result = account.get("1.0", "end").split('\n')
    password_result = password.get("1.0", "end").split('\n')
    # 处理文本内容
    account_result.remove('')
    password_result.remove('')

    data = []
    ss = dict(zip(account_result, password_result))
    for key, value in ss.items():
        data.append(key + '       ' + value)
    # 持久化处理
    with open('./tempFiles/account.txt', 'w') as f:
        f.write('\n'.join(data))


# 主界面
def mainGUi():
    main = tkinter.Tk()
    main.title('欢迎您，今天的工作开始了')
    main.geometry('400x400+500+300')
    # 设置图标
    main.iconbitmap('./tempFiles/favicon.ico')
    # 专利查询网标题
    patent_text = tkinter.Label(main, text='中国及多国专利审查信息查询', font=('宋体', 16))
    patent_text.pack()

    # 账号标题
    account_word = tkinter.Label(main, text='账号', font=('仿宋', 11))
    account_word.place(x=95, y=35)
    # 密码标题
    password_word = tkinter.Label(main, text='密码', font=('仿宋', 11))
    password_word.place(x=260, y=35)

    # 创建账号文本框 设置滚动条
    account = scrolledtext.ScrolledText(main, font=('宋体', 14), width=12, height=9)
    account.place(x=50, y=60)
    # 创建密码文本框 设置滚动条
    password = scrolledtext.ScrolledText(main, font=('宋体', 14), width=15, height=9)
    password.place(x=200, y=60)

    # 读取账户密码显示出来
    with open('./tempFiles/account.txt', 'r') as f:
        data = f.read().split('\n')

    dispose = ','.join(data).split('       ')
    account_result = []
    password_result = []
    for index, value in enumerate(','.join(dispose).split(',')):
        if index == 0:
            account_result.append(value)
        if index % 2 == 0 and index != 0:
            account_result.append(value)
        elif index % 2 != 0 and index != 0:
            password_result.append(value)

    # 显示账户
    for i in account_result:
        account.insert(END, i + '\n')
    # 锁定账户文本框
    account.configure(state='disabled')

    # 显示密码
    for i in password_result:
        password.insert(END, i + '\n')
    # 锁定密码文本框
    password.configure(state='disabled')

    # 保存按钮
    save = tkinter.Button(main, text='保存', font=('宋体', 11), command=lambda: saveGui(account, password))
    save.place(x=250, y=250)
    # 修改按钮
    amend = tkinter.Button(main, text='修改', font=('宋体', 11), command=lambda: amendGui(account, password))
    amend.place(x=90, y=250)

    # 分割线
    sep = Separator(main, orient=HORIZONTAL)  # VERTICAL为竖的分割线
    sep.pack(padx=10, fill=X)

    dd = Separator(main, orient=HORIZONTAL)  # HORIZONTAL建立水平分隔线，VERTICAL建立垂直分隔线
    dd.pack(fill=X, pady=220)

    # 年费状态更新按钮
    # annual_fee_status = tkinter.Button(main, text='年费状态更新', font=('宋体', 12))
    # annual_fee_status.place(x=20, y=290)

    main.mainloop()


window = tkinter.Tk()
# 设置窗口文字
window.title('飞镖自动化-登录')
# 设置窗口大小及位置
window.geometry('300x300+500+300')
# 设置图标
window.iconbitmap('./tempFiles/favicon.ico')
# 设置背景色
# window['bg'] = '#ADB4BC'

# 标题
login_text = tkinter.Label(window, text='飞镖网-管理后台', font=('黑体', 19))
login_text.pack()

# 账号及输入窗口
account_text = tkinter.Label(window, text='账号:', font=('宋体', 12), width=10, height=2)
account_text.place(x=12, y=82, width=50, height=20)
account_input = tkinter.Entry(window, width=20)
account_input.place(x=80, y=80, width=160, height=23)

# 密码及输入窗口
password_text = tkinter.Label(window, text='密码:', font=('宋体', 12), width=10, height=2)
password_text.place(x=12, y=152, width=50, height=20)
password_input = tkinter.Entry(window, show='*', width=20)
password_input.place(x=80, y=150, width=160, height=23)

# 登录按钮
login = tkinter.Button(window, text="登录", font=('宋体', 10), command=loginGui)
login.place(x=50, y=220, width=60, height=30)
# 退出按钮
quitTkinter = tkinter.Button(window, text="退出", font=('宋体', 10), command=quitGui)
quitTkinter.place(x=190, y=220, width=60, height=30)

window.mainloop()
