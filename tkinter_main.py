import os
import random
import tkinter
from tkinter import HORIZONTAL, X, scrolledtext, END
from tkinter.ttk import Separator
import tkinter.messagebox
from utils.cnipaUtils import login_cnipa, gain_cnipa_cookies, get_cookies
from utils.commonUtils import gain_feibiao_cookie
from utils.driverUtils import FirefoxDriver
from utils.requestsUtils import get_acquisition_patent_Number, annual_fee_to_update


# 年费采集按钮
def Annual_update_button():
    if account_frame.get() == '':
        tkinter.messagebox.showerror(title='error', message='账号不能为空!')
    elif password_frame.get() == '':
        tkinter.messagebox.showerror(title='error', message='密码不能为空!')
    elif account_frame.get() != '' and password_frame.get() != '':
        main.withdraw()

        infobox_main = tkinter.Tk()
        infobox_main.title('开始更新')
        infobox_main.geometry('400x200+500+300')
        # 设置图标
        infobox_main.iconbitmap('./tempFiles/favicon.ico')
        # 创建账号文本框 设置滚动条
        message_box = scrolledtext.ScrolledText(infobox_main, font=('宋体', 14), width=12, height=9)
        message_box.place(x=0, y=0, width=400, height=200)

        message_box.insert(END, '账号：' + account_frame.get() + '\n')
        message_box.insert(END, '密码：' + password_frame.get() + '\n')

        driver = FirefoxDriver(path=os.path.abspath(os.curdir) + '\driver\geckodriver.exe')
        # 获取飞镖网cookie
        feibiao_cookie = gain_feibiao_cookie()
        # 登录查询网站
        login_cnipa(driver, username=account_frame.get(), password=password_frame.get())
        state = True
        count = 0
        while state:
            count = count + 1
            infobox_main.update()
            message_box.insert(END, '开始第' + str(count) + '更新(每次更新20个)' + '\n')
            # 获取专利号
            patent_number = random.choice(get_acquisition_patent_Number(feibiao_cookie, state=False))
            # 获取token
            token = gain_cnipa_cookies(driver, patent_number=patent_number)
            if token == '查询次数已经耗尽':
                state = False
            # 获取cookie
            cookie = get_cookies()
            # 获取id
            ids = get_acquisition_patent_Number(feibiao_cookie, state=True)
            # 更新
            for id in ids:
                response = annual_fee_to_update(feibiao_cookie=feibiao_cookie, update_cookie=cookie, update_token=token,
                                                id=id)
                message_box.insert(END, response + '\n')
                print(response)

        infobox_main.mainloop()


main = tkinter.Tk()
main.title('欢迎您，今天的工作开始了')
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

# 状态更新
update_the_state = tkinter.Button(main, text='状态更新', font=('宋体', 9))
update_the_state.place(x=32, y=162, width=70, height=30)
# 年费采集
annual_fee_collection = tkinter.Button(main, text='年费采集', font=('宋体', 9), command=Annual_update_button)
annual_fee_collection.place(x=182, y=162, width=70, height=30)

main.mainloop()
