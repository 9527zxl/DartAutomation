import sys
import tkinter
import tkinter.messagebox


# 退出程序
def quitGui():
    sys.exit()


# 登录
def loginGui():
    if account_input.get() == '':
        tkinter.messagebox.showerror(title='error', message='账号不能为空!')
    elif password_input.get() == '':
        tkinter.messagebox.showerror(title='error', message='密码不能为空!')
    elif account_input.get() != '' and password_input.get() != '':
        tkinter.messagebox.showinfo(title='登录中。。。', message='请耐心等待')
        # 登录飞镖网后台
        # driver = FirefoxDriver(path=os.path.abspath(os.curdir) + '\driver\geckodriver.exe')
        # login_return = login_get_cookies(driver, username=account_input.get(), password=password_input.get())
        login_return = '登录成功'
        if login_return == '登录成功':
            window.destroy()  # 关闭登录窗口
            from tkinter_main import Annual_update_button
            Annual_update_button()
        elif login_return == '登录失败，用户名或密码不正确！':
            tkinter.messagebox.showerror(title='error', message=login_return)


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
