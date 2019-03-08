from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QApplication,QDesktopWidget,QGroupBox,QGridLayout,QComboBox,QAbstractButton
from PyQt5.QtGui import QFont,QPixmap,QIcon
import sys
import pymysql
import time
from PIL import Image
class Manual_window(QWidget):
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def initUI(self):
        self.db = pymysql.connect('10.0.0.111','root','password','green')
        self.db.autocommit(True)
        self.cursor = self.db.cursor()
        #启动手模式
        sql = "update command1 set manual = 'Y'"
        self.cursor.execute(sql)
        self.db.commit()
        self.resize(1000,600)
        self.center()
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon('image/hand.png'))
        self.setWindowTitle('手动模式')
        bg = QPixmap('image/all_set_bg.png')
        bg_l = QLabel(self)
        bg_l.setPixmap(bg)
        bg_l.setGeometry(0, 0, 1000, 600)
        water_source = ['选择','自来水','蓄水池']
        l1 = QLabel('选择水源')
        the_box = QComboBox()
        the_box.addItems(water_source)
        the_box.activated[str].connect(self.chose_source)
        lay = QGridLayout()
        lay.addWidget(l1,0,0)
        lay.addWidget(the_box,0,1)
        self.g1 = QGroupBox(self)
        self.g1.setLayout(lay)
        self.g1.setFont(QFont('楷体',15))
        self.g1.setGeometry(500,100,300,100)
        self.btn1 = QPushButton('1号区域')
        self.btn2 = QPushButton('2号区域')
        self.btn3 = QPushButton('3号区域')
        self.btn4 = QPushButton('4号区域')
        self.btn5 = QPushButton('5号区域')
        self.btn6 = QPushButton('6号区域')
        self.btn1.setIcon(QIcon('image/Button2.png'))
        self.btn2.setIcon(QIcon('image/Button2.png'))
        self.btn3.setIcon(QIcon('image/Button2.png'))
        self.btn4.setIcon(QIcon('image/Button2.png'))
        self.btn5.setIcon(QIcon('image/Button2.png'))
        self.btn6.setIcon(QIcon('image/Button2.png'))

        self.btn1.setCheckable(True)
        self.btn2.setCheckable(True)
        self.btn3.setCheckable(True)
        self.btn4.setCheckable(True)
        self.btn5.setCheckable(True)
        self.btn6.setCheckable(True)
        self.btns = [self.btn1,self.btn2,self.btn3,self.btn4,self.btn5,self.btn6]
        self.btn1.clicked.connect(self.open_area1)
        self.btn2.clicked.connect(self.open_area2)
        self.btn3.clicked.connect(self.open_area3)
        self.btn4.clicked.connect(self.open_area4)
        self.btn5.clicked.connect(self.open_area5)
        self.btn6.clicked.connect(self.open_area6)


        lay_btn = QGridLayout()
        lay_btn.addWidget(self.btn1,0,0)
        lay_btn.addWidget(self.btn2, 0, 1)
        lay_btn.addWidget(self.btn3, 0, 2)
        lay_btn.addWidget(self.btn4, 1, 0)
        lay_btn.addWidget(self.btn5, 1, 1)
        lay_btn.addWidget(self.btn6, 1, 2)
        self.btn_group = QGroupBox(self)
        self.btn_group.setLayout(lay_btn)
        self.btn_group.setTitle('区域水阀开关:')
        self.btn_group.setFont(QFont('楷体',15))
        self.btn_group.setGeometry(500,250,400,200)
        self.btn_group.hide()
        self.source_l = QLabel(self)
        self.source_l.setFont(QFont('楷体',15))
        self.source_l.setGeometry(500,200,300,30)
        self.source_l.hide()
        #抽水泵设置
        pump_sup_l = QLabel('抽水泵:')
        self.pump_btn = QPushButton('OFF')
        self.pump_btn.setIcon(QIcon('image/Button2.png'))
        self.pump_btn.setCheckable(True)
        self.pump_btn.clicked.connect(self.set_pump)

        # 相机设置
        camera_l = QLabel('相机：')
        self.camera_btn1 = QPushButton('拍照')
        self.camera_btn1.setIcon(QIcon('image/cameraing.png'))
        self.camera_btn1.clicked.connect(self.do_camera)
        self.camera_btn2 = QPushButton('查看照片')
        self.camera_btn2.setIcon(QIcon('image/camera.png'))
        self.camera_btn2.clicked.connect(self.do_camera_end)
        self.camera_btn2.hide()
        self.camera_btn2.setDisabled(True)

        pump_lay = QGridLayout()
        pump_lay.addWidget(pump_sup_l,0,0)
        pump_lay.addWidget(self.pump_btn,0,1)
        pump_lay.addWidget(camera_l,2,0)
        pump_lay.addWidget(self.camera_btn1,2,1)
        pump_lay.addWidget(self.camera_btn2, 3, 1)
        pump_group = QGroupBox(self)
        pump_group.setLayout(pump_lay)
        pump_group.setFont(QFont('楷体',15))
        pump_group.setGeometry(150,100,300,200)





        btn_exit = QPushButton('退出',self)
        btn_exit.clicked.connect(self.exit_page)
        btn_exit.setFont(QFont('楷体',15))
        btn_exit.setGeometry(500,500,100,30)

        self.show()
#开启抽水泵：
    def set_pump(self):
        print('设置抽水泵')
        if self.pump_btn.isChecked():
            self.pump_btn.setText('ON')
            self.pump_btn.setIcon(QIcon('image/Button1.png'))
            sql = "update command1 set manswitch = 1 where name ='pump_supply'"
            self.cursor.execute(sql)
            self.db.commit()
        else:
            self.pump_btn.setText('OFF')
            self.pump_btn.setIcon(QIcon('image/Button2.png'))
            sql_ = "update command1 set manswitch = 0 where name ='pump_supply'"
            self.cursor.execute(sql_)
            self.db.commit()
#开启排水泵
    def set_pump_out(self):
        print('设置排水泵')
        if self.pump_out_btn.isChecked():
            self.pump_out_btn.setText('ON')
            self.pump_out_btn.setIcon(QIcon('image/Button1.png'))
            sql = "update command1 set manswitch = 1 where name ='pump_out'"
            self.cursor.execute(sql)
            self.db.commit()
        else:
            self.pump_out_btn.setText('OFF')
            self.pump_out_btn.setIcon(QIcon('image/Button2.png'))
            sql_ = "update command1 set manswitch = 0 where name ='pump_out'"
            self.cursor.execute(sql_)
            self.db.commit()
#拍照
    def do_camera(self):
        self.camera_btn1.setDisabled(True)
        print('正在拍照')
        sql = "update command1 set manswitch = 1 where name = 'camera'"
        self.cursor.execute(sql)
        self.db.commit()
        while True:
            sql_ = "select manswitch from command1 where name = 'camera'"
            self.cursor.execute(sql_)
            if_take_pic = self.cursor.fetchall()[0][0]
            print('是否拍照', if_take_pic)
            if if_take_pic == 0:
                # self.camera_btn1.hide()

                self.camera_btn2.setDisabled(False)
                self.camera_btn2.show()
                time.sleep(1)
                break
            time.sleep(3)
        # else:
        #     print('拍照结束')
        #     self.camera_btn.setText('拍照')
        #     self.camera_btn.setIcon(QIcon('image/cameraing.png'))
        #     self.get_pic()
    def do_camera_end(self):
        self.camera_btn1.setDisabled(False)
        self.camera_btn2.setDisabled(True)
        self.camera_btn2.hide()
        # self.camera_btn1.show()
        self.get_pic()






    def get_pic(self):
        sql = "select name from pictures order by id desc limit 1"
        self.cursor.execute(sql)
        pic_name = self.cursor.fetchall()[0][0]
        m = pic_name.index('.')
        pic_ = pic_name.replace(pic_name[m:],'.png')
        print('拍照获得照片：',pic_name)
        self.pic_w = QWidget()
        self.pic_w.setWindowTitle('%s'%(pic_name))
        self.pic_w.setWindowIcon(QIcon('image/camera.png'))
        self.pic_w.setGeometry(200,200,660,500)
        self.pic_w.setFixedSize(self.pic_w.width(), self.pic_w.height())
        p = Image.open('../picture/%s'%(pic_name))
        p.save('pic_change/%s'%(pic_))
        pic = QPixmap('pic_change/%s'%(pic_))
        pic_l = QLabel(self.pic_w)
        pic_l.setPixmap(pic)
        pic_l.move(10,10)
        self.pic_w.show()






#开启区域水阀
    def open_area1(self):

        if self.btn1.isChecked():
            for i in self.btns:
                if i != self.btn1:
                    i.setDisabled(True)
            print('开启1号区域')
            self.btn1.setIcon(QIcon('image/Button1.png'))
            sql_open = "update command1 set manswitch = 1 where name = 's1'"
            self.cursor.execute(sql_open)
            self.db.commit()

        else:
            for i in self.btns:
                if i != self.btn1:
                    i.setDisabled(False)
            print('关闭1号区域')
            self.btn1.setIcon(QIcon('image/Button2.png'))
            sql_close = "update command1 set manswitch = 0 where name = 's1'"
            self.cursor.execute(sql_close)
            self.db.commit()

    def open_area2(self):

        if self.btn2.isChecked():
            for i in self.btns:
                if i != self.btn2:
                    i.setDisabled(True)
            print('开启2号区域')
            self.btn2.setIcon(QIcon('image/Button1.png'))
            sql_open = "update command1 set manswitch = 1 where name = 's2'"
            self.cursor.execute(sql_open)
            self.db.commit()
        else:
            for i in self.btns:
                if i != self.btn2:
                    i.setDisabled(False)
            print('关闭2号区域')
            self.btn2.setIcon(QIcon('image/Button2.png'))
            sql_close = "update command1 set manswitch = 0 where name = 's2'"
            self.cursor.execute(sql_close)
            self.db.commit()
    def open_area3(self):

        if self.btn3.isChecked():
            for i in self.btns:
                if i != self.btn3:
                    i.setDisabled(True)
            print('开启3号区域')
            self.btn3.setIcon(QIcon('image/Button1.png'))
            sql_open = "update command1 set manswitch = 1 where name = 's3'"
            self.cursor.execute(sql_open)
            self.db.commit()
        else:
            for i in self.btns:
                if i != self.btn3:
                    i.setDisabled(False)
            print('关闭3号区域')
            self.btn3.setIcon(QIcon('image/Button2.png'))
            sql_close = "update command1 set manswitch = 0 where name = 's3'"
            self.cursor.execute(sql_close)
            self.db.commit()
    def open_area4(self):

        if self.btn4.isChecked():
            for i in self.btns:
                if i != self.btn4:
                    i.setDisabled(True)
            print('开启4号区域')
            self.btn4.setIcon(QIcon('image/Button1.png'))
            sql_open = "update command1 set manswitch = 1 where name = 's4'"
            self.cursor.execute(sql_open)
            self.db.commit()
        else:
            for i in self.btns:
                if i != self.btn4:
                    i.setDisabled(False)
            print('关闭4号区域')
            self.btn4.setIcon(QIcon('image/Button2.png'))
            sql_close = "update command1 set manswitch = 0 where name = 's4'"
            self.cursor.execute(sql_close)
            self.db.commit()
    def open_area5(self):

        if self.btn5.isChecked():
            for i in self.btns:
                if i != self.btn5:
                    i.setDisabled(True)
            print('开启5号区域')
            self.btn5.setIcon(QIcon('image/Button1.png'))
            sql_open = "update command1 set manswitch = 1 where name = 's5'"
            self.cursor.execute(sql_open)
            self.db.commit()
        else:
            for i in self.btns:
                if i != self.btn5:
                    i.setDisabled(False)
            print('关闭5号区域')
            self.btn5.setIcon(QIcon('image/Button2.png'))
            sql_close = "update command1 set manswitch = 0 where name = 's5'"
            self.cursor.execute(sql_close)
            self.db.commit()
    def open_area6(self):

        if self.btn6.isChecked():
            for i in self.btns:
                if i != self.btn6:
                    i.setDisabled(True)
            print('开启6号区域')
            self.btn6.setIcon(QIcon('image/Button1.png'))
            sql_open = "update command1 set manswitch = 1 where name = 's6'"
            self.cursor.execute(sql_open)
            self.db.commit()
        else:
            for i in self.btns:
                if i != self.btn6:
                    i.setDisabled(False)
            print('关闭6号区域')
            self.btn6.setIcon(QIcon('image/Button2.png'))
            sql_close = "update command1 set manswitch = 0 where name = 's6'"
            self.cursor.execute(sql_close)
            self.db.commit()

    def exit_page(self):
        sql_close_manual = "update command1 set manual = 'N',manswitch = 0"
        self.cursor.execute(sql_close_manual)
        self.db.commit()
        self.close()
    def chose_source(self,text):
        print('选择水源:',text)
        if text == '自来水':
            self.source_l.setText('当前选择水源：<font color = blue>%s</font>'%(text))
            self.source_l.show()
            print('选择自来水')
            sql_chose_tapwater = "update command1 set manual = 'Y',manswitch = 1 where name = 'tapwater'"
            self.cursor.execute(sql_chose_tapwater)
            self.db.commit()
            sql_close_reservoir = "update command1 set manual = 'Y',manswitch = 0 where name = 'reservoir'"
            self.cursor.execute(sql_close_reservoir)
            self.db.commit()

            self.btn_group.show()
        elif text == '蓄水池':
            self.source_l.setText('当前选择水源：<font color = blue>%s</font>' % (text))
            self.source_l.show()
            print('选择蓄水池')
            self.btn_group.show()
            sql_chose_reservoir = "update command1 set manual = 'Y',manswitch = 1 where name = 'reservoir'"
            self.cursor.execute(sql_chose_reservoir)
            self.db.commit()
            sql_close_tapwater = "update command1 set manual = 'Y',manswitch = 0 where name = 'tapwater'"
            self.cursor.execute(sql_close_tapwater)
            self.db.commit()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Manual_window()
    w.initUI()
    sys.exit(app.exec_())