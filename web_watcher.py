from tkinter import *
from tkinter.scrolledtext import ScrolledText
import threading, time
import urllib.request as urlreq


# 外观状态的改变
def disab_lfm1():
    entr1_1["state"] = "disable"
    entr1_2["state"] = "disable"


def enab_lfm1():
    entr1_1["state"] = "normal"
    entr1_2["state"] = "normal"
    checkbox1_3["state"] = "normal"


def enab_lfm2():
    entr2_1["state"] = "normal"
    entr2_2["state"] = "normal"
    entr2_3["state"] = "normal"
    entr2_4["state"] = "normal"
    entr2_5["state"] = "normal"
    entr2_6["state"] = "normal"


def disab_lfm2():
    entr2_1["state"] = "disable"
    entr2_2["state"] = "disable"
    entr2_3["state"] = "disable"
    entr2_4["state"] = "disable"
    entr2_5["state"] = "disable"
    entr2_6["state"] = "disable"


def change_stat():
    if checkbox_val.get():
        enab_lfm2()
    else:
        disab_lfm2()


# 发送SMTP邮件
def send_mail():
    import smtplib
    from email.mime.text import MIMEText
    msg_from = entr2_6.get()  # 发件人
    passwd = entr2_3.get()  # 密码
    msg_to = entr2_5.get()  # 收件人
    subject = entr2_4.get()
    content = entr1_1.get() + entr2_4.get() + "\n告警！告警！！告警！！！"
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        sendM = smtplib.SMTP(entr2_1.get(), 25)
        sendM.login(msg_from, passwd)
        sendM.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except smtplib.SMTPException as e:
        print("发送失败")
    finally:
        sendM.quit()


# 从停止中点击开始运行后的状态改变
def start_moniter():
    global monit_state, td
    txinfo3_1.delete(0.0, END)
    monit_state = True
    btn1_r["state"] = "disable"
    btn1_r['text'] = "运行中"
    btn2_r["text"] = "停止"
    btn2_r["state"] = "normal"
    checkbox1_3["state"] = "disable"
    disab_lfm2()
    disab_lfm1()
    unm = 0
    while monit_state:
        unm += 1
        web_moniter()  # 无限循环的监控
        time.sleep(int(entr1_2.get()))


# 创建新的线程
def new_thread():
    global td
    td = threading.Thread(target=start_moniter)
    td.setDaemon(True)
    td.start()


# 线程中要运行的无限循环
def web_moniter():
    urladd = entr1_1.get()
    timeot = int(entr1_2.get())
    try:
        web_f = urlreq.urlopen(url=urladd, timeout=timeot)
        print(web_f.getcode())
        if web_f.getcode() == 200:
            succ_info = "%s正常\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("%s" % (succ_info))
            txinfo3_1.insert(END, succ_info)
            txinfo3_1.see(END)
    except:
        fail_info = "%s不正常\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("%s" % (fail_info))
        txinfo3_1.insert(END, fail_info)
        if checkbox_val.get():
            send_mail()


# 从运行中停止后的改变
def stop_moniter():
    global monit_state
    print(td.isAlive())
    monit_state = False
    btn1_r["state"] = "normal"
    btn1_r['text'] = "开始"
    btn2_r["text"] = "停止中"
    btn2_r["state"] = "disable"
    checkbox1_3["state"] = "disable"
    enab_lfm1()
    if checkbox_val.get():
        enab_lfm2()
    else:
        disab_lfm2()


# 构造windows外观及默认值
root = Tk()
root.title("网页监控1.5")
root.resizable(0, 0)
labelframe1 = LabelFrame(root, width=25, height=30, text="监控信息")
labelframe1.grid(row=0, column=0)
labelframe2 = LabelFrame(root, width=25, height=20, text="邮件信息")
labelframe2.grid(row=1, column=0)
labelframe3 = LabelFrame(root, text="监控结果")
labelframe3.grid(row=0, column=1, rowspan=3)
leble1_1 = Label(labelframe1, text="需监控的网页：")
leble1_1.grid(row=0, column=0, sticky=W)
leble1_2 = Label(labelframe1, text="监控时间间隔(s)：")
leble1_2.grid(row=2, column=0, sticky=W, )
web_addr = StringVar()
web_addr.set("http://www.baidu.com")
entr1_1 = Entry(labelframe1, width=32, textvariable=web_addr)  # 网页地址
entr1_1.grid(row=1, column=0, columnspan=2, sticky=W)
moni_time = IntVar()
moni_time.set(10)
entr1_2 = Entry(labelframe1, width=10, textvariable=moni_time)  # 监控时间
entr1_2.grid(row=3, column=0, sticky=W)
checkbox_val = BooleanVar()
checkbox_val.set(False)
checkbox1_3 = Checkbutton(labelframe1, variable=checkbox_val, text="是否邮件提醒", command=change_stat)
checkbox1_3.grid(row=3, column=1)
leble2_1 = Label(labelframe2, text="SMTP服务器(端口:25)：")
leble2_1.grid(row=0, column=0, sticky=W)
leble2_2 = Label(labelframe2, text="账    户：")
leble2_2.grid(row=2, column=0, sticky=W)
leble2_3 = Label(labelframe2, text="密    码：")
leble2_3.grid(row=4, column=0, sticky=W)
leble2_4 = Label(labelframe2, text="邮件标题：")
leble2_4.grid(row=6, column=0, sticky=W)
leble2_5 = Label(labelframe2, text="收件人(1个)：")
leble2_5.grid(row=8, column=0, sticky=W)
leble2_6 = Label(labelframe2, text="发件人(@全称)：")
leble2_6.grid(row=10, column=0, sticky=W)
smtp_var = StringVar()
smtp_var.set("smtp.163.com")
entr2_1 = Entry(labelframe2, width=30, textvariable=smtp_var, state="disable")
entr2_1.grid(row=1, column=0)
user_var = StringVar()
user_var.set("users")
entr2_2 = Entry(labelframe2, width=30, textvariable=user_var, state="disable")
entr2_2.grid(row=3, column=0)
pw_var = StringVar()
pw_var.set("password")
entr2_3 = Entry(labelframe2, width=30, textvariable=pw_var, show="@", state="disable")
entr2_3.grid(row=5, column=0)
title_var = StringVar()
title_var.set("-*-网页无法访问-*-")
entr2_4 = Entry(labelframe2, width=30, textvariable=title_var, state="disable")
entr2_4.grid(row=7, column=0)
title_var = StringVar()
title_var.set("user@163.com")
entr2_5 = Entry(labelframe2, width=30, textvariable=title_var, state="disable")
entr2_5.grid(row=9, column=0)
title_var = StringVar()
title_var.set("user@163.com")
entr2_6 = Entry(labelframe2, width=30, textvariable=title_var, state="disable")
entr2_6.grid(row=11, column=0)
txinfo3_1 = ScrolledText(labelframe3, height=40, width=30)
txinfo3_1.pack()
frame4 = Frame(root)
frame4.grid(row=2, column=0)
btn1_r = Button(frame4, width=10, text="开始", command=new_thread)
btn1_r.grid(row=0, column=0)
btn2_r = Button(frame4, width=10, text="停止中", state="disable", command=stop_moniter)
btn2_r.grid(row=0, column=1)
monit_state = True
root.mainloop()
