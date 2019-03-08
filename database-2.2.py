import threading
import time
import pymysql
import datetime
import numpy as np

sqlselect_data="select value,state from data where name='%s' order by id desc limit 1;"
sqlselect_data_y5="select state from data where name='%s' order by id desc limit 5; "
sqlselect_data_solid_y5="select state from data where address='%d' order by id desc limit 5; "
sqlselect_data_soild_address="select value,state from data where address='%d' order by time desc limit 1;"
sqlselectdevices_s123=" select exist from device where address='%d'or  address='%d' or  address='%d';"
sqlselect_devices=" select exist from device where name='%s';"
sqlselect_command1="select switch,type,manual,manswitch,set_max,set_min,switch1 from command1 where name='%s';"
sqlselect_command1_time="select timing11,timing12,timing21,timing22 from command1 where name='%s';"
sqlselects1_command1_zdtime="select zdtime11,zdtime12,zdtime21,zdtime22 from command1 where name='%s';"
sqlselect_manswitch="select manswitch from command1 where name='%s';"
sqlselect_global="select zdwind,zdrain,uplow,upheigh,downlow,downheigh,rain,source_water from global;"
sqlselect_device_data="select name,exist,send from device;"
sqlselect_command1_switch_1="select id from command1 where switch=1 and id<9;"
sqlselect_command1_switch1_1="select id from command1 where switch1=1 and id<9 and manual<>'Y';"
sqlselect_command1_manual="select id,manual from command1 where id<9;"
sqlselect_command1_manual_id="select manual from command1 where id='%d';"
sqlselect_command1_switch1_on=" select switch1 from command1 where id<9 and switch1=1;"
sqlselect_command1_camera_set_max="select set_max from command1 where name='camera';"
sqlselect_command1_uvlight_zdtime11="select zdtime11 from command1 where name='uv_light';"

sqlupdate_interface="update interface set state='%s',avg='%f' where name='%s';"
sqlupdate_device_broke="update device set broke='%d' where name='%s';"
sqlupdate_device_soil_broke="update device set broke='%d' where address='%d';"
sqlupdate_switch1_manswitch="update command1 set switch1='%d' where name='%s';"
sqlupdate_switch="update command1 set switch='%d' where name='%s';"
sqlupdate_device_send="update device set send='%d' where name='%s'"
sqlupdate_command1_switch0_all="update command1 set switch1=0 where id<9; "
sqlupdate_command1_switch1="update command1 set switch1='%d' where id='%d'; "
sqlupdate_command1_switch1_all_0="update command1 set switch1=0 where id<7; "
sqlupdate_command1_reservoir="update command1 set switch1='%d' where name='reservoir';"
sqlupdate_command1_tapwater="update command1 set switch1='%d' where name='tapwater';"
db = pymysql.connect("10.0.0.111", "root", "password", "green")
db.autocommit(True)
cursor = db.cursor()

def average(list):               # 调用函数求列表平均值
    avg = 0
    avg = sum(list) / (len(list) * 1.0)
    return avg

def send_data():
    db = pymysql.connect("10.0.0.111", "root", "password", "green")
    db.autocommit(True)
    cursor = db.cursor()
    while(1):
        print('send_data启动成功')
        try:
            cursor.execute(sqlselect_device_data)
            fetsend = cursor.fetchall()
        except:
            db.rollback()
        for row2 in fetsend:
            name = row2[0]
            if int(row2[2])==0 and int(row2[1])==1:                #只对存在且需要至1的传感器发送信息
                print("需要发送信息传感器：",name)
                try:
                    cursor.execute(sqlupdate_device_send % (1,name))
                    db.commit()
                except:
                    db.rollback()
            if int(row2[1])==0:                                      #对不存在的传感器信息置0
                try:
                    cursor.execute(sqlupdate_device_send % (0,name))
                    db.commit()
                except:
                    db.rollback()
        time.sleep(60)
        print('send_data结束')
def other_sensor(sensor):
    try:
        cursor.execute(sqlselect_data%(sensor))
        fet_sensor = cursor.fetchall()
        cursor.execute(sqlselect_devices % (sensor))
        exist_sensor = cursor.fetchall()
        print('%s测量结果:'%(sensor),fet_sensor)
    except:
        db.rollback()
    if exist_sensor[0][0]==0:
        try:
            cursor.execute(sqlupdate_interface % ('lost', 0,sensor))
            db.commit()
        except:
            db.rollback()
    else:
        if fet_sensor[0][1] == 'z':
            value_sensor = fet_sensor[0][0]
            try:  # 将传感器信息状态变为正常
                cursor.execute(sqlupdate_interface % ('normal',value_sensor, sensor))
                cursor.execute(sqlupdate_device_broke % (0,sensor))
                db.commit()
            except:
                db.rollback()
        else:
            cursor.execute(sqlselect_data_y5 % (sensor))
            fet_broke = cursor.fetchall()
            k = 0
            print("%s传感器最近5次异常记录表：" %(sensor),fet_broke)
            for row_broke in fet_broke:
                if row_broke[0] == 'z':
                    k = 1
            if k == 0:
                print("连续5次异常记录为故障")
                try:  # 将传感器存在且异常记录到信息表中的故障
                    cursor.execute(sqlupdate_interface % ('broke', 0, sensor))
                    cursor.execute(sqlupdate_device_broke % (1, sensor))
                    db.commit()
                except:
                    db.rollback()
def soild_command(s,s1,s2,s3):
    nowtime = datetime.datetime.now().strftime('%H:%M:%S')
    # db = pymysql.connect("10.0.0.111", "root", "password", "green")
    # db.autocommit(True)
    # cursor = db.cursor()
    lst = []
    cursor.execute(sqlselect_data_soild_address % (s1))
    fet_solid_data1 = cursor.fetchall()
    cursor.execute(sqlselect_data_soild_address % (s2))
    fet_solid_data2 = cursor.fetchall()
    cursor.execute(sqlselect_data_soild_address % (s3))
    fet_solid_data3 = cursor.fetchall()
    cursor.execute(sqlselectdevices_s123 % (s1, s2, s3))
    exist_s123 = cursor.fetchall()
    print('%s区域土壤湿度:'%(s), fet_solid_data1, fet_solid_data2, fet_solid_data3, "传感器是否存在：", exist_s123)
    if exist_s123[0][0] == exist_s123[1][0] == exist_s123[2][0] == 0:  # S1区域3个传感器都不存在记录到状态表（缺失）
        print("%s区域不存在并记录到表" % (s))
        avg1 = 9999999
        try:
            cursor.execute(sqlupdate_interface % ('lost', 0, s))
            db.commit()
        except:
            db.rollback()

    else:
        if fet_solid_data1[0][1] == fet_solid_data2[0][1] == fet_solid_data3[0][1] == 'y':
            print('%s区域传感器测量值全部异常'%(s))
            avg1 = 100000
            cursor.execute(sqlselect_data_solid_y5 % (s1))
            fet_broke_s1 = cursor.fetchall()
            cursor.execute(sqlselect_data_solid_y5 % (s2))
            fet_broke_s2 = cursor.fetchall()
            cursor.execute(sqlselect_data_solid_y5 % (s3))
            fet_broke_s3 = cursor.fetchall()
            k = 0
            print("%s区域传感器最近5次异常记录表：" % (s), fet_broke_s1,"--",fet_broke_s2,"--",fet_broke_s3)
            for row_broke_s1 in fet_broke_s1:
                if row_broke_s1[0] == 'z':
                    k = 1
            for row_broke_s2 in fet_broke_s2:
                if row_broke_s2[0] == 'z':
                    k = 1
            for row_broke_s3 in fet_broke_s3:
                if row_broke_s3[0] == 'z':
                    k = 1
            if k == 0:
                print("%s土壤区域所有传感器全部连续5次异常记录为故障"%(s))
                try:
                    cursor.execute(sqlupdate_device_soil_broke % (1, s1))
                    cursor.execute(sqlupdate_device_soil_broke % (1, s2))
                    cursor.execute(sqlupdate_device_soil_broke % (1, s3))
                    cursor.execute(sqlupdate_interface % ('broke', 0, s))  # 将全部故障记录到状态表（故障）
                    db.commit()
                except:
                    db.rollback()

        else:
            if fet_solid_data1[0][1] == 'z' and exist_s123[0][0] == 1:  # 分别判断s123数据正常异常并记录异常值
                lst.append(fet_solid_data1[0][0])
                print('%s传感器正常'%(s1))
                try:  # 获取到正常值将信息表故障状态置0 恢复正常
                    cursor.execute(sqlupdate_device_soil_broke%(0,s1))
                    db.commit()
                except:
                    db.rollback()
            else:
                if fet_solid_data1[0][1] == 'y' and exist_s123[0][0] == 1:
                    print('%s传感器异常开始判断是否连续5次异常' % (s1))
                    cursor.execute(sqlselect_data_solid_y5 % (s1))
                    fet_broke_s1 = cursor.fetchall()
                    k_s1 = 0
                    print("%d传感器最近5次异常记录表：" % (s1), fet_broke_s1)
                    for row_broke_s1 in fet_broke_s1:
                        if row_broke_s1[0] == 'z':
                            k_s1 = 1
                    if k_s1 == 0:
                        print("%d连续5次异常记录为故障" % (s1))
                        try:  # 将传感器存在且异常记录到信息表中的故障
                            cursor.execute(sqlupdate_device_soil_broke % (1, s1))
                            db.commit()
                        except:
                            db.rollback()
            if fet_solid_data2[0][1] == 'z' and exist_s123[1][0] == 1:
                lst.append(fet_solid_data2[0][0])
                try:  # 获取到正常值将信息表故障状态置0 恢复正常
                    cursor.execute(sqlupdate_device_soil_broke%(0,s2))
                    db.commit()
                except:
                    db.rollback()
                print('%s传感器正常'%(s2))
            else:
                if fet_solid_data2[0][1] == 'y' and exist_s123[1][0] == 1:
                    print('%s传感器异常开始判断是否连续5次异常' % (s2))
                    cursor.execute(sqlselect_data_solid_y5 % (s2))
                    fet_broke_s2 = cursor.fetchall()
                    k_s2 = 0
                    print("%d传感器最近5次异常记录表：" % (s2), fet_broke_s2)
                    for row_broke_s2 in fet_broke_s2:
                        if row_broke_s2[0] == 'z':
                            k_s2 = 1
                    if k_s2 == 0:
                        print("%d连续5次异常记录为故障" % (s2))
                        try:  # 将传感器存在且异常记录到信息表中的故障
                            cursor.execute(sqlupdate_device_soil_broke % (1, s2))
                            db.commit()
                        except:
                            db.rollback()
            if fet_solid_data3[0][1] == 'z' and exist_s123[2][0] == 1:
                lst.append(fet_solid_data3[0][0])
                print('%s传感器正常'%(s3))
                try:  # 获取到正常值将信息表故障状态置0 恢复正常
                    cursor.execute(sqlupdate_device_soil_broke%(0,s3))
                    db.commit()
                except:
                    db.rollback()
            else:
                if fet_solid_data3[0][1] == 'y' and exist_s123[2][0] == 1:
                    print('%s传感器异常开始判断是否连续5次异常' % (s3))
                    cursor.execute(sqlselect_data_solid_y5 % (s3))
                    fet_broke_s3 = cursor.fetchall()
                    k_s3 = 0
                    print("%d传感器最近5次异常记录表：" % (s3), fet_broke_s3)
                    for row_broke_s3 in fet_broke_s3:
                        if row_broke_s3[0] == 'z':
                            k_s3 = 1
                    if k_s3 == 0:
                        print("%d连续5次异常记录为故障" % (s3))
                        try:  # 将传感器存在且异常记录到信息表中的故障
                            cursor.execute(sqlupdate_device_soil_broke % (1, s3))
                            db.commit()
                        except:
                            db.rollback()
            avg1 = round(average(lst), 1)  # 求s123正常传感器均值
            print('%s区域传感器平均值：'%(s), avg1)
            try:  # 将平均值记录到状态表（正常，avg）
                cursor.execute(sqlupdate_interface % ('normal', avg1, s))
                db.commit()
            except:
                db.rollback()
            lst = []

    cursor.execute(sqlselect_command1%(s))
    command1 = cursor.fetchall()
    cursor.execute(sqlselect_command1_time%(s))
    timings = cursor.fetchall()
    cursor.execute(sqlselects1_command1_zdtime%(s))
    zdtime = cursor.fetchall()
    print("%s区域手动模式是否开启："%(s), command1[0][2], "其他模式选择：", command1[0][1])
    if command1[0][1] == 'A':  # 判断进入S1区域模式A
        for row1 in timings:
            print('%s区域设定时间表：' % (s), row1[0], row1[1], '|', row1[2], row1[3], "当前时间：", nowtime)

        if row1[0] < nowtime < row1[1] or row1[2] < nowtime < row1[3]:
            print('%s区域进入定时浇水模式' % (s))
            try:  # 电磁阀S1置1
                cursor.execute(sqlupdate_switch % (1, s))
                db.commit()
            except:
                db.rollback()

        else:
            print('%s区域进入定时等待模式' % (s))
            try:  # 电磁阀S1置0
                cursor.execute(sqlupdate_switch % (0, s))
                db.commit()
            except:
                db.rollback()
    if command1[0][1] == 'B':  # 判断进入S1区域自动模式
        print('%s区域进入自动模式' % (s))
        for rowzd in zdtime:
            print('%s区域自动模式设定时间表：' % (s), rowzd[0], rowzd[1], '|', rowzd[2], rowzd[3], "当前时间：", nowtime)
        try:
            cursor.execute(sqlselect_global)  # 查询全局降雨量风速阈值
            globalyz = cursor.fetchall()
        except:
            db.rollback()
        print("全局阈值(风速，降雨量)：", globalyz[0][0], globalyz[0][1], "命令表土壤湿度阈值：", command1[0][4], command1[0][5])
        if (rowzd[0] < nowtime < rowzd[1] or rowzd[2] < nowtime < rowzd[3]) and wind_speed < globalyz[0][
            0] and rainfall < globalyz[0][1]:

            print("%s区域自动模式在定时区间内并符合阈值条件内" % (s))  # 判断B模式定时区间内&&风速低于阈值&&雨量低于阈值&&土壤湿度低于阈值
            if avg1 < command1[0][5] and command1[0][0] == 0:
                print('%s区域自动模式土壤湿度不够且电磁阀关闭，启动浇水' % (s))
                try:  # S1电磁阀置1
                    cursor.execute(sqlupdate_switch % (1, s))
                    db.commit()
                except:
                    db.rollback()
            elif avg1 > command1[0][4] and command1[0][0] == 1:
                print('%s区域土壤湿度过高且电磁阀正在打开，浇水关闭' % (s))
                try:  # S1电磁阀置0
                    cursor.execute(sqlupdate_switch % (0, s))
                    db.commit()
                except:
                    db.rollback()
            else:
                print('%s区域自动模式进入自由开关状态' % (s))
        else:
            print("%s区域自动模式未到定时时间进入等待模式" % (s))
            try:  # 电磁阀S1置0
                cursor.execute(sqlupdate_switch % (0, s))
                db.commit()
            except:
                db.rollback()
def command_switch():
    db = pymysql.connect("10.0.0.111", "root", "password", "green")
    db.autocommit(True)
    cursor = db.cursor()
    t, i = 0, 0
    last=[]
    while (1):
        try:
            cursor.execute(sqlselect_command1_switch_1)
            area = cursor.fetchall()
        except:
            db.rollback()
        list = []
        for row_area in area:
            list.append(row_area[0])

        n = len(list)
        print("数据库查询浇水区域", area, "需要浇水区域列表：", list,"上一次浇水列表",last)
        if n == 0:  # 浇水列表为空
            try:
                cursor.execute(sqlupdate_command1_switch1_all_0)
                db.commit()
            except:
                db.rollback()
            t = 0
            i=0
        elif n==1:
            try:
                cursor.execute(sqlupdate_command1_switch1_all_0)
                cursor.execute(sqlupdate_command1_switch1 % (1, list[0]))
                db.commit()
            except:
                db.rollback()
            t = 0
            i = 0
        else:
            if len(last)>len(list) and i>(len(list)-1):
                t=0
                i=0
            elif len(last)>=2:
                if last[i] != list[i]:
                    t = 0

            try:
                cursor.execute(sqlupdate_command1_switch1_all_0)
                cursor.execute(sqlupdate_command1_switch1 % (1, list[i]))
                db.commit()
            except:
                db.rollback()
            if t==30:
                try:
                    cursor.execute(sqlupdate_command1_switch1 % (0, list[i]))
                    db.commit()
                except:
                    db.rollback()
                i=i+1
                t=0
            if i==len(list):
                t=0
                i=0
        t = t + 1
        last = []
        for row_area_last in area:
            last.append(row_area_last[0])
        print(" 记录结束浇水列表：",last)

        time.sleep(2)
def select_watersource():
    db = pymysql.connect("10.0.0.111", "root", "password", "green")
    db.autocommit(True)
    cursor = db.cursor()
    while(1):
        cursor.execute(sqlselect_global)
        select_source = cursor.fetchall()
        cursor.execute(sqlselect_data%('water_up'))
        water_up= cursor.fetchall()
        cursor.execute(sqlselect_command1_switch1_on)
        switch1 = cursor.fetchall()
        print("水源选择阈值：",select_source[0][7],"传感器蓄水池水位数据：",water_up)

        if water_up[0][0]>select_source[0][7] and water_up[0][1]=='z':
            print("主阀门选择蓄水池供水")
            try:
                cursor.execute(sqlupdate_command1_reservoir %(1))
                cursor.execute(sqlupdate_command1_tapwater % (0))
                db.commit()
            except:
                db.rollback()
        else:
            print("主阀门选择自来水供水")
            try:
                cursor.execute(sqlupdate_command1_reservoir %(0))
                cursor.execute(sqlupdate_command1_tapwater % (1))
                db.commit()
            except:
                db.rollback()
        time.sleep(3)
def reservoir_supply():
    db = pymysql.connect("10.0.0.111", "root", "password", "green")
    db.autocommit(True)
    cursor = db.cursor()
    while(1):
        cursor.execute(sqlselect_global)
        liquid_global  = cursor.fetchall()           #全局阈值信息
        cursor.execute(sqlselect_data%('water_up'))
        water_up= cursor.fetchall()               #上水位液面数据
        cursor.execute(sqlselect_data%('water_down'))
        water_down = cursor.fetchall()            #下水位液面数据
        cursor.execute(sqlselect_devices%('water_up'))
        devices_water_up = cursor.fetchall()                 #所有设备存在信息
        cursor.execute(sqlselect_devices % ('water_down'))
        devices_water_down = cursor.fetchall()
        print("上液面高度：",water_up,"下液面高度：",water_down,"设备信息存在:",devices_water_up[0][0], devices_water_down[0][0],
              "全局阈值：",liquid_global)
        if devices_water_up[0][0]==1 and devices_water_down[0][0]==1 and water_up[0][1] == water_down[0][1] == 'z':# 上下传感器均存在且正常计算并动作
            if (water_up[0][0] < liquid_global[0][2] and water_down[0][0] > liquid_global[0][4]) or (water_up[0][0] < liquid_global[0][3] and
                water_down[0][0] > liquid_global[0][5]) :   # liquid_global[0][2],liquid_global[0][3]上液面最低，最高警戒值
                print("水泵给蓄水池供水")                    # liquid_global[0][4],liquid_global[0][5]下液面最低，最高警戒值
                cursor.execute(sqlupdate_command1_switch1%(1,11))
                db.commit()
            if water_up[0][0] > liquid_global[0][3] or water_down[0][0] < liquid_global[0][4]:
                print("水泵停止供水")
                cursor.execute(sqlupdate_command1_switch1 % (0, 11))
                db.commit()

        else:
            print("上下液面传感器有异常或不存在暂时关闭供水排水")
            cursor.execute(sqlupdate_command1_switch1 % (0, 11))
            db.commit()


        time.sleep(15)
def light_control():
    db = pymysql.connect("10.0.0.111", "root", "password", "green")
    db.autocommit(True)
    cursor = db.cursor()
    while(1):
        nowtime = datetime.datetime.now().strftime('%H:%M:%S')
        nowtime_week = datetime.datetime.now().weekday()
        try:
            cursor.execute(sqlselect_command1_uvlight_zdtime11)
            light_time_week = cursor.fetchall()
            cursor.execute(sqlselect_command1 % ('uv_light'))
            command1 = cursor.fetchall()
            cursor.execute(sqlselect_command1_time % ('uv_light'))
            light_time = cursor.fetchall()
            light_week = light_time_week[0][0].split(',')
        except:
            db.rollback()

        print("灭菌灯手动模式是否开启：" , command1[0][2], "灭菌灯当前星期：",nowtime_week ,"灭菌灯定时星期：",light_week)
        light_star = 0
        for row_light_week in  light_week:
            if row_light_week[0]==str(nowtime_week):
                light_star=1
        if light_star == 1:  # 判断进入
            for row_light in light_time:
                print('灭菌灯进入定时日期，区域设定时间表：', row_light[0], row_light[1], '|', row_light[2], row_light[3])

            if row_light[0] < nowtime < row_light[1] or row_light[2] < nowtime < row_light[3]:
                print('灭菌灯区域进入定时开启模式')
                try:  # 电磁阀S1置1
                    cursor.execute(sqlupdate_command1_switch1 % (1, 13))
                    db.commit()
                except:
                    db.rollback()

            else:
                print('灭菌灯区域进入定时等待模式')
                try:
                    cursor.execute(sqlupdate_command1_switch1 % (0, 13))
                    db.commit()
                except:
                    db.rollback()
        else:
            print('灭菌灯区域未到指定日期关闭')
            try:
                cursor.execute(sqlupdate_command1_switch1 % (0, 13))
                db.commit()
            except:
                db.rollback()

        time.sleep(20)
def camera_control():
    db = pymysql.connect("10.0.0.111", "root", "password", "green")
    db.autocommit(True)
    cursor = db.cursor()
    while(1):
        cursor.execute(sqlselect_command1_camera_set_max)
        camera_time = cursor.fetchall()
        cursor.execute(sqlupdate_command1_switch1 % (1,14))
        db.commit()
        print("照相机执行照相")
        time.sleep(camera_time[0][0])
def other_sensor_data(sensor,data):
    try:
        cursor.execute(sqlselect_data%(data))
        fet_sensor_data = cursor.fetchall()
        cursor.execute(sqlselect_devices % (sensor))
        exist_sensor = cursor.fetchall()
        print('%s-%s测量结果:'%(sensor,data),fet_sensor_data)
    except:
        db.rollback()
    if exist_sensor[0][0]==0:
        try:
            cursor.execute(sqlupdate_interface % ('lost', 0,data))
            db.commit()
        except:
            db.rollback()
    else:
        if fet_sensor_data[0][1] == 'z':
            value_sensor_data = fet_sensor_data[0][0]
            try:  # 将传感器信息状态变为正常
                cursor.execute(sqlupdate_interface % ('normal',value_sensor_data, data))
                cursor.execute(sqlupdate_device_broke % (0,sensor))
                db.commit()
            except:
                db.rollback()
        else:
            print("%s传感器出现异常开始检查是否连续5次都异常"%(data))
            cursor.execute(sqlselect_data_y5 % (data))
            fet_broke_data = cursor.fetchall()
            k_data= 0
            print("%s传感器最近5次异常记录表：" % (data), fet_broke_data)
            for row_broke_data in fet_broke_data:
                if row_broke_data[0] == 'z':
                    k_data = 1
            if k_data == 0:
                print("连续5次异常记录为故障")
                try:  # 将传感器存在且异常记录到信息表中的故障
                    cursor.execute(sqlupdate_interface % ('broke', 0, data))
                    cursor.execute(sqlupdate_device_broke % (1, sensor))
                    db.commit()
                except:
                    db.rollback()
t1=threading.Thread(target=send_data,name='loop1')
t2=threading.Thread(target=command_switch,name='loop2')
t3=threading.Thread(target=select_watersource,name='loop3')
t4=threading.Thread(target=reservoir_supply,name='loop4')
t5=threading.Thread(target=light_control,name='loop5')
t6=threading.Thread(target=camera_control,name='loop6')
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
while(1):
    print("主程序启动")
    try:
        cursor.execute(sqlselect_data%('wind_speed'))
        fetwind_speed = cursor.fetchall()
        cursor.execute(sqlselect_data%('rainfall'))
        fet_rain = cursor.fetchall()
        cursor.execute(sqlselect_devices % ('wind_speed'))
        exist_wind_speed = cursor.fetchall()
        cursor.execute(sqlselect_devices % ('rainfall'))
        exist_rainfall = cursor.fetchall()
        print('风速测量结果:', fetwind_speed,'降雨量测量结果:',fet_rain,"是否存在",exist_wind_speed,exist_rainfall)
    except:
        db.rollback()
    if exist_wind_speed[0][0]==0:
        try:
            cursor.execute(sqlupdate_interface % ('lost', 0,'wind_speed'))
            db.commit()
        except:
            db.rollback()
    else:
        if fetwind_speed[0][1] == 'z':
            wind_speed = fetwind_speed[0][0]
            try:  # 将传感器信息状态变为正常
                cursor.execute(sqlupdate_interface % ('normal',wind_speed, 'wind_speed'))
                cursor.execute(sqlupdate_device_broke % (0, 'wind_speed'))
                db.commit()
            except:
                db.rollback()
        else:
            wind_speed=0

            cursor.execute(sqlselect_data_y5 % ('wind_speed'))
            fet_broke_wind_speed = cursor.fetchall()
            k_wind_speed = 0
            print("风速传感器最近5次异常记录表：" , fet_broke_wind_speed)
            for row_broke_wind_speed in fet_broke_wind_speed:
                if row_broke_wind_speed[0] == 'z':
                    k_wind_speed = 1
            if k_wind_speed == 0:
                print("连续5次异常记录为故障")
                try:  # 将传感器存在且异常记录到信息表中的故障
                    cursor.execute(sqlupdate_interface % ('broke', 0, 'wind_speed'))
                    cursor.execute(sqlupdate_device_broke % (1, 'wind_speed'))
                    db.commit()
                except:
                    db.rollback()

    if exist_rainfall[0][0]==0:
        try:
            cursor.execute(sqlupdate_interface % ('lost', 0,'rainfall'))
            db.commit()
        except:
            db.rollback()
    else:
        if fet_rain[0][1] == 'z':
            rainfall = fet_rain[0][0]
            try:  # 将传感器信息状态变为正常
                cursor.execute(sqlupdate_interface % ('normal',rainfall,'rainfall'))
                cursor.execute(sqlupdate_device_broke % (0, 'rainfall'))
                db.commit()
            except:
                db.rollback()
        else:
            rainfall=0
            print("风速传感器出现异常开始检查是否5次连续异常")
            cursor.execute(sqlselect_data_y5 % ('rainfall'))
            fet_broke_rainfall = cursor.fetchall()
            k_rainfall = 0
            print("风速传感器最近5次异常记录表：", fet_broke_rainfall)
            for row_broke_rainfall in fet_broke_rainfall:
                if row_broke_rainfall[0] == 'z':
                    k_rainfall = 1
            if k_rainfall == 0:
                print("连续5次异常记录为故障")
                try:  # 将传感器存在且异常记录到信息表中的故障
                    cursor.execute(sqlupdate_interface % ('broke', 0, 'rainfall'))
                    cursor.execute(sqlupdate_device_broke % (1, 'rainfall'))
                    db.commit()
                except:
                    db.rollback()




    other_sensor('wind_direction')
    other_sensor('water_up')
    other_sensor('water_down')
    other_sensor_data('light','light_intensity')
    other_sensor_data('light','humidity')
    other_sensor_data('light', 'temperature')
    other_sensor_data('flow_meter_reservoir', 'flow_meter_reservoir_total')
    other_sensor_data('flow_meter_reservoir', 'flow_meter_reservoir_instant')
    other_sensor_data('flow_meter_tapwater', 'flow_meter_tapwater_total')
    other_sensor_data('flow_meter_tapwater', 'flow_meter_tapwater_instant')
    soild_command('s1', 20, 21, 22)
    soild_command('s2', 23, 24, 25)
    soild_command('s3', 26,27,28)
    soild_command('s4', 29,30,31)
    soild_command('s5',32,33,34)
    soild_command('s6', 35,36,37)

    time.sleep(1)