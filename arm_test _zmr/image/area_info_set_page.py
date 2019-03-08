from PyQt5.QtWidgets import QWidget,QApplication,QLabel,QFrame,QPushButton,QComboBox,QGroupBox,QGridLayout,QMessageBox,QDesktopWidget
from PyQt5.QtGui import QIcon,QFont,QColor,QPainter,QPainterPath,QPixmap
from PyQt5.QtCore import pyqtSignal,QTimer,QRect,QRectF,Qt
import pymysql
import sys
import image
class SwitchBtn(QWidget):
    #信号
    checkedChanged = pyqtSignal(bool)
    def __init__(self,parent=None):
        super(QWidget, self).__init__(parent)

        self.checked = False
        self.bgColorOff = QColor(255, 255, 255)
        self.bgColorOn = QColor(0, 0, 0)

        self.sliderColorOff = QColor(100, 100, 100)
        self.sliderColorOn = QColor(100, 184, 255)

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "OFF"
        self.textOn = "ON"

        self.space = 2
        self.rectRadius = 5

        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0

        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.updateValue)  # 计时结束调用operate()方法

        #self.timer.start(5)  # 设置计时间隔并启动

        self.setFont(QFont("Microsoft Yahei", 10))

        # self.resize(55,22)

    def updateValue(self):
        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX  > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()

        self.update()


    def mousePressEvent(self,event):
        self.checked = not self.checked
        #发射信号
        self.checkedChanged.emit(self.checked)

        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 50
        #状态切换改变后自动计算终点坐标
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)

    def paintEvent(self, evt):
        #绘制准备工作, 启用反锯齿
            painter = QPainter()



            painter.begin(self)

            painter.setRenderHint(QPainter.Antialiasing)


            #绘制背景
            self.drawBg(evt, painter)
            #绘制滑块
            self.drawSlider(evt, painter)
            #绘制文字
            self.drawText(evt, painter)

            painter.end()


    def drawText(self, event, painter):
        painter.save()

        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(0, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2, 0,self.width() / 2 - self.space, self.height(), Qt.AlignCenter, self.textOff)

        painter.restore()


    def drawBg(self, event, painter):
        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        #半径为高度的一半
        radius = rect.height() / 2
        #圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()

    def drawSlider(self, event, painter):
        painter.save()

        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.drawEllipse(sliderRect)

        painter.restore()


class Device_set(QWidget):
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def initUI(self,area_id):
        self.resize(1000, 600)
        self.center()
        self.setWindowTitle('%s号区域信息' % (area_id))
        self.setWindowIcon(QIcon('D:/untitled2/4/image/window_icon.png'))
        bg = QPixmap('D:/untitled2/arm_test/image/all_set_bg.png')
        bg_l = QLabel(self)
        bg_l.setPixmap(bg)
        bg_l.setGeometry(0, 0, 1000, 600)
        #连接数据库获取相关信息
        pymysql_ip = '10.0.0.112'
        pymysql_password = 'password'
        self.area_name = 's'+area_id
        self.db = pymysql.connect(pymysql_ip,'root',pymysql_password,'green')
        self.cursor = self.db.cursor()
        #从数据库查询该区域信息
        sql_1 = "select * from interface where name = '%s'"%(self.area_name)
        self.cursor.execute(sql_1)
        area_info = self.cursor.fetchall()[0]
        #从数据库查询该区域运行模式以及电磁阀开关状态
        sql_2 = "select type,switch,manual from command1 where name = '%s'"%(self.area_name)
        self.cursor.execute(sql_2)
        #区域模式及电磁阀信息
        area_mode_switch_info = self.cursor.fetchall()[0]
        # 对应关系
        self.modes = {'A':'定时模式' , 'B': '自动模式'}
        self.switch_stas = {0:'OFF',1:'ON'}
        #模式
        area_mode_info = self.modes[area_mode_switch_info[0]]
        #电磁阀开关状态
        switch_sta = self.switch_stas[area_mode_switch_info[1]]
        #手动模式
        self.manual_info = area_mode_switch_info[2]

        print('%s号区域土壤信息：%s'%(area_id,area_info))
        print('该区域运行模式:%s'%(area_mode_info))
        print('该区域电磁阀开关状态:%s'%(switch_sta))
        print('手动模式状态：',self.manual_info)
        #区域信息显示
        area_group = QGroupBox('%s号区域信息'%(area_id),self)
        area_layout = QGridLayout()

        if area_info[1] == 'normal':#判断该区域传感器是否正常
            if self.manual_info == 'N':#判断是否是手动模式
                soil_moisture_L = QLabel('土壤湿度:')
                moisture_data = QLabel('%s' % (area_info[2]))
                moisture_data.setFrameStyle(QFrame.Panel | QFrame.Sunken)
                area_mode_L = QLabel('当前运行模式:')
                area_mode = QLabel('%s' % (area_mode_info))
                area_mode.setFrameStyle(QFrame.Panel | QFrame.Sunken)
                switch_L = QLabel('电磁阀开关状态:')
                switch_status = QLabel('%s' % (switch_sta))
                switch_status.setFrameStyle(QFrame.Panel | QFrame.Sunken)
                area_layout.addWidget(soil_moisture_L, 0, 0)
                area_layout.addWidget(moisture_data, 0, 1)
                area_layout.addWidget(area_mode_L, 0, 2)
                area_layout.addWidget(area_mode, 0, 3)
                area_layout.addWidget(switch_L, 1, 0)
                area_layout.addWidget(switch_status, 1, 1)
                area_group.setLayout(area_layout)
                area_group.setFont(QFont('楷体', 15))
                area_group.setGeometry(175, 30, 650, 150)
                font = QFont('楷体', 20)
                mode_Label = QLabel('选择模式:', self)
                mode_Label.setFont(font)
                mode_Label.resize(160, 40)
                models = ['', '自动模式', '手动模式', '定时模式']
                mode_select = QComboBox(self)
                mode_select.addItems(models)
                mode_select.setFont(font)
                mode_select.activated[str].connect(self.do_set_mode)
                mode_select_layout = QGridLayout()
                mode_select_layout.addWidget(mode_Label, 0, 0)
                mode_select_layout.addWidget(mode_select, 0, 1)
                mode_select_group = QGroupBox('模式选择', self)
                mode_select_group.setLayout(mode_select_layout)
                mode_select_group.setFont(QFont('楷体', 15))
                mode_select_group.setGeometry(300, 200, 400, 100)
            elif self.manual_info == 'Y':
                soil_moisture_L = QLabel('土壤湿度:')
                moisture_data = QLabel('%s' % (area_info[2]))
                moisture_data.setFrameStyle(QFrame.Panel | QFrame.Sunken)
                area_mode_L = QLabel('当前运行模式:')
                area_mode = QLabel('手动模式')
                area_mode.setFrameStyle(QFrame.Panel | QFrame.Sunken)
                switch_L = QLabel('电磁阀开关状态:')
                switch_status = QLabel('%s' % (switch_sta))
                switch_status.setFrameStyle(QFrame.Panel | QFrame.Sunken)
                area_layout.addWidget(soil_moisture_L, 0, 0)
                area_layout.addWidget(moisture_data, 0, 1)
                area_layout.addWidget(area_mode_L, 0, 2)
                area_layout.addWidget(area_mode, 0, 3)
                area_layout.addWidget(switch_L, 1, 0)
                area_layout.addWidget(switch_status, 1, 1)
                area_group.setLayout(area_layout)
                area_group.setFont(QFont('楷体', 15))
                area_group.setGeometry(175, 30, 650, 150)
                font = QFont('楷体', 20)
                mode_Label = QLabel('选择模式:', self)
                mode_Label.setFont(font)
                mode_Label.resize(160, 40)
                models = ['', '自动模式', '手动模式', '定时模式']
                mode_select = QComboBox(self)
                mode_select.addItems(models)
                mode_select.setFont(font)
                mode_select.activated[str].connect(self.do_set_mode)
                mode_select_layout = QGridLayout()
                mode_select_layout.addWidget(mode_Label, 0, 0)
                mode_select_layout.addWidget(mode_select, 0, 1)
                mode_select_group = QGroupBox('模式选择', self)
                mode_select_group.setLayout(mode_select_layout)
                mode_select_group.setFont(QFont('楷体', 15))
                mode_select_group.setGeometry(300, 200, 400, 100)
        #该区域传感器损坏
        elif area_info[1] == 'broke':
            soil_moisture_L = QLabel('<font color = red>  该区域传感器损坏！</font>')
            soil_moisture_L.setFont(QFont('楷体',35))
            area_layout.addWidget(soil_moisture_L)
            area_group.setLayout(area_layout)
            area_group.setGeometry(175,30,650,150)
        #该区域传感器缺失
        elif area_info[1] == 'lost':
            soil_moisture_L = QLabel('<font color = red>  该区域的传感器缺失！</font>')
            soil_moisture_L.setFont(QFont('楷体', 35))
            area_layout.addWidget(soil_moisture_L)
            area_group.setLayout(area_layout)
            area_group.setGeometry(175, 30, 650, 150)




        # 电磁阀开关控制
        manual_btn = SwitchBtn()
        manual_btn.resize(60, 30)
        if self.manual_info == 'Y':
            manual_btn.checked = True
        manual_btn.checkedChanged.connect(self.manual_action)
        btn_Label = QLabel('电磁阀开关:')
        btn_Label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        btn_Label.setFont(QFont("楷体", 15))
        btn_layout = QGridLayout()
        btn_layout.addWidget(btn_Label, 0, 0)
        btn_layout.addWidget(manual_btn, 0, 1)
        self.btn_group = QGroupBox('电磁阀控制', self)
        self.btn_group.setLayout(btn_layout)
        self.btn_group.setGeometry(350, 350, 300, 80)
        self.btn_group.hide()

        #设定灌溉时间
        time_list = ['00:00:00', '00:30:00','01:00:00', '01:30:00','02:00:00','02:30:00', '03:00:00', '03:30:00',
                     '04:00:00','04:30:00', '05:00:00', '05:30:00','06:00:00', '06:30:00','07:00:00','07:30:00',
                     '08:00:00', '08:30:00','09:00:00','09:30:00', '10:00:00', '10:30:00','11:00:00','11:30:00','12:00:00','12:30:00',
                     '13:00:00', '13:30:00','14:00:00','14:30:00', '15:00:00','15:30:00', '16:00:00','16:30:00',
                     '17:00:00', '17:30:00','18:00:00','18:30:00', '19:00:00','19:30:00', '20:00:00','20:30:00',
                     '21:00:00', '21:30:00', '22:00:00','22:30:00','23:00:00','23:30:00']
        #时间段1
        time_1 = QLabel('时间段1:')
        time_irrigation_start_1 = QLabel('开始时间:')
        time_irrigation_start_1.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        time_irrigation_end_1 = QLabel('结束时间:')
        time_irrigation_end_1.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.start_time_1 = '00:00:00'
        self.end_time_1 = '00:00:00'
        #下拉框插入元素
        self.time_select_start_1 = QComboBox()
        self.time_select_start_1.addItems(time_list)
        self.time_select_start_1.activated[str].connect(self.time_start_1)
        self.time_select_end_1 = QComboBox()
        self.time_select_end_1.addItems(time_list)
        self.time_select_end_1.activated[str].connect(self.time_end_1)
        #时间段2
        time_2 = QLabel('时间段2:')
        time_irrigation_start_2 = QLabel('开始时间:')
        time_irrigation_start_2.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        time_irrigation_end_2 = QLabel('结束时间:')
        time_irrigation_end_2.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.start_time_2 = '00:00:00'
        self.end_time_2 = '00:00:00'
        self.time_select_start_2 = QComboBox()
        self.time_select_start_2.addItems(time_list)
        self.time_select_start_2.activated[str].connect(self.time_start_2)
        self.time_select_end_2 = QComboBox()
        self.time_select_end_2.addItems(time_list)
        self.time_select_end_2.activated[str].connect(self.time_end_2)
        #按钮
        #定时模式下按钮组
        self.btn_1 = QPushButton('确定')
        self.btn_1.clicked.connect(self.update_the_irrigation_time)
        self.btn_2 = QPushButton('取消')
        self.btn_2.clicked.connect(self.cancel_the_irrigation_time)
        self.btn_1.hide()
        self.btn_2.hide()
        #自动模式下按钮组
        self.btn_3 = QPushButton('确定')
        self.btn_3.clicked.connect(self.update_the_automatic_time)
        self.btn_4= QPushButton('取消')
        self.btn_4.clicked.connect(self.cancel_the_automatic_time)
        self.btn_3.hide()
        self.btn_4.hide()


        time_layout = QGridLayout()
        time_layout.addWidget(time_1,0,0)
        time_layout.addWidget(time_irrigation_start_1, 1, 0)
        time_layout.addWidget(self.time_select_start_1, 1, 1)
        time_layout.addWidget(time_irrigation_end_1, 1, 2)
        time_layout.addWidget(self.time_select_end_1, 1, 3)
        time_layout.addWidget(time_2,2,0)
        time_layout.addWidget(time_irrigation_start_2, 3, 0)
        time_layout.addWidget(self.time_select_start_2, 3, 1)
        time_layout.addWidget(time_irrigation_end_2, 3, 2)
        time_layout.addWidget(self.time_select_end_2, 3, 3)
        time_layout.addWidget(self.btn_1,4,1)
        time_layout.addWidget(self.btn_2,4,2)
        time_layout.addWidget(self.btn_3, 4, 1)
        time_layout.addWidget(self.btn_4, 4, 2)


        self.time_group = QGroupBox('设定灌溉时间',self)
        self.time_group.setLayout(time_layout)
        self.time_group.setFont(QFont('楷体',15))
        self.time_group.setGeometry(150,300,700,250)
        self.time_group.hide()







        self.show()
    def manual_action(self, checked):
        if checked == True:
            sql_ = "update command1 set manual = '%s',manswitch = '%s'where name = '%s'" \
                   % ('Y',1, self.area_name)
            self.cursor.execute(sql_)
            self.db.commit()
            print('打开电磁阀')

        else:
            sql_ = "update command1 set manual = '%s',manswitch = '%s'where name = '%s'" \
                   % ('N',0, self.area_name)
            self.cursor.execute(sql_)
            self.db.commit()
            print('关闭电磁阀')


    def do_set_mode(self,text):
        if text =='自动模式':
            print('自动模式')
            self.btn_group.hide()
            self.time_group.show()
            self.btn_1.hide()
            self.btn_2.hide()
            self.btn_3.show()
            self.btn_4.show()

        elif text == '手动模式':
            print('手动模式')
            self.time_group.hide()
            self.btn_group.show()
        else:
            print('定时模式')
            # 灌溉时间设置
            self.btn_group.hide()
            self.time_group.show()
            self.btn_3.hide()
            self.btn_4.hide()
            self.btn_1.show()
            self.btn_2.show()

    def time_start_1(self,text):
        self.start_time_1 = text
    def time_end_1(self,text):
        self.end_time_1 = text

    def time_start_2(self,text):
        self.start_time_2 = text
    def time_end_2(self,text):
        self.end_time_2 = text

    # 灌溉时间设置
    def update_the_irrigation_time(self):
        print('定时模式时间设定')
        print('时间段1：%s - %s'%(self.start_time_1,self.end_time_1))
        print('时间段2：%s - %s' % (self.start_time_2, self.end_time_2))
        if self.start_time_1 > self.end_time_1:
            print('开始时间不能比结束时间晚，请重新选择时间段1的初始时间！')
            button = QMessageBox.warning(self, "时间选择错误", "开始时间不能比结束时间晚，请重新选择时间段1的开始时间！",
                                         QMessageBox.Ok, QMessageBox.Ok)
            if button == QMessageBox.Ok:
                return
            else:
                return
        elif self.start_time_2 > self.end_time_2:
            print('开始时间不能比结束时间晚，请重新选择时间段2的初始时间！')
            button = QMessageBox.warning(self, "时间选择错误", "开始时间不能比结束时间晚，请重新选择时间段2的开始时间！",
                                         QMessageBox.Ok, QMessageBox.Ok)
            if button == QMessageBox.Ok:
                return
            else:
                return
        elif self.start_time_2 < self.end_time_1:
            print('两时间段不能重合')
            button = QMessageBox.warning(self, "时间选择错误", "两时间段不能重合！",
                                         QMessageBox.Ok, QMessageBox.Ok)
            if button == QMessageBox.Ok:
                return
            else:
                return
        else:
            print('确定灌溉时间段1：%s - %s' % (self.start_time_1, self.end_time_1))
            print('确定灌溉时间段2：%s - %s' % (self.start_time_2, self.end_time_2))
            sql_ = "update command1 set manual = '%s',type = '%s',timing11 = '%s',timing12 = '%s',timing21='%s',timing22='%s',switch = '%s' where name = '%s'"\
                   %('N','A',self.start_time_1,self.end_time_1,self.start_time_2,self.end_time_2,0,self.area_name)
            self.cursor.execute(sql_)
            self.db.commit()
            button = QMessageBox.information(self, "时间设定成功", "定时模式灌溉时间设定成功！",QMessageBox.Ok,QMessageBox.Ok)
            if button == QMessageBox.Ok:
                return
            else:
                return

    def cancel_the_irrigation_time(self):
        print('取消设定灌溉时间')
        self.time_group.hide()

    # 自动模式灌溉时间设定
    def update_the_automatic_time(self):
        print('自动模式时间设定')
        print('时间段1：%s - %s' % (self.start_time_1, self.end_time_1))
        print('时间段2：%s - %s' % (self.start_time_2, self.end_time_2))
        if self.start_time_1 > self.end_time_1:
            print('开始时间不能比结束时间晚，请重新选择时间段1的初始时间！')
            button = QMessageBox.warning(self, "时间选择错误", "开始时间不能比结束时间晚，请重新选择时间段1的开始时间！",
                                         QMessageBox.Ok, QMessageBox.Ok)
            if button == QMessageBox.Ok:
                return
            else:
                return
        elif self.start_time_2 > self.end_time_2:
            print('开始时间不能比结束时间晚，请重新选择时间段2的初始时间！')
            button = QMessageBox.warning(self, "时间选择错误", "开始时间不能比结束时间晚，请重新选择时间段2的开始时间！",
                                         QMessageBox.Ok, QMessageBox.Ok)
            if button == QMessageBox.Ok:
                return
            else:
                return
        elif self.start_time_2 < self.end_time_1:
            print('两时间段不能重合')
            button = QMessageBox.warning(self, "时间选择错误", "两时间段不能重合！",
                                         QMessageBox.Ok, QMessageBox.Ok)
            if button == QMessageBox.Ok:
                return
            else:
                return
        else:
            print('确定灌溉时间段1：%s - %s' % (self.start_time_1, self.end_time_1))
            print('确定灌溉时间段2：%s - %s' % (self.start_time_2, self.end_time_2))
            sql_ = "update command1 set manual = '%s',type = '%s',zdtime11 = '%s',zdtime12 = '%s',zdtime21='%s',zdtime22='%s',switch = '%s'where name = '%s'" \
                   % ('N', 'B', self.start_time_1, self.end_time_1, self.start_time_2, self.end_time_2, 0,self.area_name)
            self.cursor.execute(sql_)
            self.db.commit()
            button = QMessageBox.information(self, "时间设定成功", "自动模式灌溉时间设定成功！", QMessageBox.Ok, QMessageBox.Ok)
            if button == QMessageBox.Ok:
                return
            else:
                return


    def cancel_the_automatic_time(self):
        print('取消设定自动模式时间')
        self.time_group.hide()













if __name__ == '__main__':
    app = QApplication(sys.argv)
    the_window = Device_set()
    the_window.initUI('3')
    sys.exit(app.exec_())