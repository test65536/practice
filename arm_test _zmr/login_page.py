from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QPushButton,QMessageBox,QApplication,QCommandLinkButton,QGridLayout,QGroupBox,QDesktopWidget
from PyQt5 import QtGui,QtCore
import pymysql
import sys
from home_page import Home_window


class Login_window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.login_btn.clicked.connect(self.login)
        self.esc_btn.clicked.connect(self.Esc)

    def initUI(self):
        self.resize(800,500)
        self.center()
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowTitle('屋顶绿化系统登录界面')
        self.setWindowIcon(QtGui.QIcon('/home/arm/3/image/window_icon.png'))
        self.image = QtGui.QMovie('/home/arm/3/image/timg.gif')
        self.bg_image = QLabel(self)
        self.bg_image.setMovie(self.image)
        self.image.start()
        self.bg_image.setGeometry(0,0,800,500)
        font = QtGui.QFont()
        font.setFamily("华文彩云")
        self.titleLabel = QLabel("<html><head/><body><p align='center'><span style='font-size:30pt; color:#ffffff;'>屋顶绿化系统</span></p></body></html>", self)
        self.titleLabel.setFont(font)
        self.titleLabel.setGeometry(250,100, 300, 60)
        self.userLabel = QLabel('<font color = white>用户名：</font>',self)
        self.userLabel.setGeometry(250,300,60,30)
        self.userEntry = QLineEdit(self)
        self.userEntry.setPlaceholderText('用户名')
        self.userEntry.setGeometry(320,300,200,25)
        self.pswdLabel = QLabel('<font color = white>密码：</font>', self)
        self.pswdLabel.setGeometry(250, 330, 60, 30)
        self.pswdEntry = QLineEdit(self)
        self.pswdEntry.setPlaceholderText('密码')
        self.pswdEntry.setEchoMode(QLineEdit.Password)
        self.pswdEntry.setGeometry(320, 330, 200, 25)
        self.login_btn = QPushButton('登录',self)
        self.login_btn.setGeometry(320,380,80,30)
        self.esc_btn = QPushButton('退出', self)
        self.esc_btn.setGeometry(440, 380, 80, 30)
        self.forget_btn = QCommandLinkButton('忘记密码',self)
        self.forget_btn.setStyleSheet("color:white")
        self.forget_btn.clicked.connect(self.forget_pswd)
        self.forget_btn.move(520,300)

        self.show()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def forget_pswd(self):
        print('找回密码')
        self.the_window = Forget_pswd()
        self.the_window.initUI()

    def login(self):
        pymysql_ip = "10.0.0.111"
        pymysql_pswd = "password"
        db = pymysql.connect(pymysql_ip,'root',pymysql_pswd,'green')
        cursor = db.cursor()
        sql = "select * from user_list"
        cursor.execute(sql)
        user_info = cursor.fetchall()
        print('用户信息表：',user_info)
        print('**************************')
        print('输入的用户名：',self.userEntry.text())
        print('输入的密码：',self.pswdEntry.text())
        print('**************************')
        flag = 0
        for i in user_info:
            if (self.userEntry.text()==i[0])&(self.pswdEntry.text()==i[1]):
                flag = 1
                print('登陆成功！')
                self.Jump_to_home(i[2])
                break
        if flag == 0:
            print('用户名或者密码错误！')
            self.Wrong_user()


    def Wrong_user(self):
        button = QMessageBox.warning(self,"登录错误","用户名或者密码错误！",
                                     QMessageBox.Ok,QMessageBox.Ok)
        if button ==QMessageBox.Ok:
            return
        else:
            return
    def Esc(self):
        self.close()
    #跳转页面
    def Jump_to_home(self,user_level):
        self.close()
        self.home_winodw = Home_window()
        self.home_winodw.initUI(user_level)

class Forget_pswd(QWidget):
    def initUI(self):
        self.resize(600,400)
        self.center()
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowTitle('忘记密码')
        self.setWindowIcon(QtGui.QIcon('/home/arm/3/image/forget_pswd.jpg'))
        user_name = QLabel('请输入您的用户名：')
        self.user_name = QLineEdit()
        user_pthone_num = QLabel('请输入您设置的手机号：')
        self.pthone_num_e = QLineEdit()
        btn1 = QPushButton('确定')
        btn2 = QPushButton('退出')
        btn2.clicked.connect(self.cancel_the_w)
        btn1.clicked.connect(self.confirm_the_w)
        layout1 = QGridLayout()
        layout2 = QGridLayout()
        layout1.addWidget(user_name, 0, 0)
        layout1.addWidget(self.user_name, 0, 1)
        layout1.addWidget(user_pthone_num,1,0)
        layout1.addWidget(self.pthone_num_e,1,1)
        layout2.addWidget(btn1,0,1)
        layout2.addWidget(btn2,0,3)
        group1 = QGroupBox('输入信息',self)
        group2 = QGroupBox(self)
        group1.setLayout(layout1)
        group1.setGeometry(100,50,400,200)
        group2.setLayout(layout2)
        group2.setGeometry(200,250,200, 100)
        self.show()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def confirm_the_w(self):
        pymysql_ip = "10.0.0.33"#找回密码，需要连接我的数据库
        pymysql_pswd = "zong123"
        db = pymysql.connect(pymysql_ip,"root",pymysql_pswd,"green_roof")
        cursor = db.cursor()
        print('确定')
        sql = "select * from forget_password"
        cursor.execute(sql)
        user_info =cursor.fetchall()
        print(user_info)
        user_name = self.user_name.text()
        user_phone = self.pthone_num_e.text()
        flag = 0
        for i in user_info:
            if (user_name == i[0])&(user_phone == i[1]):
                password = i[2]
                flag = 1
                button = QMessageBox.information(self, "正确密码", "您的密码是%s请妥善保管！"%(password),
                                             QMessageBox.Ok, QMessageBox.Ok)
                if button == QMessageBox.Ok:
                    self.close()
                    return
                else:
                    self.close()
                    return
        if flag == 0:
            button = QMessageBox.warning(self, "信息错误", "用户名不存在或者手机号填写错误！",
                                         QMessageBox.Ok, QMessageBox.Ok)
            if button == QMessageBox.Ok:
                return
            else:
                return

    def cancel_the_w(self):
        self.close()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    the_window = Login_window()
    sys.exit(app.exec_())
