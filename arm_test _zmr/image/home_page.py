from PyQt5.QtWidgets import QMainWindow,QAction,QLabel,QLineEdit,QPushButton,QApplication,QGroupBox,QGridLayout,QMessageBox,QCheckBox,QDesktopWidget
from PyQt5.QtGui import QIcon,QFont,QPixmap
from PyQt5.QtCore import QDateTime,QTimer,Qt
import pymysql
from area_info_set_page import Device_set
from all_set_page import All_device_set
import image
import sys
class Home_window(QMainWindow):
    # def __init__(self):
    #     super().__init__()
    #     self.initUI()

    def initUI(self,user_level):
        pymysql_ip = '10.0.0.112'
        pymysql_password = 'password'
        self.db = pymysql.connect(pymysql_ip,'root',pymysql_password,'green')
        self.cursor = self.db.cursor()

        self.user_level = user_level
        if user_level == '1':
            user_menu_state = False
        else:
            user_menu_state = True
        self.screen_w = int(QApplication.desktop().width() *0.9)
        self.screen_h = int(QApplication.desktop().height()*0.9)
        self.resize(self.screen_w,self.screen_h)
        self.center()
        self.setWindowTitle('屋顶绿化系统')
        self.setWindowIcon(QIcon(':/window_icon.png'))
        self.statusBar().showMessage('准备就绪')
        #界面纯白背景设置
        image = QPixmap(':/bg_image_white.jpg')
        self.bg_image = QLabel(self)
        self.bg_image.setPixmap(image)
        self.bg_image.setGeometry(0, 65, self.screen_w, self.screen_h-100)

        #设计菜单：*******************************************************
        #设置

        set_action = QAction(QIcon(':/set.png'),'设置',self)
        set_action.setShortcut('Ctrl+S')
        set_action.setStatusTip('设置')
        set_action.triggered.connect(self.Setting)
        #退出
        esc_action = QAction(QIcon(':exit.png'),'退出',self)
        esc_action.setShortcut('Ctrl+Q')
        esc_action.setStatusTip('退出')
        esc_action.triggered.connect(self.Esc)
        #用户管理
        add_user = QAction(QIcon(':/add.png'),'添加用户',self)
        add_user.setShortcut('Ctrl+A')
        add_user.setStatusTip('添加用户')
        add_user.triggered.connect(self.add_U)

        delete_user = QAction(QIcon(':/delete.png'),'删除用户',self)
        delete_user.setStatusTip('删除用户')
        delete_user.setShortcut('Ctrl+D')
        delete_user.triggered.connect(self.delete_U)

        phone_manager = QAction(QIcon(':/phone.png'), '绑定手机号', self)
        phone_manager.setStatusTip('绑定手机号')
        phone_manager.setShortcut('Ctrl+N')
        phone_manager.triggered.connect(self.set_phone)

        #修改密码：
        password_manager = QAction(QIcon(':/manager.png'),'修改密码',self)
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
        device_set = QAction(QIcon(':/all_set.png'),'一键设置',self)
        device_set.triggered.connect(self.All_device_set)
        tool_bar_1 = self.addToolBar('一键设置')
        tool_bar_1.addAction(device_set)
        #阈值设置
        data_set = QAction(QIcon(':/mrp.png'), '参数阈值设置', self)
        data_set.triggered.connect(self.All_value_set)
        tool_bar_0 = self.addToolBar('参数设置')
        tool_bar_0.addAction(data_set)



        #刷新
        do_refresh = QAction(QIcon(':/refresh.png'), '刷新', self)
        do_refresh.triggered.connect(self.do_refresh)
        tool_bar_2 = self.addToolBar('刷新')
        tool_bar_2.addAction(do_refresh)

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

        time_layout = QGridLayout()
        self.time_Label = QLabel(self)
        self.time_Label.resize(200,20)
        self.time_Label.setFont(self.font)
        time_layout.addWidget(self.time_Label)
        self.time_group = QGroupBox(self)
        self.time_group.setGeometry(int(self.screen_w*(5/6)), 10, int(self.screen_w*(3/20)), 55)
        # self.time_group.resize(225,55)
        self.time_group.setLayout(time_layout)
        timer = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start()
            # 光照强度

        the_global_info_layout = QGridLayout()
        sun_image = QPixmap(':/sun.png')
        self.sun_l = QLabel(self)
        self.sun_l.setPixmap(sun_image)
        self.sun_l.resize(80,80)#光照强度图标显示
        # self.sun_l.setGeometry(20,80,80,80)
        self.sun_int = '10'
        self.sg = 'blue'
        #光照强度数值显示
        self.sun_data = QLabel('<font color = %s>光照强度:</font><font color= %s>%s</font>' % (self.label_color,self.sg, self.sun_int), self)
        self.sun_data.setFont(self.font)
        # self.sun_data.move(10,160)
            #降雨量
        rain_image = QPixmap(':/rain.png')
        self.rain_l = QLabel(self)
        self.rain_l.setPixmap(rain_image)
        self.rain_l.resize(80,80)
        # self.rain_l.setGeometry(140, 80, 80, 80)
        self.rain_int = '10'
        self.rg = 'blue'
        self.rain_data = QLabel('<font color = %s>降雨量:</font><font color= %s>%smL</font>' % (self.label_color,self.rg, self.rain_int), self)
        self.rain_data.setFont(self.font)
        # self.rain_data.move(140, 160)
            #温度
        tim_image = QPixmap(':/tim.png')
        self.tim_l = QLabel(self)
        self.tim_l.setPixmap(tim_image)
        self.tim_l.resize(80,80)
        # self.tim_l.setGeometry(260, 80, 80, 80)
        self.tim_int = '10'
        self.tg = 'blue'
        self.tim_data = QLabel('<font color = %s>大气温度</font><font color= %s>%s℃</font>' % (self.label_color,self.tg, self.tim_int), self)
        self.tim_data.setFont(self.font)
        # self.tim_data.move(260, 160)
            #大气湿度
        wet_image = QPixmap(':/wet.png')
        self.wet_l = QLabel(self)
        self.wet_l.setPixmap(wet_image)
        self.wet_l.resize(80, 80)
        # self.tim_l.setGeometry(260, 80, 80, 80)
        self.wet_int = '10'
        self.wg = 'blue'
        self.wet_data = QLabel(
            '<font color = %s>大气湿度</font><font color= %s>%s℃</font>' % (self.label_color, self.wg, self.wet_int))
        self.wet_data.setFont(self.font)


            #风速
        speed_image = QPixmap(':/wind_speed.png')
        self.speed_l = QLabel(self)
        self.speed_l.setPixmap(speed_image)
        self.speed_l.resize(80,80)
        # self.speed_l.setGeometry(380, 80, 80, 80)
        self.speed_int = '10'
        self.spg = 'blue'
        self.speed_data = QLabel('<font color = %s>风速:</font><font color= %s>%s</font>' % (self.label_color,self.spg, self.speed_int), self)
        self.speed_data.setFont(self.font)
        # self.speed_data.move(380, 160)
            #风向
        direction_image = QPixmap(':/wind_direction.png')
        self.direction_l = QLabel(self)
        self.direction_l.setPixmap(direction_image)
        self.direction_l.resize(80,80)
        # self.direction_l.setGeometry(500, 80, 80, 80)
        self.direction_int = '东南'
        self.dg = 'blue'
        self.direction_data = QLabel('<font color = %s>风向:</font><font color= %s>%s</font>' % (self.label_color,self.dg, self.direction_int), self)
        self.direction_data.setFont(self.font)
        # self.direction_data.move(500, 160)
            #下方水位
        w_level_image = QPixmap(':/water.png')
        self.d_water_level = QLabel(self)
        self.d_water_level.setPixmap(w_level_image)
        self.d_water_level.resize(80,80)
        # self.d_water_level.setGeometry(20,200,80,80)
        self.d_water_int = '50'
        self.dwg = 'blue'
        self.d_water_data = QLabel('<font color = %s>下方水位:</font><font color= %s>%sL</font>' % (self.label_color,self.dwg, self.d_water_int), self)
        self.d_water_data.setFont(self.font)
        # self.d_water_data.move(20,280)
            #上方水位
        self.u_water_level = QLabel(self)
        self.u_water_level.setPixmap(w_level_image)
        self.u_water_level.resize(80,80)
        # self.u_water_level.setGeometry(140, 200, 80, 80)
        self.u_water_int = '40'
        self.uwg = 'red'
        self.u_water_data = QLabel('<font color = %s>上方水位:</font><font color= %s>%sL</font>' % (self.label_color,self.uwg, self.u_water_int), self)
        self.u_water_data.setFont(self.font)
        # self.u_water_data.move(130, 280)
            #水泵开关状态
        pump_image = QPixmap(':/pump.png')
        self.pump_l = QLabel(self)
        self.pump_l.setPixmap(pump_image)
        self.pump_l.resize(80,80)
        # self.pump_l.setGeometry(260,200,80,80)
        self.pump_int = 'OFF'
        self.pump_g = 'red'
        self.pump_data = QLabel(
            '<font color = %s>水泵状态:</font><font color= %s>%s</font>' % (self.label_color, self.pump_g, self.pump_int),
            self)
        self.pump_data.setFont(self.font)
        # self.pump_data.move(250, 280)
            #灭菌灯开关状态
        light_image = QPixmap(':/light.png')
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
        # self.light_data.move(370, 280)
        the_global_info_layout.addWidget(self.sun_l,0,0)
        the_global_info_layout.addWidget(self.sun_data, 1, 0)
        the_global_info_layout.addWidget(self.rain_l, 0, 1)
        the_global_info_layout.addWidget(self.rain_data, 1, 1)
        the_global_info_layout.addWidget(self.tim_l, 0, 2)
        the_global_info_layout.addWidget(self.tim_data, 1, 2)
        the_global_info_layout.addWidget(self.wet_l, 0, 3)
        the_global_info_layout.addWidget(self.wet_data, 1, 3)
        the_global_info_layout.addWidget(self.speed_l, 0, 4)
        the_global_info_layout.addWidget(self.speed_data, 1, 4)
        the_global_info_layout.addWidget(self.direction_l, 2, 0)
        the_global_info_layout.addWidget(self.direction_data,3, 0)
        the_global_info_layout.addWidget(self.d_water_level, 2, 1)
        the_global_info_layout.addWidget(self.d_water_data, 3, 1)
        the_global_info_layout.addWidget(self.u_water_level, 2, 2)
        the_global_info_layout.addWidget(self.u_water_data, 3, 2)
        the_global_info_layout.addWidget(self.pump_l, 2, 3)
        the_global_info_layout.addWidget(self.pump_data, 3, 3)
        the_global_info_layout.addWidget(self.light_l,2,4)
        the_global_info_layout.addWidget(self.light_data,3,4)
        #全局信息显示组：光照强度，风速，风向等
        self.the_global_info_group = QGroupBox(self)
        # self.the_global_info_group.setGeometry(20, 80, 900, 240)
        self.the_global_info_group.resize(int(self.screen_w*0.6),int(self.screen_h*0.3))
        self.the_global_info_group.setLayout(the_global_info_layout)


            #现场照片显示设计

        site_image = QPixmap(':/garden.png')
        self.site_image_l = QLabel()
        self.site_image_l.setPixmap(site_image)
        # self.site_image_l.resize(400,360)
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
            #8块区域信息显示
        self.area_info = {}
        sql = "select manual,type,switch from command1 where name between 's1' and 's8'"
        self.cursor.execute(sql)
        area_info = self.cursor.fetchall()
        sql_ = "select state,avg from interface"
        self.cursor.execute(sql_)
        sensor_info = self.cursor.fetchall()
        print('区域手动模式状态,运行模式,电磁阀开关:',(area_info))
        print('电磁阀状态，土壤湿度',sensor_info)
        area_sensor_info = []
        for i in range(8):
            a = list(sensor_info[i])
            b = list(area_info[i])
            a.extend(b)
            area_sensor_info.append(a)
        print('整体信息：电磁阀状态(0)，土壤湿度(1)，区域手动模式(2)，运行模式(3)，电磁阀开关(4)',area_sensor_info)
        n = 0
        diancifa = {0:['OFF','blue'],1:['ON','red']}
        modes = {'A':['自动','blue'],'B':['定时','green']}

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
                  self.area_information_5,self.area_information_6,
                  self.area_information_7,self.area_information_8]
        zuobiao = [[0,0],[0,1],[0,2],[0,3],
                   [1,0],[1,1],[1,2],[1,3]]
        self.main_area_group = QGroupBox(self)
        main_area_layout = QGridLayout()
        for i in range(len(self.area_info)):
            main_area_layout.addWidget(groups[i]('%s号区域'%(i+1),self.area_info[i][0],self.area_info[i][1],self.area_info[i][2],self.area_info[i][3],self.area_info[i][4],self.area_info[i][5]),zuobiao[i][0],zuobiao[i][1])
        self.main_area_group.setLayout(main_area_layout)
        # self.main_area_group.setGeometry(20,450,1460,250)
        self.main_area_group.resize(int(self.screen_w*0.97),int(self.screen_h*0.3))
        # *******************************************************************

        #布局显示
        self.Buju()

        self.show()

    #区域信息显示

    def area_information_1(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):
        self.group_1 = QGroupBox(name)
        self.group_1.resize(300,100)
        layout = QGridLayout()
        #土壤湿度

        soil_moisture_L = QLabel('<font>土壤湿度：</font><font color = %s>%s</font>'%(soil_color,soil_moisture))
        soil_moisture_L.setFont(self.font)
        #电磁阀开关状态

        switch_status_L = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        switch_status_L.setFont(self.font)
        #当前运行模式

        current_mode_L = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        current_mode_L.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon(':/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_1)
        #把以上组件放入网格布局中
        layout.addWidget(soil_moisture_L,1,0)
        layout.addWidget(current_mode_L,1,1)
        layout.addWidget(switch_status_L,2,0)
        layout.addWidget(a_button,2,1)
        self.group_1.setLayout(layout)
        return self.group_1

    def area_information_2(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):
        self.group_2 = QGroupBox(name)
        self.group_2.resize(300,100)
        layout = QGridLayout()
        #土壤湿度

        soil_moisture_L = QLabel('<font>土壤湿度：</font><font color = %s>%s</font>'%(soil_color,soil_moisture))
        soil_moisture_L.setFont(self.font)
        #电磁阀开关状态

        switch_status_L = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        switch_status_L.setFont(self.font)
        #当前运行模式

        current_mode_L = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        current_mode_L.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon(':/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_2)
        #把以上组件放入网格布局中
        layout.addWidget(soil_moisture_L,1,0)
        layout.addWidget(current_mode_L,1,1)
        layout.addWidget(switch_status_L,2,0)
        layout.addWidget(a_button,2,1)
        self.group_2.setLayout(layout)
        return self.group_2

    def area_information_3(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):

        layout = QGridLayout()
        #土壤湿度

        soil_moisture_L = QLabel('<font>土壤湿度：</font><font color = %s>%s</font>'%(soil_color,soil_moisture))
        soil_moisture_L.setFont(self.font)
        #电磁阀开关状态

        switch_status_L = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        switch_status_L.setFont(self.font)
        #当前运行模式

        current_mode_L = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        current_mode_L.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon(':/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_3)
        #把以上组件放入网格布局中
        layout.addWidget(soil_moisture_L,1,0)
        layout.addWidget(current_mode_L,1,1)
        layout.addWidget(switch_status_L,2,0)
        layout.addWidget(a_button,2,1)
        self.group_3 = QGroupBox(name)
        self.group_3.resize(300, 100)
        self.group_3.setLayout(layout)
        return self.group_3

    def area_information_4(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):
        self.group_4 = QGroupBox(name)
        self.group_4.resize(300,100)
        layout = QGridLayout()
        #土壤湿度

        soil_moisture_L = QLabel('<font>土壤湿度：</font><font color = %s>%s</font>'%(soil_color,soil_moisture))
        soil_moisture_L.setFont(self.font)
        #电磁阀开关状态

        switch_status_L = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        switch_status_L.setFont(self.font)
        #当前运行模式

        current_mode_L = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        current_mode_L.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon(':/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_4)
        #把以上组件放入网格布局中
        layout.addWidget(soil_moisture_L,1,0)
        layout.addWidget(current_mode_L,1,1)
        layout.addWidget(switch_status_L,2,0)
        layout.addWidget(a_button,2,1)
        self.group_4.setLayout(layout)
        return self.group_4

    def area_information_5(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):
        layout = QGridLayout()
        #土壤湿度

        soil_moisture_L = QLabel('<font>土壤湿度：</font><font color = %s>%s</font>'%(soil_color,soil_moisture))
        soil_moisture_L.setFont(self.font)
        #电磁阀开关状态

        switch_status_L = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        switch_status_L.setFont(self.font)
        #当前运行模式

        current_mode_L = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        current_mode_L.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon(':/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_5)
        #把以上组件放入网格布局中
        layout.addWidget(soil_moisture_L,1,0)
        layout.addWidget(current_mode_L,1,1)
        layout.addWidget(switch_status_L,2,0)
        layout.addWidget(a_button,2,1)
        self.group_5 = QGroupBox(name)
        self.group_5.resize(300, 100)
        self.group_5.setLayout(layout)
        return self.group_5

    def area_information_6(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):
        layout = QGridLayout()
        #土壤湿度

        soil_moisture_L = QLabel('<font>土壤湿度：</font><font color = %s>%s</font>'%(soil_color,soil_moisture))
        soil_moisture_L.setFont(self.font)
        #电磁阀开关状态

        switch_status_L = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        switch_status_L.setFont(self.font)
        #当前运行模式

        current_mode_L = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        current_mode_L.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon(':/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_6)
        #把以上组件放入网格布局中
        layout.addWidget(soil_moisture_L,1,0)
        layout.addWidget(current_mode_L,1,1)
        layout.addWidget(switch_status_L,2,0)
        layout.addWidget(a_button,2,1)
        self.group_6 = QGroupBox(name)
        self.group_6.resize(300, 100)
        self.group_6.setLayout(layout)
        return self.group_6

    def area_information_7(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):
        layout = QGridLayout()
        #土壤湿度

        soil_moisture_L = QLabel('<font>土壤湿度：</font><font color = %s>%s</font>'%(soil_color,soil_moisture))
        soil_moisture_L.setFont(self.font)
        #电磁阀开关状态

        switch_status_L = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        switch_status_L.setFont(self.font)
        #当前运行模式

        current_mode_L = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        current_mode_L.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon(':/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_7)
        #把以上组件放入网格布局中
        layout.addWidget(soil_moisture_L,1,0)
        layout.addWidget(current_mode_L,1,1)
        layout.addWidget(switch_status_L,2,0)
        layout.addWidget(a_button,2,1)
        self.group_7 = QGroupBox(name)
        self.group_7.resize(300, 100)
        self.group_7.setLayout(layout)
        return self.group_7

    def area_information_8(self,name,soil_moisture,soil_color,switch_status,switch_status_color,current_mode,current_mode_color):
        layout = QGridLayout()
        #土壤湿度

        soil_moisture_L = QLabel('<font>土壤湿度：</font><font color = %s>%s</font>'%(soil_color,soil_moisture))
        soil_moisture_L.setFont(self.font)
        #电磁阀开关状态

        switch_status_L = QLabel('<font>水阀开关：</font><font color = %s>%s</font>' % (switch_status_color, switch_status))
        switch_status_L.setFont(self.font)
        #当前运行模式

        current_mode_L = QLabel(
            '<font>运行模式：</font><font color = %s>%s</font>' % (current_mode_color, current_mode))
        current_mode_L.setFont(self.font)
        #调整按钮
        a_button = QPushButton('调整参数')
        a_button.setFont(self.font)
        a_button.setIcon(QIcon(':/set.png'))
        a_button.setToolTip('调整当前区域的相关参数')
        a_button.clicked.connect(self.set_alone_8)
        #把以上组件放入网格布局中
        layout.addWidget(soil_moisture_L,1,0)
        layout.addWidget(current_mode_L,1,1)
        layout.addWidget(switch_status_L,2,0)
        layout.addWidget(a_button,2,1)
        self.group_8 = QGroupBox(name)
        self.group_8.resize(300, 100)
        self.group_8.setLayout(layout)
        return self.group_8

# 桌面显示设计**************************************************************



    # 窗口整体布局函数
    def Buju(self):
        self.the_global_info_group.setGeometry(int(self.screen_w*0.01), int(self.screen_h*0.1), int(self.screen_w*0.5), int(self.screen_h*0.45))
        self.main_area_group.setGeometry(int(self.screen_w*0.0133),int(self.screen_h*0.5625),int(self.screen_w*0.97),int(self.screen_h*0.32))
        self.site_image_group.setGeometry(int(self.screen_w*(2/3)), int(self.screen_h*0.13), int(self.screen_w*(4/15)), int(self.screen_h*0.45))
    #绑定手机号
    def set_phone(self):
        print('绑定手机号')
        self.set_phone_window = Set_phone_number()
        self.set_phone_window.initUI()





    #设置全局参数阈值
    def All_value_set(self):
        print('设置全局参数阈值')


    def show_time(self):
        date_time = QDateTime.currentDateTime()
        text=date_time.toString()
        self.time_Label.setText('<font color=blue>%s</font>'%(text))
    def look_the_pic(self):
        print('查看历史照片')
    def Setting(self):
        print('点击设置')
    def Esc(self):
        self.destroy()
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
    def set_alone_7(self):
        print('设置当前土地')
        area_id = '7'
        self.the_area_window_7 = Device_set()
        self.the_area_window_7.initUI(area_id)
    def set_alone_8(self):
        print('设置当前土地')
        area_id = '8'
        self.the_area_window_8 = Device_set()
        self.the_area_window_8.initUI(area_id)
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

class Set_phone_number(QMainWindow):#绑定手机号
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def initUI(self):
        self.db_1 = pymysql.connect('10.0.0.112','root','password','green')
        self.cursor_1 = self.db_1.cursor()
        self.db_2 = pymysql.connect('10.0.0.33', 'root', 'zong123', 'green_roof')
        self.cursor_2 = self.db_2.cursor()
        self.resize(600,400)
        self.center()
        self.setWindowIcon(QIcon(':/phone.png'))
        self.setWindowTitle('绑定手机号')
        user_L = QLabel('用户名：')
        self.user_E = QLineEdit()
        pswd_L = QLabel('密码：')
        self.pswd_E = QLineEdit()
        self.pswd_E.setEchoMode(QLineEdit.Password)
        phone_L = QLabel('手机号：')
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
class Password_set(QMainWindow):
    def iniUI(self):
        pymysql_ip = '10.0.0.112'
        pymysql_password = 'password'
        self.db = pymysql.connect(pymysql_ip,'root',pymysql_password,'green')
        self.cursor = self.db.cursor()
        self.setWindowTitle('密码管理')
        self.setWindowIcon(QIcon(':/password.png'))
        self.resize(600,400)
        self.center()
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
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

class Add_user(QMainWindow):

    def iniUI(self):
        self.db = pymysql.connect('10.0.0.112','root','password','green')
        self.cursor = self.db.cursor()

        self.setWindowTitle('添加用户')
        self.resize(600,400)
        self.center()
        self.setWindowIcon(QIcon(':/add.png'))
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

class Delete_user(QMainWindow):
    def iniUI(self):
        self.setWindowTitle('删除用户')
        self.resize(600,400)
        self.center()
        self.setWindowIcon(QIcon(':/delete.png'))
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
        db = pymysql.connect('10.0.0.112','root','password','green')
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
if __name__ == '__main__':
    app =QApplication(sys.argv)
    home_page = Home_window()
    home_page.initUI('1')
    sys.exit(app.exec_())


