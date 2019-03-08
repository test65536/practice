from PyQt5.QtWidgets import QMainWindow,QWidget,QAction,QLabel,QLineEdit,QPushButton,QApplication,QGroupBox,QGridLayout,QMessageBox,QCheckBox,QDesktopWidget,QComboBox,QFrame
from PyQt5.QtGui import QIcon,QFont,QPixmap,QColor,QPainter,QPainterPath
from PyQt5.QtCore import QDateTime,QTimer,Qt,pyqtSignal,QRect,QRectF
from PyQt5.Qt import QRegExp,QRegExpValidator
from PIL import Image
import pymysql
import sys
import time
import threading as td
from area_info_set_page import Device_set
from all_set_page import All_device_set
from pic_time_line import window
from manual_page import Manual_window


class Home_window(QMainWindow):
    # def __init__(self):
    #     super().__init__()
    #     self.initUI()

    def initUI(self,user_level):
        self.if_break = True
        pymysql_ip = '10.0.0.111'
        pymysql_password = 'password'
        self.db = pymysql.connect(pymysql_ip,'root',pymysql_password,'green')
        self.cursor = self.db.cursor()

        self.user_level = user_level
        if user_level == '1':
            user_menu_state = False
        else:
            user_menu_state = True
        self.screen_w = int(QApplication.desktop().width())
        self.screen_h = int(QApplication.desktop().height()*0.94)
        self.resize(self.screen_w,self.screen_h)
        self.setFixedSize(self.width(), self.height())#设置窗口不可放大和拉伸
        self.move(0,0)
        self.setWindowTitle('屋顶绿化系统')
        self.setWindowIcon(QIcon('image/window_icon.png'))
        self.statusBar().showMessage('准备就绪')
        #界面纯白背景设置
        image = QPixmap('image/bg_image_white.jpg')
        self.bg_image = QLabel(self)
        self.bg_image.setPixmap(image)
        self.bg_image.setGeometry(0, 65, self.screen_w, self.screen_h-100)

        #设计菜单：*******************************************************
        #设置

        set_action = QAction(QIcon('image/set.png'),'设置',self)
        set_action.setShortcut('Ctrl+S')
        set_action.setStatusTip('设置')
        set_action.triggered.connect(self.Setting)
        #退出
        esc_action = QAction(QIcon('image/exit.png'),'退出',self)
        esc_action.setShortcut('Ctrl+Q')
        esc_action.setStatusTip('退出')
        esc_action.triggered.connect(self.Esc)
        #用户管理
        add_user = QAction(QIcon('image/add.png'),'添加用户',self)
        add_user.setShortcut('Ctrl+A')
        add_user.setStatusTip('添加用户')
        add_user.triggered.connect(self.add_U)

        delete_user = QAction(QIcon('image/delete.png'),'删除用户',self)
        delete_user.setStatusTip('删除用户')
        delete_user.setShortcut('Ctrl+D')
        delete_user.triggered.connect(self.delete_U)

        phone_manager = QAction(QIcon('image/phone.png'), '绑定手机号', self)
        phone_manager.setStatusTip('绑定手机号')
        phone_manager.setShortcut('Ctrl+N')
        phone_manager.triggered.connect(self.set_phone)

        #修改密码：
        password_manager = QAction(QIcon('image/manager.png'),'修改密码',self)
        password_manager.setStatusTip('修改密码')
        password_manager.setShortcut('Ctrl+P')
        password_manager.triggered.connect(self.password_set)



        #帮助
        help_action = QAction(QIcon(),'帮助',self)
        help_action.setShortcut('Ctrl+H')
        help_action.setStatusTip('帮助')
        help_action.triggered.connect(self.Help_menu)

        menu_bar = self.menuBar()
        set_menu = menu_bar.addMenu('菜单')
        set_menu.addAction(set_action)
        set_menu.addAction(esc_action)

        user_menu = menu_bar.addMenu('用户管理')
        user_menu.addAction(add_user)
        user_menu.addAction(delete_user)
        user_menu.addAction(phone_manager)
        user_menu.setDisabled(user_menu_state)


        password_menu = menu_bar.addMenu('密码管理')
        password_menu.addAction(password_manager)

        help_menu = menu_bar.addMenu('帮助')
        help_menu.addAction(help_action)

        #*******************************************************************

        #设计工具栏*********************************************************
        #一键设置
        device_set = QAction(QIcon('image/all_set.png'),'一键设置',self)
        device_set.triggered.connect(self.All_device_set)
        tool_bar_1 = self.addToolBar('一键设置')
        tool_bar_1.addAction(device_set)
        #阈值设置
        data_set = QAction(QIcon('image/mrp.png'), '参数阈值设置', self)
        data_set.triggered.connect(self.All_value_set)
        tool_bar_0 = self.addToolBar('参数设置')
        tool_bar_0.addAction(data_set)

        #灭菌灯控制
        light_set = QAction(QIcon('image/light.png'), '灭菌灯设置', self)
        light_set.triggered.connect(self.light_set)
        tool_bar_3 = self.addToolBar('灭菌灯设置')
        tool_bar_3.addAction(light_set)

        #手动控制按钮
        manual_set = QAction(QIcon('image/hand.png'), '手动模式', self)
        manual_set.triggered.connect(self.manual_set)
        tool_bar_4 = self.addToolBar('手动模式')
        tool_bar_4.addAction(manual_set)


        #退出按钮
        exit_set = QAction(QIcon('image/exit.png'), '退出', self)
        exit_set.triggered.connect(self.Esc)
        tool_bar_5 = self.addToolBar('退出')
        tool_bar_5.addAction(exit_set)

        #刷新
        # do_refresh = QAction(QIcon('D:/untitled2/4/image/refresh.png'), '刷新', self)
        # do_refresh.triggered.connect(self.do_refresh)
        # tool_bar_2 = self.addToolBar('刷新')
        # tool_bar_2.addAction(do_refresh)

        # *******************************************************************

# 桌面显示设计**************************************************************
        #全局变量显示设计

        sql_getinfo  = "select avg from interface limit 8,15"
        self.cursor.execute(sql_getinfo)
        getinfo = self.cursor.fetchall()
        print('光照强度(0)，降雨量(1)，大气温度(2)，大气湿度(3)，风速(4)，风向(5)，上水位(6)，下水位(7)\n',(getinfo))

            #时间显示：
        self.font = QFont()
        self.font.setFamily('楷体')
        self.label_color = 'black'

        # time_layout = QGridLayout()
        # self.time_Label = QLabel(self)
        # self.time_Label.resize(200,20)
        # self.time_Label.setFont(self.font)
        # time_layout.addWidget(self.time_Label)
        # self.time_group = QGroupBox(self)
        # self.time_group.setGeometry(int(self.screen_w*(5/6)), 10, int(self.screen_w*(3/20)), 55)
        # # self.time_group.resize(225,55)
        # self.time_group.setLayout(time_layout)
        # timer = QTimer(self)
        # timer.timeout.connect(self.show_time)
        # timer.start()
            # 光照强度

        the_global_info_layout = QGridLayout()
        sun_image = QPixmap('image/sun.png')
        self.sun_l = QLabel(self)
        self.sun_l.setPixmap(sun_image)
        self.sun_l.resize(80,80)#光照强度图标显示
        # self.sun_l.setGeometry(20,80,80,80)
        self.sun_int = '10'
        self.sun_g = 'blue'
        #光照强度数值显示
        self.sun_data = QLabel('<font color = %s>光照强度:</font><font color= %s>%s</font>' % (self.label_color,self.sun_g, self.sun_int), self)
        self.sun_data.setFont(self.font)
        # self.sun_data.move(10,160)
            #降雨量
        rain_image = QPixmap('image/rain.png')
        self.rain_l = QLabel(self)
        self.rain_l.setPixmap(rain_image)
        self.rain_l.resize(80,80)
        # self.rain_l.setGeometry(140, 80, 80, 80)
        self.rain_int = '10'
        self.rain_g = 'blue'
        self.rain_data = QLabel('<font color = %s>降雨量:</font><font color= %s>%smL</font>' % (self.label_color,self.rain_g, self.rain_int), self)
        self.rain_data.setFont(self.font)
        # self.rain_data.move(140, 160)
            #温度
        tim_image = QPixmap('image/tim.png')
        self.tim_l = QLabel(self)
        self.tim_l.setPixmap(tim_image)
        self.tim_l.resize(80,80)
        # self.tim_l.setGeometry(260, 80, 80, 80)
        self.tim_int = '10'
        self.tim_g = 'blue'
        self.tim_data = QLabel('<font color = %s>大气温度</font><font color= %s>%s℃</font>' % (self.label_color,self.tim_g, self.tim_int), self)
        self.tim_data.setFont(self.font)
        # self.tim_data.move(260, 160)
            #大气湿度
        wet_image = QPixmap('image/wet.png')
        self.wet_l = QLabel(self)
        self.wet_l.setPixmap(wet_image)
        self.wet_l.resize(80, 80)
        # self.tim_l.setGeometry(260, 80, 80, 80)
        self.wet_int = '10'
        self.wet_g = 'blue'
        self.wet_data = QLabel(
            '<font color = %s>大气湿度</font><font color= %s>%s℃</font>' % (self.label_color, self.wet_g, self.wet_int))
        self.wet_data.setFont(self.font)


            #风速
        speed_image = QPixmap('image/wind_speed.png')
        self.speed_l = QLabel(self)
        self.speed_l.setPixmap(speed_image)
        self.speed_l.resize(80,80)
        # self.speed_l.setGeometry(380, 80, 80, 80)
        self.speed_int = '10'
        self.speed_g = 'blue'
        self.speed_data = QLabel('<font color = %s>风速:</font><font color= %s>%s</font>' % (self.label_color,self.speed_g, self.speed_int), self)
        self.speed_data.setFont(self.font)
        # self.speed_data.move(380, 160)
            #风向
        direction_image = QPixmap('image/wind_direction.png')
        self.direction_l = QLabel(self)
        self.direction_l.setPixmap(direction_image)
        self.direction_l.resize(80,80)
        # self.direction_l.setGeometry(500, 80, 80, 80)
        self.direction_int = '东南'
        self.direction_g = 'blue'
        self.direction_data = QLabel('<font color = %s>风向:</font><font color= %s>%s</font>' % (self.label_color,self.direction_g, self.direction_int), self)
        self.direction_data.setFont(self.font)
        # self.direction_data.move(500, 160)
            #下方水位
        w_level_image = QPixmap('image/water.png')
        self.d_water_level = QLabel(self)
        self.d_water_level.setPixmap(w_level_image)
        self.d_water_level.resize(80,80)
        # self.d_water_level.setGeometry(20,200,80,80)
        self.d_water_int = '50'
        self.d_water_g = 'blue'
        self.d_water_data = QLabel('<font color = %s>下方水位:</font><font color= %s>%sL</font>' % (self.label_color,self.d_water_g, self.d_water_int), self)
        self.d_water_data.setFont(self.font)
        # self.d_water_data.move(20,280)
            #上方水位
        self.u_water_level = QLabel(self)
        self.u_water_level.setPixmap(w_level_image)
        self.u_water_level.resize(80,80)
        # self.u_water_level.setGeometry(140, 200, 80, 80)
        self.u_water_int = '40'
        self.u_water_g = 'red'
        self.u_water_data = QLabel('<font color = %s>上方水位:</font><font color= %s>%sL</font>' % (self.label_color,self.u_water_g, self.u_water_int), self)
        self.u_water_data.setFont(self.font)
        # self.u_water_data.move(130, 280)
            #水泵开关状态
        pump_image = QPixmap('image/pump.png')
        self.pump_l = QLabel(self)
        self.pump_l.setPixmap(pump_image)
        self.pump_l.resize(80,80)
        # self.pump_l.setGeometry(260,200,80,80)
        self.pump_int = 'OFF'
        self.pump_g = 'red'
        self.pump_data = QLabel(
            '<font color = %s>排水水泵:</font><font color= %s>%s</font>' % (self.label_color, self.pump_g, self.pump_int),
            self)
        self.pump_data.setFont(self.font)
        #供水水泵
        self.pump_l_sup = QLabel(self)
        self.pump_l_sup.setPixmap(pump_image)
        self.pump_l_sup.resize(80, 80)
        # self.pump_l.setGeometry(260,200,80,80)
        self.pump_sup_int = 'OFF'
        self.pump_sup_g = 'red'
        self.pump_sup_data = QLabel(
            '<font color = %s>供水水泵:</font><font color= %s>%s</font>' % (self.label_color, self.pump_sup_g, self.pump_sup_int),
            self)
        self.pump_sup_data.setFont(self.font)

        # self.pump_data.move(250, 280)
            #灭菌灯开关状态
        light_image = QPixmap('image/light.png')
        self.light_l = QLabel(self)
        self.light_l.setPixmap(light_image)
        self.light_l.resize(80,80)
        # self.light_l.setGeometry(380, 200, 80, 80)
        self.light_int = 'OFF'
        self.light_g = 'red'
        self.light_data = QLabel(
            '<font color = %s>灭菌灯状态:</font><font color= %s>%s</font>' % (self.label_color, self.light_g, self.light_int),
            self)
        self.light_data.setFont(self.font)
        #自来水流量
        flow_image = QPixmap('image/flow.png')
        self.flow_l = QLabel(self)
        self.flow_l.setPixmap(flow_image)
        self.flow_l.resize(80, 80)
        # self.light_l.setGeometry(380, 200, 80, 80)
        self.flow_int = '0'
        self.flow_g = 'red'
        self.flow_data = QLabel(
            '<font color = %s>蓄水池流量:</font><font color= %s>%s</font>' % (
            self.label_color, self.flow_g, self.flow_int),
            self)
        self.flow_data.setFont(self.font)
        #自来水流速
        flow_speed_image = QPixmap('image/flow_speed.png')
        self.flow_speed_l = QLabel(self)
        self.flow_speed_l.setPixmap(flow_speed_image)
        self.flow_speed_l.resize(80, 80)
        self.flow_speed_int = '0'
        self.flow_speed_g = 'red'
        self.flow_speed_data = QLabel(
            '<font color = %s>蓄水池流速:</font><font color= %s>%s m³/h</font>' % (
                self.label_color, self.flow_speed_g, self.flow_speed_int),
            self)
        self.flow_speed_data.setFont(self.font)

        # 蓄水池流量
        flow_image = QPixmap('image/flow.png')
        self.flow_l_x = QLabel(self)
        self.flow_l_x.setPixmap(flow_image)
        self.flow_l_x.resize(80, 80)
        # self.light_l.setGeometry(380, 200, 80, 80)
        self.flow_int_x = '0'
        self.flow_g_x = 'red'
        self.flow_data_x = QLabel(
            '<font color = %s>自来水流量:</font><font color= %s>%s</font>' % (
                self.label_color, self.flow_g_x, self.flow_int_x),
            self)
        self.flow_data_x.setFont(self.font)
        # 蓄水池流速
        flow_speed_image = QPixmap('image/flow_speed.png')
        self.flow_speed_l_x = QLabel(self)
        self.flow_speed_l_x.setPixmap(flow_speed_image)
        self.flow_speed_l_x.resize(80, 80)
        self.flow_speed_int_x = '0'
        self.flow_speed_g_x = 'red'
        self.flow_speed_data_x = QLabel(
            '<font color = %s>自来水流速:</font><font color= %s>%s m³/h</font>' % (
                self.label_color, self.flow_speed_g_x, self.flow_speed_int_x),
            self)
        self.flow_speed_data_x.setFont(self.font)


        water_source_image = QPixmap('image/water_source.png')
        self.water_source_l = QLabel(self)
        self.water_source_l.setPixmap(water_source_image)
        self.water_source_l.resize(80, 80)
        self.water_source_int = '自来水'
        self.water_source_g = 'red'
        self.water_source_data = QLabel(
            '<font color = %s>水源:</font><font color= %s>%s</font>' % (
                self.label_color, self.water_source_g, self.water_source_int),
            self)
        self.water_source_data.setFont(self.font)


        # self.light_data.move(370, 280)
        the_global_info_layout.addWidget(self.sun_l,0,0)
        the_global_info_layout.addWidget(self.sun_data, 1, 0)
        the_global_info_layout.addWidget(self.rain_l, 0, 1)
        the_global_info_layout.addWidget(self.rain_data, 1, 1)
        the_global_info_layout.addWidget(self.tim_l, 0, 2)
        the_global_info_layout.addWidget(self.tim_data, 1, 2)
        the_global_info_layout.addWidget(self.wet_l, 2, 0)
        the_global_info_layout.addWidget(self.wet_data, 3, 0)
        the_global_info_layout.addWidget(self.speed_l, 2, 1)
        the_global_info_layout.addWidget(self.speed_data, 3, 1)
        the_global_info_layout.addWidget(self.direction_l, 2, 2)
        the_global_info_layout.addWidget(self.direction_data,3, 2)
        the_global_info_layout.addWidget(self.d_water_level, 4, 0)
        the_global_info_layout.addWidget(self.d_water_data, 5, 0)
        the_global_info_layout.addWidget(self.u_water_level, 4, 1)
        the_global_info_layout.addWidget(self.u_water_data, 5, 1)
        the_global_info_layout.addWidget(self.pump_l, 4, 2)
        the_global_info_layout.addWidget(self.pump_data, 5, 2)
        the_global_info_layout.addWidget(self.light_l,2,3)
        the_global_info_layout.addWidget(self.light_data,3,3)
        the_global_info_layout.addWidget(self.flow_l,6,0)
        the_global_info_layout.addWidget(self.flow_data,7,0)
        the_global_info_layout.addWidget(self.pump_l_sup,4,3)
        the_global_info_layout.addWidget(self.pump_sup_data,5,3)
        the_global_info_layout.addWidget(self.flow_speed_l,6,1)
        the_global_info_layout.addWidget(self.flow_speed_data,7,1)
        the_global_info_layout.addWidget(self.flow_l_x,6,2)
        the_global_info_layout.addWidget(self.flow_data_x,7,2)
        the_global_info_layout.addWidget(self.flow_speed_l_x,6,3)
        the_global_info_layout.addWidget(self.flow_speed_data_x,7,3)
        the_global_info_layout.addWidget(self.water_source_l,0,3)
        the_global_info_layout.addWidget(self.water_source_data,1,3)
        #全局信息显示组：光照强度，风速，风向等
        self.the_global_info_group = QGroupBox(self)
        # self.the_global_info_group.setGeometry(20, 80, 900, 240)
        self.the_global_info_group.resize(int(self.screen_w*0.6),int(self.screen_h*0.3))
        self.the_global_info_group.setLayout(the_global_info_layout)
        self.the_global_info_group.setFont(QFont('楷体',12))


            #现场照片显示设计
        sql_pic = "select name from pictures order by id desc limit 1"
        self.cursor.execute(sql_pic)
        pic = self.cursor.fetchall()[0][0]
        img = Image.open('D:/PycharmProjects/untitled/picture/%s'%(pic))

        pic_ = pic.replace(pic[pic.index('.'):],'.png')
        img.save('pic_change/%s' % (pic_))



        site_image = QPixmap('pic_change/%s'%(pic_))
        self.site_image_l = QLabel()
        self.site_image_l.resize(500,327)
        self.site_image_l.setPixmap(site_image)
        site_image_btn = QPushButton('查看详情')
        site_image_btn.setFont(self.font)
        site_image_btn.clicked.connect(self.look_the_pic)
        site_image_layout = QGridLayout()
        site_image_layout.addWidget(site_image_btn,1,0)
        site_image_layout.addWidget(self.site_image_l,0,0)

        self.site_image_group = QGroupBox('现场最新时刻照片',self)
        # self.site_image_group.setGeometry(1000, 80, 400, 327)
        self.site_image_group.resize(int(self.screen_w*0.25),int(self.screen_h*0.45))
        self.site_image_group.setLayout(site_image_layout)
        self.site_image_group.setFont(QFont('楷体',12))
        t_n = pic.index('.')
        print('索引', t_n)
        pic_data = pic[:t_n]
        year_ = pic_data[:4]
        month_ = pic_data[4:6]
        day_ = pic_data[6:8]
        h_ = pic_data[9:11]
        m_ = pic_data[11:13]
        s_ = pic_data[13:]
        data_ = year_ + '年' + month_ + '月' + day_ + '日' + h_ + ':' + m_ + ':' + s_
        self.pic_data = QLabel('<font color = red>%s</font>' % (data_), self)




            #8块区域信息显示
        self.area_info = {}
        sql = "select manual,type,switch from command1 where name between 's1' and 's6'"
        self.cursor.execute(sql)
        area_info = self.cursor.fetchall()
        sql_ = "select state,avg from interface where name between 's1' and 's6'"
        self.cursor.execute(sql_)
        sensor_info = self.cursor.fetchall()
        print('区域手动模式状态,运行模式,电磁阀开关:',(area_info))
        print('电磁阀状态，土壤湿度',sensor_info)
        area_sensor_info = []
        for i in range(6):
            a = list(sensor_info[i])
            b = list(area_info[i])
            a.extend(b)
            area_sensor_info.append(a)
        print('整体信息：电磁阀状态(0)，土壤湿度(1)，区域手动模式(2)，运行模式(3)，电磁阀开关(4)',area_sensor_info)
        n = 0
        diancifa = {0:['OFF','blue'],1:['ON','red']}
        modes = {'B':['自动','blue'],'A':['定时','green']}

        for j in area_sensor_info:
            if j[0] == 'normal':
                if j[2] == 'Y':
                    if (j[1] >= 50):
                        self.area_info[n] = [j[1],'blue' ,diancifa[j[4]][0],diancifa[j[4]][1] ,'手动','red']
                    elif (j[1]<50):
                        self.area_info[n] = [j[1],'red',diancifa[j[4]][0],diancifa[j[4]][1],'手动','red']
                else:
                    if (j[1] >= 50):
                        self.area_info[n] = [j[1],'blue' ,diancifa[j[4]][0],diancifa[j[4]][1] ,modes[j[3]][0],modes[j[3]][1]]
                    elif (j[1]<50):
                        self.area_info[n] = [j[1],'red',diancifa[j[4]][0],diancifa[j[4]][1],modes[j[3]][0],modes[j[3]][1]]
            elif j[0] == 'broke':
                self.area_info[n] = ['NULL','red','NULL','red','NULL','red']
            else:
                self.area_info[n] = ['NULL','red','NULL','red','NULL','red']
            n+=1

        groups = [self.area_information_1,self.area_information_2,
                  self.area_information_3,self.area_information_4,
                  self.area_information_5,self.area_information_6
                  ]
        zuobiao = [[0,0],[0,1],[0,2],
                   [1,0],[1,1],[1,2]]
        self.main_area_group = QGroupBox(self)
        main_area_layout = QGridLayout()
        for i in range(len(self.area_info)):
            main_area_layout.addWidget(groups[i]('%s号区域'%(i+1),self.area_info[i][0],self.area_info[i][1],self.area_info[i][2],self.area_info[i][3],self.area_info[i][4],self.area_info[i][5]),zuobiao[i][0],zuobiao[i][1])
        self.main_area_group.setLayout(main_area_layout)
        # self.main_area_group.setGeometry(20,450,1460,250)
        self.main_area_group.resize(int(self.screen_w*0.97),int(self.screen_h*0.3))
        # *******************************************************************

        # 开启线程定时更新照片：
        thread_get_pic = td.Thread(target=self.get_the_new_pic)
        thread_get_pic.start()

        # 开启线程1用于全局信息实时更新

        the_get_info_thread = td.Thread(target=self.get_global_info)
        the_get_info_thread.start()

        #定时更新区域信息
        thread_get_area = td.Thread(target=self.get_area_info)
        thread_get_area.start()
        #布局显示
        self.Buju()

        self.show()
    def manual_set(self):
        print('手动模式')
        self.manual_window = Manual_window()
        self.manual_window.initUI()











    #区域信息显示

    def area_information_1(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):
        self.group_1 = QGroupBox(name)
        self.group_1.resize(300,100)
        layout = QGridLayout()
        #土壤湿度

        self.soil_moisture_L_1 = QLabel('<font>土壤湿度：</font><font color = %s>%s</font><font color = blue> %s</font>'%(soil_color,soil_moisture,'%RH'))
        self.soil_moisture_L_1.setFont(self.font)
        #电磁阀开关状态

        self.switch_status_L_1 = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        self.switch_status_L_1.setFont(self.font)
        #当前运行模式

        self.current_mode_L_1 = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        self.current_mode_L_1.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon('image/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_1)
        #把以上组件放入网格布局中
        layout.addWidget(self.soil_moisture_L_1,1,0)
        layout.addWidget(self.current_mode_L_1,1,1)
        layout.addWidget(self.switch_status_L_1,2,0)
        layout.addWidget(a_button,2,1)
        self.group_1.setLayout(layout)
        self.group_1.setFont(QFont('楷体', 15))
        return self.group_1


    def area_information_2(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):
        self.group_2 = QGroupBox(name)
        self.group_2.resize(300,100)
        layout = QGridLayout()
        #土壤湿度

        self.soil_moisture_L_2 = QLabel('<font>土壤湿度：</font><font color = %s>%s</font>'%(soil_color,soil_moisture))
        self.soil_moisture_L_2.setFont(self.font)
        #电磁阀开关状态

        self.switch_status_L_2 = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        self.switch_status_L_2.setFont(self.font)
        #当前运行模式

        self.current_mode_L_2 = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        self.current_mode_L_2.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon('image/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_2)
        #把以上组件放入网格布局中
        layout.addWidget(self.soil_moisture_L_2,1,0)
        layout.addWidget(self.current_mode_L_2,1,1)
        layout.addWidget(self.switch_status_L_2,2,0)
        layout.addWidget(a_button,2,1)
        self.group_2.setLayout(layout)
        self.group_2.setFont(QFont('楷体',15))
        return self.group_2

    def area_information_3(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):

        layout = QGridLayout()
        #土壤湿度

        self.soil_moisture_L_3 = QLabel('<font>土壤湿度：</font><font color = %s>%s</font>'%(soil_color,soil_moisture))
        self.soil_moisture_L_3.setFont(self.font)
        #电磁阀开关状态

        self.switch_status_L_3 = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        self.switch_status_L_3.setFont(self.font)
        #当前运行模式

        self.current_mode_L_3 = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        self.current_mode_L_3.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon('image/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_3)
        #把以上组件放入网格布局中
        layout.addWidget(self.soil_moisture_L_3,1,0)
        layout.addWidget(self.current_mode_L_3,1,1)
        layout.addWidget(self.switch_status_L_3,2,0)
        layout.addWidget(a_button,2,1)
        self.group_3 = QGroupBox(name)
        self.group_3.resize(300, 100)
        self.group_3.setLayout(layout)
        self.group_3.setFont(QFont('楷体', 15))
        return self.group_3

    def area_information_4(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):
        self.group_4 = QGroupBox(name)
        self.group_4.resize(300,100)
        layout = QGridLayout()
        #土壤湿度

        self.soil_moisture_L_4 = QLabel('<font>土壤湿度：</font><font color = %s>%s</font>'%(soil_color,soil_moisture))
        self.soil_moisture_L_4.setFont(self.font)
        #电磁阀开关状态

        self.switch_status_L_4 = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        self.switch_status_L_4.setFont(self.font)
        #当前运行模式

        self.current_mode_L_4 = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        self.current_mode_L_4.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon('image/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_4)
        #把以上组件放入网格布局中
        layout.addWidget(self.soil_moisture_L_4,1,0)
        layout.addWidget(self.current_mode_L_4,1,1)
        layout.addWidget(self.switch_status_L_4,2,0)
        layout.addWidget(a_button,2,1)
        self.group_4.setLayout(layout)
        self.group_4.setFont(QFont('楷体', 15))
        return self.group_4

    def area_information_5(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):
        layout = QGridLayout()
        #土壤湿度

        self.soil_moisture_L_5 = QLabel('<font>土壤湿度：</font><font color = %s>%s</font>'%(soil_color,soil_moisture))
        self.soil_moisture_L_5.setFont(self.font)
        #电磁阀开关状态

        self.switch_status_L_5 = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        self.switch_status_L_5.setFont(self.font)
        #当前运行模式

        self.current_mode_L_5 = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        self.current_mode_L_5.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon('image/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_5)
        #把以上组件放入网格布局中
        layout.addWidget(self.soil_moisture_L_5,1,0)
        layout.addWidget(self.current_mode_L_5,1,1)
        layout.addWidget(self.switch_status_L_5,2,0)
        layout.addWidget(a_button,2,1)
        self.group_5 = QGroupBox(name)
        self.group_5.resize(300, 100)
        self.group_5.setLayout(layout)
        self.group_5.setFont(QFont('楷体', 15))
        return self.group_5

    def area_information_6(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):
        layout = QGridLayout()
        #土壤湿度

        self.soil_moisture_L_6 = QLabel('<font>土壤湿度：</font><font color = %s>%s</font>'%(soil_color,soil_moisture))
        self.soil_moisture_L_6.setFont(self.font)
        #电磁阀开关状态

        self.switch_status_L_6 = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        self.switch_status_L_6.setFont(self.font)
        #当前运行模式

        self.current_mode_L_6 = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        self.current_mode_L_6.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon('image/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_6)
        #把以上组件放入网格布局中
        layout.addWidget(self.soil_moisture_L_6,1,0)
        layout.addWidget(self.current_mode_L_6,1,1)
        layout.addWidget(self.switch_status_L_6,2,0)
        layout.addWidget(a_button,2,1)
        self.group_6 = QGroupBox(name)
        self.group_6.resize(300, 100)
        self.group_6.setLayout(layout)
        self.group_6.setFont(QFont('楷体', 15))
        return self.group_6




        # 定时获取信息并更新
    def get_global_info(self):

        data_1 = [['大气温度:', '℃'], ['大气湿度:', '%'], ['降雨量:', 'mm/min'], ['风速:', 'm/s'], ['风向:', '°'],
                  ['光照强度:', 'Lux'], ['上方水位:', 'm'], ['下方水位:', 'm'], ['蓄水池流量:', 'm³'], ['蓄水池流速:', 'm³/h'],
                  ['自来水流量:', 'm³'], ['自来水流速:', 'm³/h']]
        data_l_1 = [self.tim_data, self.wet_data, self.rain_data, self.speed_data, self.direction_data,
                    self.sun_data, self.u_water_data, self.d_water_data, self.flow_data, self.flow_speed_data,
                    self.flow_data_x, self.flow_speed_data_x]
        data_2 = [['供水水泵:', self.pump_sup_data], ['排水水泵:', self.pump_data], ['灭菌灯:', self.light_data]]
        db = pymysql.connect('10.0.0.111', 'root', 'password', 'green')
        db.autocommit(True)  # 实时更新数据库连接
        cursor = db.cursor()
        while self.if_break:
            print('****************定时获取全局信息*******************************')
            sql_get_global = "select state,avg from interface limit 6,12"
            cursor.execute(sql_get_global)
            the_info = cursor.fetchall()
            print('当前信息******************')
            print(the_info)
            print('******')
            for i in range(12):
                if the_info[i][0] == 'lost':
                    data_l_1[i].setText(
                        '<font color = black>%s</font><font color = %s>%s</font>' % (data_1[i][0], 'red', '缺失'))
                elif the_info[i][0] == 'broke':
                    data_l_1[i].setText(
                        '<font color = black>%s</font><font color = %s>%s</font>' % (data_1[i][0], 'red', '损坏'))
                else:

                    data_l_1[i].setText('<font color = black>%s</font><font color = %s>%s %s</font>' % (
                    data_1[i][0], 'blue', the_info[i][1], data_1[i][1]))

            sql_get_com = "select switch1 from command1 limit 8,3"
            cursor.execute(sql_get_com)
            the_info_2 = cursor.fetchall()
            print(the_info_2)
            for j in range(3):
                if the_info_2[j][0] == 1:
                    data_2[j][1].setText(
                        '<font color = black>%s</font><font color = %s>%s</font>' % (data_2[j][0], 'red', 'ON'))
                elif the_info_2[j][0] == 0:
                    data_2[j][1].setText(
                        '<font color = black>%s</font><font color = %s>%s</font>' % (data_2[j][0], 'blue', 'OFF'))

            sql_water_source = "select switch1 from command1 limit 6,2"
            cursor.execute(sql_water_source)
            the_info_3 = cursor.fetchall()
            print('***')
            print(the_info_3)
            if (the_info_3[0][0] == 1) & (the_info_3[1][0] == 0):
                self.water_source_data.setText('<font color = black>水源:</font><font color = blue>蓄水池</font>')
            elif (the_info_3[0][0] == 0) & (the_info_3[1][0] == 1):
                self.water_source_data.setText('<font color = black>水源:</font><font color = green>自来水</font>')
            else:
                self.water_source_data.setText('<font color = black>水源:</font><font color = red>无</font>')
            print('2秒后刷新******************')
            print('****************定时获取全局信息*******************************')
            time.sleep(2)

    # 定时更新照片
    def get_the_new_pic(self):
        db = pymysql.connect('10.0.0.111', 'root', 'password', 'green')
        db.autocommit(True)  # 实时更新数据库连接
        cursor = db.cursor()
        while self.if_break:
            print('更新照片*********************************')
            sql = "select name from pictures order by id desc limit 1"
            cursor.execute(sql)
            pic = cursor.fetchall()[0][0]
            pic_ = pic.replace(pic[pic.index('.'):], '.png')
            pic_img = Image.open('D:/PycharmProjects/untitled/picture/%s' % (pic))
            pic_img.save('pic_change/%s' % (pic_))
            img = QPixmap('pic_change/%s' % (pic_))

            self.site_image_l.setPixmap(img)
            self.site_image_group.setTitle('照片：%s' % (pic_))
            t_n = pic.index('.')
            print('索引', t_n)
            pic_data = pic[:t_n]
            year_ = pic_data[:4]
            month_ = pic_data[4:6]
            day_ = pic_data[6:8]
            h_ = pic_data[9:11]
            m_ = pic_data[11:13]
            s_ = pic_data[13:]
            data_ = year_ + '年' + month_ + '月' + day_ + '日' + h_ + ':' + m_ + ':' + s_
            self.pic_data.setText('<font color = red>%s</font>' % (data_))
            print('**************')
            print('照片名字:', pic_)
            print('更新照片******************************')
            time.sleep(2)


    #定时获得区域信息
    def get_area_info(self):

        area_show_l = [[self.soil_moisture_L_1, self.switch_status_L_1, self.current_mode_L_1],
                       [self.soil_moisture_L_2, self.switch_status_L_2, self.current_mode_L_2],
                       [self.soil_moisture_L_3, self.switch_status_L_3, self.current_mode_L_3],
                       [self.soil_moisture_L_4, self.switch_status_L_4, self.current_mode_L_4],
                       [self.soil_moisture_L_5, self.switch_status_L_5, self.current_mode_L_5],
                       [self.soil_moisture_L_6, self.switch_status_L_6, self.current_mode_L_6]
                       ]

        db = pymysql.connect('10.0.0.111', 'root', 'password', 'green')
        db.autocommit(True)#实时更新数据库连接
        cursor = db.cursor()
        while self.if_break:
            print('*****************定时获取各区域信息，并更新***************************************')
            sql_state_avg = "select state,avg from interface where name between 's1' and 's6'"#获取传感器状态，土壤湿度
            cursor.execute(sql_state_avg)
            info_1 = cursor.fetchall()
            print('传感器状态,湿度值\n',info_1)
            sql_area_info = "select type,manual,switch1,manswitch from command1 where name between 's1' and 's6'"
            cursor.execute(sql_area_info)
            info_2 = cursor.fetchall()
            print('各地区运行模式，水阀开关',info_2)
            switchs = {1:['red','ON'],0:['blue','OFF']}
            unit = '%RH'
            for i in range(6):
                if (info_1[i][0] == 'lost')or (info_1[i][0] == 'broke'):
                    area_show_l[i][0].setText('土壤湿度:<font color = red>异常</font>')

                    if info_2[i][1] == 'Y':
                        area_show_l[i][2].setText('运行模式:<font color = red>手动</font>')
                        area_show_l[i][1].setText(
                            '水阀开关:<font color = %s>%s</font>' % (switchs[info_2[i][3]][0], switchs[info_2[i][3]][1]))
                    else:
                        area_show_l[i][1].setText(
                            '水阀开关:<font color = %s>%s</font>' % (switchs[info_2[i][2]][0], switchs[info_2[i][2]][1]))
                        if info_2[i][0] == 'A':
                            area_show_l[i][2].setText('运行模式:<font color = green>定时</font>')
                        else:
                            area_show_l[i][2].setText('运行模式:<font color = blue>自动</font>')
                else:
                    area_show_l[i][0].setText('土壤湿度:<font color = blue>%s</font> %s'%(info_1[i][1],unit))

                    if info_2[i][1] == 'Y':
                        area_show_l[i][2].setText('运行模式:<font color = red>手动</font>')
                        area_show_l[i][1].setText(
                            '水阀开关:<font color = %s>%s</font>' % (switchs[info_2[i][3]][0], switchs[info_2[i][3]][1]))
                    else:
                        area_show_l[i][1].setText(
                            '水阀开关:<font color = %s>%s</font>' % (switchs[info_2[i][2]][0], switchs[info_2[i][2]][1]))
                        if info_2[i][0] == 'A':
                            area_show_l[i][2].setText('运行模式:<font color = green>定时</font>')
                        else:
                            area_show_l[i][2].setText('运行模式:<font color = blue>自动</font>')
            print('*****************定时获取各区域信息，并更新***************************************')


            time.sleep(2)


# 桌面显示设计**************************************************************



    # 窗口整体布局函数
    def Buju(self):
        self.the_global_info_group.setGeometry(int(self.screen_w*0.01), int(self.screen_h*0.08), int(self.screen_w*0.4), int(self.screen_h*0.55))
        self.main_area_group.setGeometry(int(self.screen_w*0.0133),int(self.screen_h*0.63),int(self.screen_w*0.97),int(self.screen_h*0.32))

        self.site_image_group.setGeometry(int(self.screen_w*(2/3)), int(self.screen_h*0.13), int(self.screen_w*(4/15)), int(self.screen_h*0.45))
        self.pic_data.setGeometry(int(self.screen_w * (2 / 3)) + 20,
                                  int(self.screen_h * 0.13) + int(self.screen_h * 0.45) - 80, 200, 30)
    #绑定手机号
    def set_phone(self):
        print('绑定手机号')
        self.set_phone_window = Set_phone_number()
        self.set_phone_window.initUI()





    #设置全局参数阈值
    def All_value_set(self):
        print('设置全局参数阈值')
        self.All_set_win = Set_All_V()
        self.All_set_win.initUI()

    # 设置灭菌灯
    def light_set(self):
        print('灭菌灯设置')
        self.light_window = Set_light()
        self.light_window.initUI()

    # def show_time(self):
    #     date_time = QDateTime.currentDateTime()
    #     text=date_time.toString()
    #     self.time_Label.setText('<font color=blue>%s</font>'%(text))
    def look_the_pic(self):
        print('查看历史照片')
        self.pic_window = window()
        self.pic_window.initUi()


    def Setting(self):
        print('点击设置')
    def Esc(self):
        self.if_break = False
        self.close()
    def Help_menu(self):
        print('帮助')
    def All_device_set(self):
        print('一键设置')
        self.device_set = All_device_set()
        self.device_set.initUI()
    def add_U(self):
        print('添加用户')
        self.add_windwo = Add_user()
        self.add_windwo.iniUI()

    def delete_U(self):
        print('删除用户')
        self.delete_window = Delete_user()
        self.delete_window.iniUI()

    def password_set(self):
        print('密码修改')
        self.password_set_window = Password_set()
        self.password_set_window.iniUI()

    #单个区域设置参数
    def set_alone_1(self):
        print('设置当前土地')
        area_id = '1'
        self.the_area_window_1 = Device_set()
        self.the_area_window_1.initUI(area_id)
    def set_alone_2(self):
        print('设置当前土地')
        area_id = '2'
        self.the_area_window_2 = Device_set()
        self.the_area_window_2.initUI(area_id)
    def set_alone_3(self):
        print('设置当前土地')
        area_id = '3'
        self.the_area_window_3 = Device_set()
        self.the_area_window_3.initUI(area_id)
    def set_alone_4(self):
        print('设置当前土地')
        area_id = '4'
        self.the_area_window_4 = Device_set()
        self.the_area_window_4.initUI(area_id)
    def set_alone_5(self):
        print('设置当前土地')
        area_id = '5'
        self.the_area_window_5 = Device_set()
        self.the_area_window_5.initUI(area_id)
    def set_alone_6(self):
        print('设置当前土地')
        area_id = '6'
        self.the_area_window_6 = Device_set()
        self.the_area_window_6.initUI(area_id)
    # def set_alone_7(self):
    #     print('设置当前土地')
    #     area_id = '7'
    #     self.the_area_window_7 = Device_set()
    #     self.the_area_window_7.initUI(area_id)
    # def set_alone_8(self):
    #     print('设置当前土地')
    #     area_id = '8'
    #     self.the_area_window_8 = Device_set()
    #     self.the_area_window_8.initUI(area_id)
    #刷新页面
    def do_refresh(self):
        self.close()
        self.home_page = Home_window()
        self.home_page.initUI(1)
        print('刷新页面成功')
    #居中显示
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


#按钮绘制
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
#设置灭菌灯
class Set_light(QWidget):
    def initUI(self):
        self.if_break = True
        pymysqlip = '10.0.0.111'
        pymysql_pswd = 'password'
        self.db = pymysql.connect(pymysqlip,'root',pymysql_pswd,'green')
        self.cursor = self.db.cursor()
        sql_s = "select manual,switch1,manswitch from command1 where name = 'uv_light'"
        self.cursor.execute(sql_s)
        l = self.cursor.fetchall()[0]
        s = {0:['blue','OFF'],1:['red','ON']}
        self.resize(1000,600)
        self.setFixedSize(self.width(), self.height())  # 设置窗口不可放大和拉伸
        self.center()
        self.setWindowIcon(QIcon('image/light.png'))
        self.setWindowTitle('灭菌灯设置')
        bg = QPixmap('image/all_set_bg.png')
        bg_L = QLabel(self)
        bg_L.setPixmap(bg)
        bg_L.setGeometry(0,0,1000,600)

        light_state = QLabel('灭菌灯状态:')
        mode_state = QLabel('运行模式:')
        if l[0] == 'Y':
            self.light_s = QLabel('<font color = %s>%s</font>' % (s[l[2]][0], s[l[2]][1]))
            self.mode_s = QLabel('<font color = %s>%s</font>' % ('red', '手动'))
        else:
            self.light_s = QLabel('<font color = %s>%s</font>' % (s[l[1]][0], s[l[1]][1]))
            self.mode_s = QLabel('<font color = %s>%s</font>' % ('blue', '定时'))
        self.light_s.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.mode_s.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        refresh_uv_light_state = td.Thread(target=self.refresh_uv_light)
        refresh_uv_light_state.start()


        light_L = QLabel('模式选择:')
        models = ['选择','手动模式', '定时模式']
        mode_select = QComboBox()
        mode_select.addItems(models)
        mode_select.activated[str].connect(self.do_select)
        mode_lay = QGridLayout()
        mode_lay.addWidget(light_state,0,0)
        mode_lay.addWidget(self.light_s,0,1)
        mode_lay.addWidget(mode_state,1,0)
        mode_lay.addWidget(self.mode_s,1,1)
        mode_lay.addWidget(light_L,1,2)
        mode_lay.addWidget(mode_select,1,3)
        mode_group = QGroupBox(self)
        mode_group.setLayout(mode_lay)
        mode_group.setFont(QFont('楷体',18))
        mode_group.setGeometry(225,20,550,120)
        #设置手动模式开关
        sql = "select manual,switch1,manswitch from command1 where name = 'uv_light'"
        self.cursor.execute(sql)
        manual_info = self.cursor.fetchall()[0]
        print(manual_info)
        light_switch = QLabel('灭菌灯开关')
        btn = SwitchBtn(self)
        btn.resize(60, 30)
        if manual_info[0] == 'Y':
            if manual_info[2] == 1:
                btn.checked = True
        else:
            if manual_info[1] == 1:
                btn.checked = True

        btn.checkedChanged.connect(self.manual_action)
        light_lay = QGridLayout()
        light_lay.addWidget(light_switch,0,0)
        light_lay.addWidget(btn,0,1)
        self.light_group = QGroupBox(self)
        self.light_group.setLayout(light_lay)
        self.light_group.setFont(QFont('楷体',18))
        self.light_group.setGeometry(350,300,300,60)
        self.light_group.hide()
        #设置定时时间
        sql_look_data = "select zdtime11 from command1 where name = 'uv_light'"
        self.cursor.execute(sql_look_data)
        try:
            self.chosed_data = self.cursor.fetchall()[0][0].split(',')
        except:
            self.chosed_data = []
        self.set_data = []
        print('已选日期：',self.chosed_data)
        cycle_l = QLabel('开灯日期：')
        self.cycle_box = QCheckBox('全选')
        self.cycle_box_1 = QCheckBox('周一')
        self.cycle_box_2 = QCheckBox('周二')
        self.cycle_box_3 = QCheckBox('周三')
        self.cycle_box_4 = QCheckBox('周四')
        self.cycle_box_5 = QCheckBox('周五')
        self.cycle_box_6 = QCheckBox('周六')
        self.cycle_box_7 = QCheckBox('周日')
        self.cycle_boxs = [self.cycle_box,self.cycle_box_1,self.cycle_box_2,self.cycle_box_3,self.cycle_box_4,self.cycle_box_5,self.cycle_box_6,self.cycle_box_7]
        set_data_choices = [self.set_data_choice_0,self.set_data_choice_1,self.set_data_choice_2,self.set_data_choice_3,self.set_data_choice_4,self.set_data_choice_5,self.set_data_choice_6,self.set_data_choice_7]
        cycle_lay = QGridLayout()
        for i in range(8):
            cycle_lay.addWidget(self.cycle_boxs[i],0,i)
            self.cycle_boxs[i].stateChanged.connect(set_data_choices[i])
        for j in self.chosed_data:
            n = int(j) + 1
            self.cycle_boxs[n].setChecked(True)
        self.cycle_group = QGroupBox('选择日期',self)
        self.cycle_group.setLayout(cycle_lay)
        self.cycle_group.setFont(QFont('楷体',12))
        self.cycle_group.setGeometry(200,150,600,100)
        self.cycle_group.hide()

        time_list = ['00:00:00', '00:30:00', '01:00:00', '01:30:00', '02:00:00', '02:30:00', '03:00:00', '03:30:00',
                     '04:00:00', '04:30:00', '05:00:00', '05:30:00', '06:00:00', '06:30:00', '07:00:00', '07:30:00',
                     '08:00:00', '08:30:00', '09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00',
                     '12:00:00', '12:30:00',
                     '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00', '16:00:00', '16:30:00',
                     '17:00:00', '17:30:00', '18:00:00', '18:30:00', '19:00:00', '19:30:00', '20:00:00', '20:30:00',
                     '21:00:00', '21:30:00', '22:00:00', '22:30:00', '23:00:00', '23:30:00']

        time_1 = QLabel('时间段1:')
        time_irrigation_start_1 = QLabel('开始时间:')
        time_irrigation_start_1.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        time_irrigation_end_1 = QLabel('结束时间:')
        time_irrigation_end_1.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.start_time_1 = '00:00:00'
        self.end_time_1 = '00:00:00'
        # 下拉框插入元素
        self.time_select_start_1 = QComboBox()
        self.time_select_start_1.addItems(time_list)
        self.time_select_start_1.activated[str].connect(self.time_start_1)
        self.time_select_end_1 = QComboBox()
        self.time_select_end_1.addItems(time_list)
        self.time_select_end_1.activated[str].connect(self.time_end_1)
        # 时间段2
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
        self.btn_1 = QPushButton('确定')
        self.btn_1.clicked.connect(self.update_the_irrigation_time)
        self.btn_2 = QPushButton('取消')
        self.btn_2.clicked.connect(self.cancel_the_irrigation_time)

        #布局
        time_layout = QGridLayout()
        time_layout.addWidget(time_1, 1, 0)
        time_layout.addWidget(time_irrigation_start_1, 2, 0)
        time_layout.addWidget(self.time_select_start_1, 2, 1)
        time_layout.addWidget(time_irrigation_end_1, 2, 2)
        time_layout.addWidget(self.time_select_end_1, 2, 3)
        time_layout.addWidget(time_2, 3, 0)
        time_layout.addWidget(time_irrigation_start_2, 4, 0)
        time_layout.addWidget(self.time_select_start_2, 4, 1)
        time_layout.addWidget(time_irrigation_end_2, 4, 2)
        time_layout.addWidget(self.time_select_end_2, 4, 3)
        time_layout.addWidget(self.btn_1, 5, 1)
        time_layout.addWidget(self.btn_2, 5, 2)

        self.time_group = QGroupBox('设定时间',self)
        self.time_group.setLayout(time_layout)
        self.time_group.setFont(QFont('楷体',15))
        self.time_group.setGeometry(200,250,600,250)
        self.time_group.hide()
        btn_exit = QPushButton('退出',self)
        btn_exit.setGeometry(400,530,200,30)
        btn_exit.setFont(QFont('楷体',15))
        btn_exit.clicked.connect(self.exit_page)
        sql_look_time = "select timing11,timing12,timing21,timing22 from command1 where name = 'uv_light'"
        self.cursor.execute(sql_look_time)
        the_time = self.cursor.fetchall()[0]
        self.start_time_1 = the_time[0]
        self.end_time_1 = the_time[1]
        self.start_time_2 = the_time[2]
        self.end_time_2 = the_time[3]
        self.time_select_start_1.setCurrentText(the_time[0])
        self.time_select_end_1.setCurrentText(the_time[1])
        self.time_select_start_2.setCurrentText(the_time[2])
        self.time_select_end_2.setCurrentText(the_time[3])
        self.show()

    #选择日期
    def set_data_choice_0(self,state):

        if state == Qt.Checked:
            print('全选')
            for i in self.cycle_boxs:
                i.setChecked(True)
        else:
            print('全取消')
            for i in self.cycle_boxs:
                i.setChecked(False)
        print(self.set_data)

    def set_data_choice_1(self,state):

        if state == Qt.Checked:
            self.set_data.append('0')
            print('选择周一')
        else:
            self.set_data.remove('0')
            print('取消周一')
    def set_data_choice_2(self,state):

        if state == Qt.Checked:
            self.set_data.append('1')
            print('选择周二')
        else:
            self.set_data.remove('1')
            print('取消周二')
    def set_data_choice_3(self,state):

        if state == Qt.Checked:
            self.set_data.append('2')
            print('选择周三')
        else:
            self.set_data.remove('2')
            print('取消周三')
    def set_data_choice_4(self,state):

        if state == Qt.Checked:
            self.set_data.append('3')
            print('选择周四')
        else:
            self.set_data.remove('3')
            print('取消周四')
    def set_data_choice_5(self,state):

        if state == Qt.Checked:
            self.set_data.append('4')
            print('选择周五')
        else:
            self.set_data.remove('4')
            print('取消周五')
    def set_data_choice_6(self,state):

        if state == Qt.Checked:
            self.set_data.append('5')
            print('选择周六')
        else:
            self.set_data.remove('5')
            print('取消周六')
    def set_data_choice_7(self,state):

        if state == Qt.Checked:
            self.set_data.append('6')
            print('选择周日')
        else:
            self.set_data.remove('6')
            print('取消周日')
    def exit_page(self):
        self.if_break = False
        self.close()
    def refresh_uv_light(self):
        print('开始更新灭菌灯状态')
        db = pymysql.connect('10.0.0.111','root','password','green')
        db.autocommit(True)  # 实时更新数据库连接
        cursor = db.cursor()
        s = {0: ['blue', 'OFF'], 1: ['red', 'ON']}
        while self.if_break:
            sql = "select manual,switch1,manswitch from command1 where name = 'uv_light'"
            cursor.execute(sql)
            uv_data = cursor.fetchall()[0]
            print('灭菌灯状态：')
            print(uv_data)

            if uv_data[0] == 'Y':
                self.light_s.setText('<font color = %s>%s</font>'%(s[uv_data[2]][0],s[uv_data[2]][1]))
                self.mode_s.setText('<font color = %s>%s</font>' % ('red', '手动'))
            else:
                self.light_s.setText('<font color = %s>%s</font>' % (s[uv_data[1]][0], s[uv_data[1]][1]))
                self.mode_s.setText('<font color = %s>%s</font>' % ('blue', '定时'))


            time.sleep(2)

    def manual_action(self,checked):
        if checked == True:
            sql_ = "update command1 set manual = '%s',manswitch = '%s' where name = 'uv_light'" % ('Y', 1)
            self.cursor.execute(sql_)
            self.db.commit()
            print('打开灭菌灯')
        else:
            sql_ = "update command1 set manual = '%s',manswitch = '%s' where name = 'uv_light'" % ('Y', 0)
            self.cursor.execute(sql_)
            self.db.commit()
            print('关闭灭菌灯')

    def time_start_1(self,text):
        self.start_time_1 = text
    def time_end_1(self,text):
        self.end_time_1 = text
    def time_start_2(self,text):
        self.start_time_2 = text
    def time_end_2(self,text):
        self.end_time_2 = text
    def update_the_irrigation_time(self):
        print('定时模式时间设定')
        print('时间段1：%s - %s' % (self.start_time_1, self.end_time_1))
        print('时间段2：%s - %s' % (self.start_time_2, self.end_time_2))
        msg = ''
        if len(self.set_data) == 0:
            button = QMessageBox.warning(self, "未选择日期", "请先选择日期！",
                                         QMessageBox.Ok, QMessageBox.Ok)
            if button == QMessageBox.Ok:
                return
            else:
                return
        else:
            for i in self.set_data:
                if (self.set_data.index(i) != (len(self.set_data)-1)):
                    msg += i + ','
                else:
                    msg += i

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
            print('确定开灯时间段1：%s - %s' % (self.start_time_1, self.end_time_1))
            print('确定开灯时间段2：%s - %s' % (self.start_time_2, self.end_time_2))
            sql_ = "update command1 set manual = '%s',type = '%s',timing11 = '%s',timing12 = '%s',timing21='%s',timing22='%s',manswitch = '%s',zdtime11 = '%s' where name = 'uv_light'" \
                   % ('N', 'A', self.start_time_1, self.end_time_1, self.start_time_2, self.end_time_2, 0,msg)
            self.cursor.execute(sql_)
            self.db.commit()
            button = QMessageBox.information(self, "时间设定成功", "灭菌灯开关时间设定成功！", QMessageBox.Ok, QMessageBox.Ok)
            if button == QMessageBox.Ok:
                return
            else:
                return
    def cancel_the_irrigation_time(self):
        print('取消设定时间')
        self.cycle_group.hide()
        self.time_group.hide()

    def do_select(self,text):
        if text == '手动模式':
            print('手动模式')
            self.cycle_group.hide()
            self.time_group.hide()
            self.light_group.show()
        else:
            print('定时模式')

            self.light_group.hide()
            self.cycle_group.show()
            self.time_group.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
#绑定手机号
class Set_phone_number(QMainWindow):#绑定手机号
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def initUI(self):
        self.db_1 = pymysql.connect('10.0.0.111','root','password','green')
        self.cursor_1 = self.db_1.cursor()
        self.db_2 = pymysql.connect('10.0.0.33', 'root', 'zong123', 'green_roof')
        self.cursor_2 = self.db_2.cursor()
        self.resize(600,400)
        self.setFixedSize(self.width(), self.height())  # 设置窗口不可放大和拉伸
        self.center()
        self.setWindowIcon(QIcon('image/phone.png'))
        self.setWindowTitle('绑定手机号')
        bg = QPixmap('image/all_set_bg.png')
        bg_l = QLabel(self)
        bg_l.setPixmap(bg)
        bg_l.setGeometry(0, 0, 600, 400)
        user_L = QLabel('用户名：')
        self.user_E = QLineEdit()
        pswd_L = QLabel('密码')
        self.pswd_E = QLineEdit()
        self.pswd_E.setEchoMode(QLineEdit.Password)
        phone_L = QLabel('手机号:')
        self.phone_E = QLineEdit()
        layout = QGridLayout()
        layout.addWidget(user_L,0,0)
        layout.addWidget(self.user_E, 0, 1)
        layout.addWidget(pswd_L, 1, 0)
        layout.addWidget(self.pswd_E, 1, 1)
        layout.addWidget(phone_L, 2, 0)
        layout.addWidget(self.phone_E, 2, 1)
        group = QGroupBox(self)
        group.setLayout(layout)
        group.setFont(QFont('楷体',12))
        group.setGeometry(150,50,300,200)
        btn1 = QPushButton('确定')
        btn2 = QPushButton('取消')
        btn1.clicked.connect(self.confirm_set)
        btn2.clicked.connect(self.cancel_set)
        layout2 = QGridLayout()
        layout2.addWidget(btn1,0,0)
        layout2.addWidget(btn2,0,1)
        group2  = QGroupBox(self)
        group2.setLayout(layout2)
        group2.setFont(QFont('楷体',12))
        group2.setGeometry(225,300,150,50)

        self.show()
    def confirm_set(self):
        print('确定绑定')
        sql_1 = "select name,password from user_list"
        self.cursor_1.execute(sql_1)
        user_info = self.cursor_1.fetchall()
        flag = 0
        for i in user_info:
            if (self.user_E.text() == i[0])&(self.pswd_E.text() == i[1]):
                print('可以绑定')
                sql_2 = "insert into forget_password (name,password,phone_number) values('%s','%s','%s')"%(self.user_E.text(),self.pswd_E.text(),self.phone_E.text())
                self.cursor_2.execute(sql_2)
                self.db_2.commit()
                flag = 1
                btn = QMessageBox.information(self, "绑定成功", "手机号绑定成功！",
                                          QMessageBox.Ok, QMessageBox.Ok)
                if btn == QMessageBox.Ok:
                    self.close()
                    return
                else:
                    self.close()
                    return
        if flag == 0:
            print('用户名护或者密码错误！')
            btn = QMessageBox.warning(self, "信息错误", "用户名护或者密码错误！",
                                      QMessageBox.Ok, QMessageBox.Ok)
            if btn == QMessageBox.Ok:
                return
            else:
                return
    def cancel_set(self):
        print('取消绑定')
        self.close()
#修改密码
class Password_set(QMainWindow):
    def iniUI(self):
        pymysql_ip = '10.0.0.111'
        pymysql_password = 'password'
        self.db = pymysql.connect(pymysql_ip,'root',pymysql_password,'green')
        self.cursor = self.db.cursor()
        self.setWindowTitle('密码管理')
        self.setWindowIcon(QIcon('image/password.png'))
        self.resize(600,400)
        self.setFixedSize(self.width(), self.height())  # 设置窗口不可放大和拉伸
        self.center()
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        bg = QPixmap('image/all_set_bg.png')
        bg_l = QLabel(self)
        bg_l.setPixmap(bg)
        bg_l.setGeometry(0, 0, 600, 400)
        self.user_L = QLabel('输入用户名：',self)
        self.user_E = QLineEdit(self)
        self.password_L =QLabel('输入原密码：',self)
        self.password_E =QLineEdit(self)
        self.password_E.setEchoMode(QLineEdit.Password)
        self.user_L.setGeometry(150,100,80,30)
        self.user_E.setGeometry(240,100,150,30)
        self.password_L.setGeometry(150,150,80,30)
        self.password_E.setGeometry(240,150,150,30)
        self.n_password_L = QLabel('请输入新密码：', self)
        self.n_password_L.hide()
        self.n_password_E = QLineEdit(self)
        self.n_password_E.setEchoMode(QLineEdit.Password)
        self.n_password_E.hide()
        self.r_n_password_L = QLabel('请确认新密码：', self)
        self.r_n_password_L.hide()
        self.r_n_password_E = QLineEdit(self)
        self.r_n_password_E.setEchoMode(QLineEdit.Password)
        self.r_n_password_E.hide()
        self.n_password_L.setGeometry(150, 100, 100, 30)
        self.n_password_E.setGeometry(260, 100, 150, 30)
        self.r_n_password_L.setGeometry(150, 150, 100, 30)
        self.r_n_password_E.setGeometry(260, 150, 150, 30)
        self.ptn_1 = QPushButton('确认',self)
        self.ptn_2 = QPushButton('取消',self)
        self.ptn_1.move(150,300)
        self.ptn_2.move(350,300)
        self.ptn_1.clicked.connect(self.confirm_change)
        self.ptn_2.clicked.connect(self.cancel_change)
        self.ptn_3 = QPushButton('确认', self)
        self.ptn_4 = QPushButton('取消', self)
        self.ptn_3.move(150, 300)
        self.ptn_4.move(350, 300)
        self.ptn_3.clicked.connect(self.confirm_set)
        self.ptn_4.clicked.connect(self.cancel_set)
        self.ptn_3.hide()
        self.ptn_4.hide()

        self.show()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def confirm_set(self):
        print('确认修改')
        print('用户名：',self.user_E.text())
        if self.n_password_E.text() == self.r_n_password_E.text():
            sql = "update user_list set password = '%s'  where name = '%s'" % (
            self.n_password_E.text(), self.user_E.text())
            self.cursor.execute(sql)
            self.db.commit()
            btn = QMessageBox.information(self, "修改成功", "修改密码成功！",
                                      QMessageBox.Ok, QMessageBox.Ok)
            if btn == QMessageBox.Ok:
                self.close()
                return
            else:
                self.close()
                return
        else:
            btn = QMessageBox.warning(self, "密码错误", "两次密码输入不同！",
                                      QMessageBox.Ok, QMessageBox.Ok)
            if btn == QMessageBox.Ok:
                return
            else:
                return



    def cancel_set(self):
        print('取消修改')
        self.close()


    def confirm_change(self):
        sql = "select * from user_list"
        self.cursor.execute(sql)
        user_info = self.cursor.fetchall()
        flag = 0
        for i in user_info:
            if (self.user_E.text() == i[0])&(self.password_E.text()==i[1]):
                flag = 1
                print('可以修改')
                self.user_L.close()
                self.user_E.close()
                self.password_L.close()
                self.password_E.close()
                self.ptn_1.hide()
                self.ptn_2.hide()
                self.n_password_L.show()
                self.n_password_E.show()
                self.r_n_password_L.show()
                self.r_n_password_E.show()
                self.ptn_3.show()
                self.ptn_4.show()


        if flag == 0:
            print('用户名或者密码错误！')
            btn = QMessageBox.warning(self, "密码错误", "用户名或者密码错误！",
                                      QMessageBox.Ok, QMessageBox.Ok)
            if btn == QMessageBox.Ok:
                return
            else:
                return
    def cancel_change(self):
        self.destroy()
#增加用户
class Add_user(QMainWindow):

    def iniUI(self):
        self.db = pymysql.connect('10.0.0.111','root','password','green')
        self.cursor = self.db.cursor()

        self.setWindowTitle('添加用户')
        self.resize(600,400)
        self.setFixedSize(self.width(), self.height())  # 设置窗口不可放大和拉伸
        self.center()
        self.setWindowIcon(QIcon('image/add.png'))
        bg = QPixmap('image/all_set_bg.png')
        bg_l = QLabel(self)
        bg_l.setPixmap(bg)
        bg_l.setGeometry(0, 0, 600, 400)
        user_L = QLabel('输入用户名：',self)
        password_L = QLabel('输入密码：',self)
        r_password_L = QLabel('确认密码：',self)
        self.user_E = QLineEdit(self)
        self.password_E = QLineEdit(self)
        self.password_E.setEchoMode(QLineEdit.Password)
        self.r_password_E = QLineEdit(self)
        self.r_password_E.setEchoMode(QLineEdit.Password)
        confirm_btn = QPushButton('确认',self)
        confirm_btn.move(200,300)
        confirm_btn.clicked.connect(self.confirm_add)

        cancel_btn = QPushButton('取消', self)
        cancel_btn.move(350, 300)
        cancel_btn.clicked.connect(self.cancel_add)

        user_L.setGeometry(200,100,80,30)
        self.user_E.setGeometry(290,100,150,30)
        password_L.setGeometry(200,150,80,30)
        self.password_E.setGeometry(290,150,150,30)
        r_password_L.setGeometry(200,200,80,30)
        self.r_password_E.setGeometry(290,200,150,30)
        cb = QCheckBox('是否添加为管理员？',self)
        cb.setGeometry(290,250,160,30)
        cb.stateChanged.connect(self.set_root)
        self.if_set_rooot = '0'


        self.show()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def set_root(self,state):
        if state == Qt.Checked:
            print('添加为管理员')
            self.if_set_rooot = '1'
        else:
            print('添加为普通用户')
            self.if_set_rooot = '1'

    def confirm_add(self):

        if (self.user_E.text() == '')or(self.password_E.text()==''):
            print('用户名或者密码不能为空！')
            btn = QMessageBox.warning(self, "输入错误", "用户名或者密码不能为空！",
                                      QMessageBox.Ok, QMessageBox.Ok)
            if btn == QMessageBox.Ok:
                return
            else:
                return
        elif self.password_E.text() == self.r_password_E.text():
            print('确认添加用户')
            sql = "insert into user_list values('%s','%s','%s')"%(self.user_E.text(),self.password_E.text(),self.if_set_rooot)
            self.cursor.execute(sql)
            self.db.commit()
            btn = QMessageBox.information(self, "添加成功", "添加用户成功！",
                                      QMessageBox.Ok, QMessageBox.Ok)
            if btn == QMessageBox.Ok:
                self.close()
                return

            else:
                self.close()
                return


        else:
            btn = QMessageBox.warning(self,"密码错误","两次密码输入不同！",
                                     QMessageBox.Ok,QMessageBox.Ok)
            if btn == QMessageBox.Ok:
                return
            else:
                return
    def cancel_add(self):
        print('取消添加')
        self.close()
#删除用户
class Delete_user(QMainWindow):
    def iniUI(self):
        self.setWindowTitle('删除用户')
        self.resize(600,400)
        self.setFixedSize(self.width(), self.height())  # 设置窗口不可放大和拉伸
        self.center()
        self.setWindowIcon(QIcon('image/delete.png'))
        bg = QPixmap('image/all_set_bg.png')
        bg_l = QLabel(self)
        bg_l.setPixmap(bg)
        bg_l.setGeometry(0,0,600,400)
        user_L = QLabel('输入用户名：',self)
        user_L.move(150,100)
        self.user_E = QLineEdit(self)
        self.user_E.setGeometry(240,100,150,30)
        pswd_L = QLabel('管理员密码：', self)
        pswd_L.move(150, 150)
        self.pswd_E = QLineEdit(self)
        self.pswd_E.setGeometry(240, 150, 150, 30)
        self.pswd_E.setEchoMode(QLineEdit.Password)
        btn_1 = QPushButton('删除',self)
        btn_1.move(150,300)
        btn_2 = QPushButton('取消', self)
        btn_2.move(350, 300)
        btn_2.clicked.connect(self.cancel_delete)
        btn_1.clicked.connect(self.confirm_delete)


        self.show()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def confirm_delete(self):
        db = pymysql.connect('10.0.0.111','root','password','green')
        cursor = db.cursor()
        sql_1 = "select password from user_list where level = '1'"
        cursor.execute(sql_1)
        root_pswd = cursor.fetchall()
        flag = 0
        for i in root_pswd:
            if self.pswd_E.text() == i[0]:
                sql_2 = "select name from user_list"
                cursor.execute(sql_2)
                name_list =cursor.fetchall()
                flag_n = 0
                for n in name_list:
                    if self.user_E.text() == n[0]:
                        print('找到用户并删除')
                        sql_3 = "delete from user_list where name='%s'"%(self.user_E.text())
                        cursor.execute(sql_3)
                        db.commit()
                        flag_n = 1
                        btn = QMessageBox.information(self, "删除成功", "删除用户成功！",
                                                      QMessageBox.Ok, QMessageBox.Ok)
                        if btn == QMessageBox.Ok:
                            self.close()
                            return

                        else:
                            self.close()
                            return
                        break
                if flag_n == 0:
                    print('未找到用户名')
                    btn = QMessageBox.warning(self, "查找失败", "用户名不存在！",
                                                  QMessageBox.Ok, QMessageBox.Ok)
                    if btn == QMessageBox.Ok:
                        return

                    else:
                        return
                flag = 1
                break
        if flag == 0:
            print('管理员密码错误！')
            btn = QMessageBox.warning(self, "密码错误", "管理员密码错误！",
                                      QMessageBox.Ok, QMessageBox.Ok)
            if btn == QMessageBox.Ok:
                return

            else:
                return


    def cancel_delete(self):
        self.destroy()
#设置全局阈值
class Set_All_V(QWidget):
    def initUI(self):
        self.db = pymysql.connect('10.0.0.111','root','password','green')
        self.cursor = self.db.cursor()
        self.resize(1000,600)
        self.setFixedSize(self.width(), self.height())  # 设置窗口不可放大和拉伸
        self.center()
        self.setWindowTitle('参数设置')
        self.setWindowIcon(QIcon('image/mrp.png'))
        bg = QPixmap('image/all_set_bg.png')
        bg_l = QLabel(self)
        bg_l.setPixmap(bg)
        bg_l.setGeometry(0,0,1000,600)
        double_rx = QRegExp("100|([0-9]{0,4}[\.][0-9]{1,2})")
        wind_L = QLabel('风速阈值:')
        self.wind_V = QLineEdit()
        self.wind_V.setValidator(QRegExpValidator(double_rx))
        self.wind_V.setPlaceholderText('m/s')
        soil_L_1 = QLabel('区域1:')#土壤湿度是双阈值
        self.soil_V_d_1 = QLineEdit()
        self.soil_V_d_1.setValidator(QRegExpValidator(double_rx))
        self.soil_V_u_1 = QLineEdit()
        self.soil_V_u_1.setValidator(QRegExpValidator(double_rx))
        self.soil_V_d_1.setPlaceholderText('下阈值')
        self.soil_V_u_1.setPlaceholderText('上阈值')

        soil_L_2 = QLabel('区域2:')  # 土壤湿度是双阈值
        self.soil_V_d_2 = QLineEdit()
        self.soil_V_d_2.setValidator(QRegExpValidator(double_rx))
        self.soil_V_u_2 = QLineEdit()
        self.soil_V_u_2.setValidator(QRegExpValidator(double_rx))
        self.soil_V_d_2.setPlaceholderText('下阈值')
        self.soil_V_u_2.setPlaceholderText('上阈值')

        soil_L_3 = QLabel('区域3:')  # 土壤湿度是双阈值
        self.soil_V_d_3 = QLineEdit()
        self.soil_V_d_3.setValidator(QRegExpValidator(double_rx))
        self.soil_V_u_3 = QLineEdit()
        self.soil_V_u_3.setValidator(QRegExpValidator(double_rx))
        self.soil_V_d_3.setPlaceholderText('下阈值')
        self.soil_V_u_3.setPlaceholderText('上阈值')

        soil_L_4 = QLabel('区域4:')  # 土壤湿度是双阈值
        self.soil_V_d_4 = QLineEdit()
        self.soil_V_d_4.setValidator(QRegExpValidator(double_rx))
        self.soil_V_u_4 = QLineEdit()
        self.soil_V_u_4.setValidator(QRegExpValidator(double_rx))
        self.soil_V_d_4.setPlaceholderText('下阈值')
        self.soil_V_u_4.setPlaceholderText('上阈值')

        soil_L_5 = QLabel('区域5:')  # 土壤湿度是双阈值
        self.soil_V_d_5 = QLineEdit()
        self.soil_V_d_5.setValidator(QRegExpValidator(double_rx))
        self.soil_V_u_5 = QLineEdit()
        self.soil_V_u_5.setValidator(QRegExpValidator(double_rx))
        self.soil_V_d_5.setPlaceholderText('下阈值')
        self.soil_V_u_5.setPlaceholderText('上阈值')

        soil_L_6 = QLabel('区域6:')  # 土壤湿度是双阈值
        self.soil_V_d_6 = QLineEdit()
        self.soil_V_d_6.setValidator(QRegExpValidator(double_rx))
        self.soil_V_u_6 = QLineEdit()
        self.soil_V_u_6.setValidator(QRegExpValidator(double_rx))
        self.soil_V_d_6.setPlaceholderText('下阈值')
        self.soil_V_u_6.setPlaceholderText('上阈值')

        # soil_L_7 = QLabel('区域7:')  # 土壤湿度是双阈值
        # self.soil_V_d_7 = QLineEdit()
        # self.soil_V_d_7.setValidator(QRegExpValidator(double_rx))
        # self.soil_V_u_7 = QLineEdit()
        # self.soil_V_u_7.setValidator(QRegExpValidator(double_rx))
        # self.soil_V_d_7.setPlaceholderText('下阈值')
        # self.soil_V_u_7.setPlaceholderText('上阈值')
        #
        # soil_L_8 = QLabel('区域8:')  # 土壤湿度是双阈值
        # self.soil_V_d_8 = QLineEdit()
        # self.soil_V_d_8.setValidator(QRegExpValidator(double_rx))
        # self.soil_V_u_8 = QLineEdit()
        # self.soil_V_u_8.setValidator(QRegExpValidator(double_rx))
        # self.soil_V_d_8.setPlaceholderText('下阈值')
        # self.soil_V_u_8.setPlaceholderText('上阈值')

        rain_L = QLabel('降雨量阈值:')
        self.rain_V = QLineEdit()
        self.rain_V.setValidator(QRegExpValidator(double_rx))
        self.rain_V.setPlaceholderText('mm/min')
        source_water = QLabel('  水源选择水位:')
        self.source_water_v = QLineEdit()
        self.source_water_v.setValidator(QRegExpValidator(double_rx))
        self.source_water_v.setPlaceholderText('m')
        water_L_u = QLabel('上水库预警水位:')
        water_L_d = QLabel('下水库预警水位:')
        self.water_L_u_h = QLineEdit()
        self.water_L_u_h.setValidator(QRegExpValidator(double_rx))
        self.water_L_u_l = QLineEdit()
        self.water_L_u_l.setValidator(QRegExpValidator(double_rx))
        self.water_L_d_h = QLineEdit()
        self.water_L_d_h.setValidator(QRegExpValidator(double_rx))
        self.water_L_d_l = QLineEdit()
        self.water_L_d_l.setValidator(QRegExpValidator(double_rx))
        self.water_L_d_h.setPlaceholderText('高预警水位(m)')
        self.water_L_d_l.setPlaceholderText('低预警水位(m)')
        self.water_L_u_h.setPlaceholderText('高预警水位(m)')
        self.water_L_u_l.setPlaceholderText('低预警水位(m)')
        camera_L = QLabel('拍照频率:')
        camera_U = ['选择','天','周']
        self.camera_box = QComboBox()
        self.camera_box.addItems(camera_U)
        self.camera_box.activated[str].connect(self.select_unit)
        camera_D = ['天','1','2','3','4','5','6','7']
        camera_W = ['周','1','2','3','4','5','6','7']
        self.D_box = QComboBox()
        self.D_box.addItems(camera_D)
        self.D_box.activated[str].connect(self.set_camera_D)
        self.D_box.hide()
        self.W_box = QComboBox()
        self.W_box.addItems(camera_W)
        self.W_box.activated[str].connect(self.set_camera_W)
        self.W_box.hide()
        self.camera_L = QLabel('选择时间：')
        self.camera_L.hide()
        layout = QGridLayout()
        layout.addWidget(wind_L,0,0)
        layout.addWidget(self.wind_V,0,1)
        layout.addWidget(rain_L, 1, 0)
        layout.addWidget(self.rain_V,1,1 )
        layout.addWidget(camera_L,2,0)
        layout.addWidget(self.camera_box,2,1)
        layout.addWidget(self.camera_L, 3, 0)
        layout.addWidget(self.D_box, 3, 1)
        layout.addWidget(self.W_box,3,1)
        layout.addWidget(source_water,4,2)
        layout.addWidget(self.source_water_v,4,3)
        layout.addWidget(water_L_u,0,2)
        layout.addWidget(self.water_L_u_l,0,3)
        layout.addWidget(self.water_L_u_h,1,3)
        layout.addWidget(water_L_d,2,2)
        layout.addWidget(self.water_L_d_l,2,3)
        layout.addWidget(self.water_L_d_h,3,3)
        layout.setSpacing(5)
        group = QGroupBox(self)
        group.setLayout(layout)
        group.setFont(QFont('温软雅黑',12))
        group.setGeometry(200,20,600,200)
        self.camera_time = ''#拍照时间间隔

        layout_1 = QGridLayout()
        layout_1.addWidget(soil_L_1,0,0)
        layout_1.addWidget(self.soil_V_d_1,0,1)
        layout_1.addWidget(self.soil_V_u_1,1,1)

        layout_1.addWidget(soil_L_2, 0, 2)
        layout_1.addWidget(self.soil_V_d_2, 0, 3)
        layout_1.addWidget(self.soil_V_u_2, 1, 3)

        layout_1.addWidget(soil_L_3, 0, 4)
        layout_1.addWidget(self.soil_V_d_3, 0, 5)
        layout_1.addWidget(self.soil_V_u_3, 1, 5)

        layout_1.addWidget(soil_L_4, 2, 0)
        layout_1.addWidget(self.soil_V_d_4, 2, 1)
        layout_1.addWidget(self.soil_V_u_4, 3, 1)

        layout_1.addWidget(soil_L_5, 2, 2)
        layout_1.addWidget(self.soil_V_d_5, 2, 3)
        layout_1.addWidget(self.soil_V_u_5, 3, 3)

        layout_1.addWidget(soil_L_6, 2, 4)
        layout_1.addWidget(self.soil_V_d_6, 2, 5)
        layout_1.addWidget(self.soil_V_u_6, 3, 5)


        group_1 = QGroupBox('土壤湿度阈值(%RH)',self)
        group_1.setLayout(layout_1)
        group_1.setFont(QFont('温软雅黑', 12))
        group_1.setGeometry(200, 230, 600, 200)

        btn_1 = QPushButton('确定',self)
        btn_2 = QPushButton('退出',self)
        btn_1.clicked.connect(self.confirm_set)
        btn_2.clicked.connect(self.cancel_set)
        btn_1.setFont(QFont('微软雅黑',10))
        btn_2.setFont(QFont('微软雅黑', 10))
        btn_1.move(325,500)
        btn_2.move(575,500)

        self.show()

    def select_unit(self,text):
        self.camera_L.show()
        if text == '天':
            print('选择单位:天')
            self.W_box.hide()
            self.D_box.show()
        elif text == '周':
            self.D_box.hide()
            self.W_box.show()



    def set_camera_D(self,text):
        if text != '天':
            v = int(text)
            self.camera_time = v * 3600 * 24
            print('设置拍照时间间隔:\n',self.camera_time)
    def set_camera_W(self,text):
        if text != '周':
            v = int(text)
            self.camera_time = v * 7 * 3600 *24
            print('设置拍照时间间隔:\n', self.camera_time)

    def confirm_set(self):
        wind_v = self.wind_V.text()
        rain_v = self.rain_V.text()
        water_d_l = self.water_L_d_l.text()
        water_d_h = self.water_L_d_h.text()
        water_u_l = self.water_L_u_l.text()
        water_u_h = self.water_L_u_h.text()
        source_water = self.source_water_v.text()
        soil_v = [[self.soil_V_u_1.text(),self.soil_V_d_1.text()],[self.soil_V_u_2.text(),self.soil_V_d_2.text()],[self.soil_V_u_3.text(),self.soil_V_d_3.text()],[self.soil_V_u_4.text(),self.soil_V_d_4.text()],
                  [self.soil_V_u_5.text(),self.soil_V_d_5.text()],[self.soil_V_u_6.text(),self.soil_V_d_6.text()]]
        print('风速阈值：',wind_v)
        print('土壤湿度阈值:')
        print('\t区域1：高：%s低：%s\t区域2：高：%s低：%s\t区域3：高：%s低：%s\t区域4：高：%s低：%s'%(soil_v[0][0],soil_v[0][1],soil_v[1][0],soil_v[1][1],soil_v[2][0],soil_v[2][1],soil_v[3][0],soil_v[3][1]))
        print('\t区域5：高：%s低：%s\t区域6：高：%s低：%s\t' % (
            soil_v[4][0], soil_v[4][1], soil_v[5][0], soil_v[5][1]))
        print('降雨量阈值',rain_v)
        print('水库水位阈值:')
        print('\t上水库低：',water_u_l)
        print('\t上水库高：', water_u_h)
        print('\t下水库低：', water_d_l)
        print('\t下水库高：', water_d_h)
        print('水源选择水位：',source_water)
        print('拍照时间',self.camera_time)

        sql = "update global set zdwind = '%s',zdrain = '%s',source_water = '%s',uplow = '%s',upheigh = '%s',downlow = '%s',downheigh = '%s' where id = 1"%(wind_v,rain_v,source_water,water_u_l,water_u_h,water_d_l,water_d_h)
        self.cursor.execute(sql)
        self.db.commit()
        sql_ = "update command1 set set_max = '%s' where id = 14"%(self.camera_time)
        self.cursor.execute(sql_)
        self.db.commit()

        for i in range(6):
            a = i+1
            sql_soil = "update command1 set set_max = '%s',set_min = '%s' where id = '%s'"%(soil_v[i][0],soil_v[i][1],a)
            self.cursor.execute(sql_soil)
            self.db.commit()
        button = QMessageBox.information(self, "设置成功", "参数设置成功！",
                                         QMessageBox.Ok, QMessageBox.Ok)
        if button == QMessageBox.Ok:
            self.close()
            return
        else:
            self.close()
            return

    def cancel_set(self):
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app =QApplication(sys.argv)
    home_page = Home_window()
    home_page.initUI('1')
    sys.exit(app.exec_())


