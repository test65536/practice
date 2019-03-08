import serial
import threading
import time
import pymysql
import os
import struct
# import cv2

# 2018.10.16 版本：没有增加判断/dev/ttyUSB0
# 2018.9.15 10:00 7.2 增加单片机开关；拍照成功后写入数据库；新增压力传感器在7.3
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, bytesize=8, timeout=0.15)  # 连接串口1,RS232
# '/dev/ttyAMA3'
db = pymysql.connect("localhost", "root", "password", "green")  # 连接数据库
cursor = db.cursor()  # 使用cursor()方法获取操作游标


class crc16:
    auchCRCHi = [0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, \
                 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, \
                 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, \
                 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, \
                 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, \
                 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, \
                 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, \
                 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, \
                 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, \
                 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, \
                 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, \
                 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, \
                 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, \
                 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, \
                 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, \
                 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, \
                 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, \
                 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, \
                 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, \
                 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, \
                 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, \
                 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, \
                 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, \
                 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, \
                 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, \
                 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40]

    auchCRCLo = [0x00, 0xC0, 0xC1, 0x01, 0xC3, 0x03, 0x02, 0xC2, 0xC6, 0x06, \
                 0x07, 0xC7, 0x05, 0xC5, 0xC4, 0x04, 0xCC, 0x0C, 0x0D, 0xCD, \
                 0x0F, 0xCF, 0xCE, 0x0E, 0x0A, 0xCA, 0xCB, 0x0B, 0xC9, 0x09, \
                 0x08, 0xC8, 0xD8, 0x18, 0x19, 0xD9, 0x1B, 0xDB, 0xDA, 0x1A, \
                 0x1E, 0xDE, 0xDF, 0x1F, 0xDD, 0x1D, 0x1C, 0xDC, 0x14, 0xD4, \
                 0xD5, 0x15, 0xD7, 0x17, 0x16, 0xD6, 0xD2, 0x12, 0x13, 0xD3, \
                 0x11, 0xD1, 0xD0, 0x10, 0xF0, 0x30, 0x31, 0xF1, 0x33, 0xF3, \
                 0xF2, 0x32, 0x36, 0xF6, 0xF7, 0x37, 0xF5, 0x35, 0x34, 0xF4, \
                 0x3C, 0xFC, 0xFD, 0x3D, 0xFF, 0x3F, 0x3E, 0xFE, 0xFA, 0x3A, \
                 0x3B, 0xFB, 0x39, 0xF9, 0xF8, 0x38, 0x28, 0xE8, 0xE9, 0x29, \
                 0xEB, 0x2B, 0x2A, 0xEA, 0xEE, 0x2E, 0x2F, 0xEF, 0x2D, 0xED, \
                 0xEC, 0x2C, 0xE4, 0x24, 0x25, 0xE5, 0x27, 0xE7, 0xE6, 0x26, \
                 0x22, 0xE2, 0xE3, 0x23, 0xE1, 0x21, 0x20, 0xE0, 0xA0, 0x60, \
                 0x61, 0xA1, 0x63, 0xA3, 0xA2, 0x62, 0x66, 0xA6, 0xA7, 0x67, \
                 0xA5, 0x65, 0x64, 0xA4, 0x6C, 0xAC, 0xAD, 0x6D, 0xAF, 0x6F, \
                 0x6E, 0xAE, 0xAA, 0x6A, 0x6B, 0xAB, 0x69, 0xA9, 0xA8, 0x68, \
                 0x78, 0xB8, 0xB9, 0x79, 0xBB, 0x7B, 0x7A, 0xBA, 0xBE, 0x7E, \
                 0x7F, 0xBF, 0x7D, 0xBD, 0xBC, 0x7C, 0xB4, 0x74, 0x75, 0xB5, \
                 0x77, 0xB7, 0xB6, 0x76, 0x72, 0xB2, 0xB3, 0x73, 0xB1, 0x71, \
                 0x70, 0xB0, 0x50, 0x90, 0x91, 0x51, 0x93, 0x53, 0x52, 0x92, \
                 0x96, 0x56, 0x57, 0x97, 0x55, 0x95, 0x94, 0x54, 0x9C, 0x5C, \
                 0x5D, 0x9D, 0x5F, 0x9F, 0x9E, 0x5E, 0x5A, 0x9A, 0x9B, 0x5B, \
                 0x99, 0x59, 0x58, 0x98, 0x88, 0x48, 0x49, 0x89, 0x4B, 0x8B, \
                 0x8A, 0x4A, 0x4E, 0x8E, 0x8F, 0x4F, 0x8D, 0x4D, 0x4C, 0x8C, \
                 0x44, 0x84, 0x85, 0x45, 0x87, 0x47, 0x46, 0x86, 0x82, 0x42, \
                 0x43, 0x83, 0x41, 0x81, 0x80, 0x40]

    def __init__(self):
        pass

    def createcrc(self, array):
        crchi = 0xff
        crclo = 0xff
        for i in range(0, len(array)):
            crcIndex = crchi ^ array[i]
            crchi = crclo ^ self.auchCRCHi[crcIndex]
            crclo = self.auchCRCLo[crcIndex]
        return (crchi << 8 | crclo)

    def createarray(self, array):
        crcvalue = self.createcrc(array)
        array.append(crcvalue >> 8)
        array.append(crcvalue & 0xff)
        return array

    def calcrc(self, array):
        crchi = 0xff
        crclo = 0xff
        lenarray = len(array)
        for i in range(0, lenarray - 2):
            crcIndex = crchi ^ array[i]
            crchi = crclo ^ self.auchCRCHi[crcIndex]
            crclo = self.auchCRCLo[crcIndex]
        if crchi == array[lenarray - 2] and crclo == array[lenarray - 1]:
            return 0
        else:
            return 1


# 风速-03
def f_read_wind_speed():
    read_wind_speed = [0x03, 0x03, 0x00, 0x09, 0x00, 0x01, 0x55, 0xEA]  # 读取风速帧命令
    lock.acquire()
    ser.write(read_wind_speed)
    read_wind_speed_raw = tuple(ser.read(20))  # 读取风速原始数据,读取20字节
    lock.release()
    if len(read_wind_speed_raw) >= 7:
        wind_speed_raw_h = read_wind_speed_raw[3] * 256  # 风速高字节
        wind_speed_raw_l = read_wind_speed_raw[4]  # 风速低字节
        wind_speed_raw = wind_speed_raw_h + wind_speed_raw_l

        received_wind_speed_crc_raw_h = hex(read_wind_speed_raw[5])[2:].upper()
        received_wind_speed_crc_raw_l = hex(read_wind_speed_raw[6])[2:].upper()

        # 接收数据校验
        received_wind_speed_crc = crc16()
        array = [0x03, 0x03, 0x02, read_wind_speed_raw[3],
                 read_wind_speed_raw[4]]

        cal_received_wind_speed_crc_raw = hex(received_wind_speed_crc.createcrc(array)).upper()
        cal_received_crc_h = 0
        cal_received_crc_l = 0
        if len(cal_received_wind_speed_crc_raw) == 5:
            cal_received_crc_h = cal_received_wind_speed_crc_raw[2]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_wind_speed_crc_raw[3:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        elif len(cal_received_wind_speed_crc_raw) == 6:
            cal_received_crc_h = cal_received_wind_speed_crc_raw[2:4]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_wind_speed_crc_raw[4:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        # 判断是否自己计算的校验码与原始校验码相等

        if (cal_received_crc_h == received_wind_speed_crc_raw_h
                and cal_received_crc_l == received_wind_speed_crc_raw_l):  # 判断是否自己计算的校验码
            print("\033[0;34m%s\033[0m" % '接收到的数据校验成功！')
            print("\033[0;34m%s\033[0m" % '风速原始数据:', read_wind_speed_raw)
            print("\033[0;34m%s\033[0m" % '当前风速:%.1f m/s' % (wind_speed_raw*0.1))  # 转化为风速
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 插入数据---------------------------------------------
            print('即将写入数据库...')
            try:
                sqlinsert = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (3, 'wind_speed', t, wind_speed_raw*0.1, 'z')
                db.ping(reconnect=True)
                cursor.execute(sqlinsert)  # 执行插入数据操作
                db.commit()
            except:
                pass
            print('*'*40)
            return 1  # 正确，函数返回1
        else:
            return 0  # 错误，函数返回0
    else:
        return 0  # 错误，函数返回0


# 风向-04
def f_read_wind_direction():
    read_wind_direction = [0x04, 0x03, 0x00, 0x0A, 0x00, 0x01, 0xA4, 0x5D]
    lock.acquire()
    ser.write(read_wind_direction)
    read_wind_direction_raw = tuple(ser.read(20))  # 读取风向原始数据,读取20字节
    lock.release()
    if len(read_wind_direction_raw) >= 7:
        wind_direction_raw_h = read_wind_direction_raw[3] * 256  # 风向高字节
        wind_direction_raw_l = read_wind_direction_raw[4]  # 风向高字节
        wind_direction_raw = wind_direction_raw_h + wind_direction_raw_l
        received_wind_direction_crc_raw_h = hex(read_wind_direction_raw[5])[2:].upper()
        received_wind_direction_crc_raw_l = hex(read_wind_direction_raw[6])[2:].upper()
        # 接收数据校验
        received_wind_direction_crc = crc16()
        array = [0x04, 0x03, 0x02, read_wind_direction_raw[3],
                 read_wind_direction_raw[4]]

        cal_received_wind_direction_crc_raw = hex(received_wind_direction_crc.createcrc(array)).upper()
        cal_received_crc_h = 0
        cal_received_crc_l = 0
        if len(cal_received_wind_direction_crc_raw) == 5:
            cal_received_crc_h = cal_received_wind_direction_crc_raw[2]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_wind_direction_crc_raw[3:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        elif len(cal_received_wind_direction_crc_raw) == 6:
            cal_received_crc_h = cal_received_wind_direction_crc_raw[2:4]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_wind_direction_crc_raw[4:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        # 判断是否自己计算的校验码与原始校验码相等

        if (cal_received_crc_h == received_wind_direction_crc_raw_h
                and cal_received_crc_l == received_wind_direction_crc_raw_l):  # 判断是否自己计算的校验码
            print("\033[0;34m%s\033[0m" % '接收到的数据校验成功！')
            print("\033[0;34m%s\033[0m" % '风向原始数据:', read_wind_direction_raw)
            print("\033[0;34m%s\033[0m" % '当前风向北偏西:%d °(正北为0 °)' % (wind_direction_raw*0.1))  # 转化为风向
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 插入数据---------------------------------------------
            print('即将写入数据库...')
            try:
                sqlinsert = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                4, 'wind_direction', t, wind_direction_raw*0.1, 'z')
                db.ping(reconnect=True)
                cursor.execute(sqlinsert)  # 执行插入数据操作
                db.commit()
            except:
                pass
            print('*'*40)
            return 1  # 正确，函数返回1
        else:
            return 0  # 错误，函数返回0
    else:
        return 0  # 错误，函数返回0


# 降雨量-05
def f_read_rainfall():
    lock.acquire()
    read_rainfall = [0x05, 0x04, 0x00, 0x01, 0x00, 0x01, 0x61, 0x8E]  # 读取降雨量帧命令
    ser.write(read_rainfall)
    lock.release()
    time.sleep(60)
    lock.acquire()
    ser.write(read_rainfall)
    read_rainfall_raw = tuple(ser.read(20))
    lock.release()
    print('降雨量原始值：',read_rainfall_raw)
    if len(read_rainfall_raw) >= 7:
        rainfall_raw_h = read_rainfall_raw[3] * 256  # 降雨量高字节
        rainfall_raw_l = read_rainfall_raw[4]  # 降雨量低字节
        rainfall_raw = rainfall_raw_h + rainfall_raw_l
        received_rainfall_crc_raw_h = hex(read_rainfall_raw[5])[2:].upper()
        received_rainfall_crc_raw_l = hex(read_rainfall_raw[6])[2:].upper()
        print('原始校验码：',received_rainfall_crc_raw_h,received_rainfall_crc_raw_l)
        # 接收数据校验
        received_rainfall_crc = crc16()
        array = [0x05, 0x04, 0x02, read_rainfall_raw[3],
                 read_rainfall_raw[4]]

        cal_received_rainfall_crc_raw = hex(received_rainfall_crc.createcrc(array)).upper()
        cal_received_crc_h = 0
        cal_received_crc_l = 0
        if len(cal_received_rainfall_crc_raw) == 5:
            cal_received_crc_h = cal_received_rainfall_crc_raw[2]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_rainfall_crc_raw[3:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        elif len(cal_received_rainfall_crc_raw) == 6:
            cal_received_crc_h = cal_received_rainfall_crc_raw[2:4]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_rainfall_crc_raw[4:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        print('生成的校验码：',cal_received_crc_h,cal_received_crc_l)
        # 判断是否自己计算的校验码与原始校验码相等
        if (cal_received_crc_h == received_rainfall_crc_raw_h
                and cal_received_crc_l == received_rainfall_crc_raw_l):  # 判断是否自己计算的校验码
            print("\033[0;34m%s\033[0m" % '接收数据校验成功！')
            print("\033[0;34m%s\033[0m" % '降雨量原始数据：', read_rainfall_raw)
            print("\033[0;34m%s\033[0m" % '当前降雨量为: %.1fmm/min' % (rainfall_raw*0.1))  # 小漏斗每动一次0.2mm/采集周期
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 插入数据---------------------------------------------
            print('即将写入数据库...')
            try:
                sqlinsert = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                5, 'rainfall', t, rainfall_raw*0.1, 'z')
                db.ping(reconnect=True)
                cursor.execute(sqlinsert)  # 执行插入数据操作
                db.commit()
            except:
                pass
            print('*'*40)
            return 1  # 正确，函数返回1
        else:
            return 0  # 错误，函数返回0
    else:
        return 0  # 错误，函数返回0


# 湿2B温2B度、光照4B-06
def f_read_humidity_temperature_light():
    read_humidity_temperature_light = [0x06, 0x03, 0x00, 0x00, 0x00, 0x09, 0x84, 0x7B]  # 读空气温度湿度，光照帧命令
    lock.acquire()
    ser.write(read_humidity_temperature_light)
    read_humidity_temperature_light_raw = tuple(ser.read(30))
    lock.release()
    print(len(read_humidity_temperature_light_raw))
    print(read_humidity_temperature_light_raw)
    if len(read_humidity_temperature_light_raw) >= 23:
        humidity = (read_humidity_temperature_light_raw[3] * 256
                    + read_humidity_temperature_light_raw[4])  # 空气湿度10进制

        temperature = (read_humidity_temperature_light_raw[5] * 256
                       + read_humidity_temperature_light_raw[6])  # 空气温度10进制

        light_1 = read_humidity_temperature_light_raw[17] * 16**6  # 光照1字节没有0x
        light_2 = read_humidity_temperature_light_raw[18] * 16**4  # 光照2字节没有0x
        light_3 = read_humidity_temperature_light_raw[19] * 16**2  # 光照3字节没有0x
        light_4 = read_humidity_temperature_light_raw[20]  # 光照4字节没有0x
        light = light_1 + light_2 + light_3 + light_4  # 光照16进制

        received_humidity_temperature_light_crc_raw_h = hex(read_humidity_temperature_light_raw[21])[2:].upper()  # 接收数据的crc高
        received_humidity_temperature_light_crc_raw_l = hex(read_humidity_temperature_light_raw[22])[2:].upper()  # 接收数据的crc低
        # 接收数据校验
        received_humidity_temperature_light_crc = crc16()
        array = [0x06, 0x03, 0x12, read_humidity_temperature_light_raw[3],
                 read_humidity_temperature_light_raw[4], read_humidity_temperature_light_raw[5],
                 read_humidity_temperature_light_raw[6],0x00,0x00,0x00,0x00,
                 0x00,0x00,0x00,0x00,0x00,0x00,read_humidity_temperature_light_raw[17],
                 read_humidity_temperature_light_raw[18],read_humidity_temperature_light_raw[19],
                 read_humidity_temperature_light_raw[20]]
        cal_received_humidity_temperature_light_crc_raw = hex(received_humidity_temperature_light_crc.createcrc(array)).upper()
        cal_received_crc_h = 0
        cal_received_crc_l = 0
        if len(cal_received_humidity_temperature_light_crc_raw) == 5:
            cal_received_crc_h = cal_received_humidity_temperature_light_crc_raw[2]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_humidity_temperature_light_crc_raw[3:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        elif len(cal_received_humidity_temperature_light_crc_raw) == 6:
            cal_received_crc_h = cal_received_humidity_temperature_light_crc_raw[2:4]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_humidity_temperature_light_crc_raw[4:]  # 计算接收数据crc校验低位，原始c
        # 判断是否自己计算的校验码与原始校验码相等

        if (cal_received_crc_h == received_humidity_temperature_light_crc_raw_h
                and cal_received_crc_l == received_humidity_temperature_light_crc_raw_l):  # 判断是否自己计算的校验码
            print("\033[0;34m%s\033[0m" % '接收数据校验成功！')
            print("\033[0;34m%s\033[0m" % '湿度、温度、光照原始数据：', read_humidity_temperature_light_raw)
            print("\033[0;34m%s\033[0m" % '空气湿度：%0.1f %%' % (humidity*0.1))
            print("\033[0;34m%s\033[0m" % '空气温度：%0.1f ℃' % (temperature*0.1))
            print("\033[0;34m%s\033[0m" % '光照强度：%d Lux' % light)
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 插入数据---------------------------------------------
            print('即将写入数据库...')
            try:
                sqlinsert1 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                6, 'humidity', t, humidity*0.1, 'z')
                sqlinsert2 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                6, 'temperature', t, temperature * 0.1, 'z')
                sqlinsert3 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                6, 'light_intensity', t, light, 'z')
                db.ping(reconnect=True)
                cursor.execute(sqlinsert1)  # 执行插入humidity数据操作
                db.ping(reconnect=True)
                cursor.execute(sqlinsert2)  # 执行插入temperature数据操作
                db.ping(reconnect=True)
                cursor.execute(sqlinsert3)  # 执行插入light数据操作
                db.commit()
            except:
                pass
            print('*'*40)
            return 1  # 正确，函数返回1
        else:
            return 0  # 错误，函数返回0
    else:
        return 0  # 错误，函数返回0


# 液位上-07
def f_read_water_up():
    read_water_up = [0x07, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x6C]  # 读取液位上帧命令
    lock.acquire()
    ser.write(read_water_up)
    read_water_up_raw = tuple(ser.read(20))  # 读取液位上原始数据,读取20字节
    lock.release()
    if len(read_water_up_raw) >= 7:
        water_up_raw_h = read_water_up_raw[3] * 256  # 风速高字节
        water_up_raw_l = read_water_up_raw[4]  # 风速低字节
        water_up_raw = water_up_raw_h + water_up_raw_l

        received_water_up_crc_raw_h = hex(read_water_up_raw[5])[2:].upper()
        received_water_up_crc_raw_l = hex(read_water_up_raw[6])[2:].upper()

        # 接收数据校验
        received_water_up_crc = crc16()
        array = [0x07, 0x03, 0x02, read_water_up_raw[3],
                 read_water_up_raw[4]]

        cal_received_water_up_crc_raw = hex(received_water_up_crc.createcrc(array)).upper()

        cal_received_crc_h = 0
        cal_received_crc_l = 0
        if len(cal_received_water_up_crc_raw) == 5:
            cal_received_crc_h = cal_received_water_up_crc_raw[2]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_water_up_crc_raw[3:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        elif len(cal_received_water_up_crc_raw) == 6:
            cal_received_crc_h = cal_received_water_up_crc_raw[2:4]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_water_up_crc_raw[4:]  # 计算接收数据crc校验低位，原始crc的低位,字符串

        # 判断是否自己计算的校验码与原始校验码相等

        if (cal_received_crc_h == received_water_up_crc_raw_h
                and cal_received_crc_l == received_water_up_crc_raw_l):  # 判断是否自己计算的校验码
            print("\033[0;34m%s\033[0m" % '接收到的数据校验成功！')
            print("\033[0;34m%s\033[0m" % '液位上原始数据:', read_water_up_raw)
            print("\033[0;34m%s\033[0m" % '当前液位上液位:%.2f m' % (water_up_raw * 5/2000))  # 转化为风速
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 插入数据---------------------------------------------
            print('即将写入数据库...')
            try:
                sqlinsert = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                    7, 'water_up', t, water_up_raw * 5/2000, 'z')
                db.ping(reconnect=True)
                cursor.execute(sqlinsert)  # 执行插入数据操作
                db.commit()
            except:
                pass
            print('*' * 40)
            return 1  # 正确，函数返回1
        else:
            return 0  # 错误，函数返回0
    else:
        return 0  # 错误，函数返回0


# 液位下-08
def f_read_water_down():
    read_water_down = [0x08, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x93]  # 读取液位上帧命令
    lock.acquire()
    ser.write(read_water_down)
    read_water_down_raw = tuple(ser.read(20))  # 读取液位上原始数据,读取20字节
    lock.release()
    print(read_water_down_raw)
    print(len(read_water_down_raw))
    if len(read_water_down_raw) >= 7:
        water_down_raw_h = read_water_down_raw[3] * 256  # 风速高字节
        water_down_raw_l = read_water_down_raw[4]  # 风速低字节
        water_down_raw = water_down_raw_h + water_down_raw_l

        received_water_down_crc_raw_h = hex(read_water_down_raw[5])[2:].upper()
        received_water_down_crc_raw_l = hex(read_water_down_raw[6])[2:].upper()

        # 接收数据校验
        received_water_down_crc = crc16()
        array = [0x08, 0x03, 0x02, read_water_down_raw[3],
                 read_water_down_raw[4]]

        cal_received_water_down_crc_raw = hex(received_water_down_crc.createcrc(array)).upper()
        cal_received_crc_h = 0
        cal_received_crc_l = 0
        if len(cal_received_water_down_crc_raw) == 5:
            cal_received_crc_h = cal_received_water_down_crc_raw[2]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_water_down_crc_raw[3:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        elif len(cal_received_water_down_crc_raw) == 6:
            cal_received_crc_h = cal_received_water_down_crc_raw[2:4]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_water_down_crc_raw[4:]  # 计算接收数据crc校验低位，原始crc的低位,字符串

        # 判断是否自己计算的校验码与原始校验码相等

        if (cal_received_crc_h == received_water_down_crc_raw_h
                and cal_received_crc_l == received_water_down_crc_raw_l):  # 判断是否自己计算的校验码
            print("\033[0;34m%s\033[0m" % '接收到的数据校验成功！')
            print("\033[0;34m%s\033[0m" % '液位下原始数据:', read_water_down_raw)
            print("\033[0;34m%s\033[0m" % '当前液位下液位:%.2f m' % (water_down_raw * 5 / 2000))  # 转化为风速
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 插入数据---------------------------------------------
            print('即将写入数据库...')
            try:
                sqlinsert = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                    8, 'water_down', t, water_down_raw * 5 / 2000, 'z')
                db.ping(reconnect=True)
                cursor.execute(sqlinsert)  # 执行插入数据操作
                db.commit()
            except:
                pass
            print('*' * 40)
            return 1  # 正确，函数返回1
        else:
            return 0  # 错误，函数返回0
    else:
        return 0  # 错误，函数返回0


# 流量计转换函数-09
def bytes2float(bytes):
    embody=bytearray()
    for tempi in range(0,4):
        embody.append(bytes[tempi])
    return struct.unpack("!f",embody)[0]


# 流量计-09蓄水池
def f_read_flow_meter():
    read_flow_meter = [0x09, 0x03, 0x01, 0x00, 0x00, 0x06, 0xC5, 0x7C]  # 读取流量计帧命令
    lock.acquire()
    ser.write(read_flow_meter)
    read_flow_meter_raw = tuple(ser.read(20))  # 读取流量计原始数据,读取20字节
    lock.release()
    if len(read_flow_meter_raw) >= 17:
        flow_meter_total_raw = read_flow_meter_raw[5:7]+read_flow_meter_raw[3:5]
        flow_meter_total = bytes2float(flow_meter_total_raw)
        flow_meter_instant_raw = read_flow_meter_raw[9:11]+read_flow_meter_raw[7:9]
        flow_meter_instant = bytes2float(flow_meter_instant_raw)

        received_flow_meter_crc_raw_h = hex(read_flow_meter_raw[15])[2:].upper()
        received_flow_meter_crc_raw_l = hex(read_flow_meter_raw[16])[2:].upper()

        # 接收数据校验
        received_flow_meter_crc = crc16()
        array = [0x09, 0x03, 0x0C, read_flow_meter_raw[3],read_flow_meter_raw[4],read_flow_meter_raw[5]
            ,read_flow_meter_raw[6],read_flow_meter_raw[7],read_flow_meter_raw[8],read_flow_meter_raw[9]
            , read_flow_meter_raw[10],read_flow_meter_raw[11],read_flow_meter_raw[12],read_flow_meter_raw[13]
            , read_flow_meter_raw[14]]

        cal_received_flow_meter_crc_raw = hex(received_flow_meter_crc.createcrc(array)).upper()
        cal_received_crc_h = 0
        cal_received_crc_l = 0
        if len(cal_received_flow_meter_crc_raw) == 5:
            cal_received_crc_h = cal_received_flow_meter_crc_raw[2]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_flow_meter_crc_raw[3:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        elif len(cal_received_flow_meter_crc_raw) == 6:
            cal_received_crc_h = cal_received_flow_meter_crc_raw[2:4]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_flow_meter_crc_raw[4:]  # 计算接收数据crc校验低位，原始crc的低位,字符串

        # 判断是否自己计算的校验码与原始校验码相等

        if (cal_received_crc_h == received_flow_meter_crc_raw_h
                and cal_received_crc_l == received_flow_meter_crc_raw_l):  # 判断是否自己计算的校验码
            print("\033[0;34m%s\033[0m" % '接收到的数据校验成功！')
            print("\033[0;34m%s\033[0m" % '流量计原始数据:', read_flow_meter_raw)
            print("\033[0;34m%s\033[0m" % '当前流量累计值:%.2f m³' % (flow_meter_total))  # 打印流量累计值
            print("\033[0;34m%s\033[0m" % '当前流量瞬时值:%.2f m³/h' % (flow_meter_instant))  # 打印流量瞬时值
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 插入数据---------------------------------------------
            print('即将写入数据库...')
            try:
                sqlinsert1 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                    9, 'flow_meter_reservoir_total', t, flow_meter_total, 'z')
                sqlinsert2 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                    9, 'flow_meter_reservoir_instant', t, flow_meter_instant, 'z')
                db.ping(reconnect=True)
                cursor.execute(sqlinsert1)  # 执行插入数据操作
                db.ping(reconnect=True)
                cursor.execute(sqlinsert2)  # 执行插入数据操作
                db.commit()
            except:
                pass
            print('*' * 40)
            return 1  # 正确，函数返回1
        else:
            return 0  # 错误，函数返回0
    else:
        return 0  # 错误，函数返回0


# 流量计-10自来水
def f_read_flow_meter1():
    read_flow_meter = [0x0A, 0x03, 0x01, 0x00, 0x00, 0x06, 0xC5, 0x4F]  # 读取流量计帧命令
    lock.acquire()
    ser.write(read_flow_meter)
    read_flow_meter_raw = tuple(ser.read(20))  # 读取流量计原始数据,读取20字节
    lock.release()
    print(read_flow_meter_raw )
    print(len(read_flow_meter_raw ))
    if len(read_flow_meter_raw) >= 17:
        flow_meter_total_raw = read_flow_meter_raw[5:7] + read_flow_meter_raw[3:5]
        flow_meter_total = bytes2float(flow_meter_total_raw)
        flow_meter_instant_raw = read_flow_meter_raw[9:11] + read_flow_meter_raw[7:9]
        flow_meter_instant = bytes2float(flow_meter_instant_raw)

        received_flow_meter_crc_raw_h = hex(read_flow_meter_raw[15])[2:].upper()
        received_flow_meter_crc_raw_l = hex(read_flow_meter_raw[16])[2:].upper()

        # 接收数据校验
        received_flow_meter_crc = crc16()
        array = [0x0A, 0x03, 0x0C, read_flow_meter_raw[3], read_flow_meter_raw[4], read_flow_meter_raw[5]
            , read_flow_meter_raw[6], read_flow_meter_raw[7], read_flow_meter_raw[8], read_flow_meter_raw[9]
            , read_flow_meter_raw[10], read_flow_meter_raw[11], read_flow_meter_raw[12], read_flow_meter_raw[13]
            , read_flow_meter_raw[14]]

        cal_received_flow_meter_crc_raw = hex(received_flow_meter_crc.createcrc(array)).upper()
        cal_received_crc_h = 0
        cal_received_crc_l = 0
        if len(cal_received_flow_meter_crc_raw) == 5:
            cal_received_crc_h = cal_received_flow_meter_crc_raw[2]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_flow_meter_crc_raw[3:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
            print(1,cal_received_crc_h)
            print(2,cal_received_crc_l)
        elif len(cal_received_flow_meter_crc_raw) == 6:
            cal_received_crc_h = cal_received_flow_meter_crc_raw[2:4]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_flow_meter_crc_raw[4:]  # 计算接收数据crc校验低位，原始crc的低位,字符串
            print(1,cal_received_crc_h)
            print(2,cal_received_crc_l)
        # 判断是否自己计算的校验码与原始校验码相等
        print(3,received_flow_meter_crc_raw_h)
        print(4,received_flow_meter_crc_raw_l)
        if (cal_received_crc_h == received_flow_meter_crc_raw_h
                or cal_received_crc_l == received_flow_meter_crc_raw_l):  # 判断是否自己计算的校验码
            print("\033[0;34m%s\033[0m" % '接收到的数据校验成功！')
            print("\033[0;34m%s\033[0m" % '流量计原始数据:', read_flow_meter_raw)
            print("\033[0;34m%s\033[0m" % '当前流量累计值:%.2f m³' % (flow_meter_total))  # 打印流量累计值
            print("\033[0;34m%s\033[0m" % '当前流量瞬时值:%.2f m³/h' % (flow_meter_instant))  # 打印流量瞬时值
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 插入数据---------------------------------------------
            print('即将写入数据库...')
            try:
                sqlinsert1 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                    10, 'flow_meter_tapwater_total', t, flow_meter_total, 'z')
                sqlinsert2 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                    10, 'flow_meter_tapwater_instant', t, flow_meter_instant, 'z')
                db.ping(reconnect=True)
                cursor.execute(sqlinsert1)  # 执行插入数据操作
                db.ping(reconnect=True)
                cursor.execute(sqlinsert2)  # 执行插入数据操作
                db.commit()
            except:
                pass
            print('*' * 40)
            return 1  # 正确，函数返回1
        else:
            return 0  # 错误，函数返回0
    else:
        return 0  # 错误，函数返回0


# 压力传感器11
def f_pressure_sensor():
    read_pressure = [0x0B,0x03,0x00,0x00,0x00,0x01,0x84,0xA0]  # 读取液位上帧命令
    lock.acquire()
    ser.write(read_pressure)
    read_pressure_raw = tuple(ser.read(20))  # 读取液位上原始数据,读取20字节
    lock.release()
    if len(read_pressure_raw) >= 7:
        pressure_raw_h = read_pressure_raw[3] * 256  # 风速高字节
        pressure_raw_l = read_pressure_raw[4]  # 风速低字节
        pressure_raw = pressure_raw_h + pressure_raw_l

        received_pressure_crc_raw_h = hex(read_pressure_raw[5])[2:].upper()
        received_pressure_crc_raw_l = hex(read_pressure_raw[6])[2:].upper()

        # 接收数据校验
        received_pressure_crc = crc16()
        array = [0x0B, 0x03, 0x02, read_pressure_raw[3],
                 read_pressure_raw[4]]

        cal_received_pressure_crc_raw = hex(received_pressure_crc.createcrc(array)).upper()

        cal_received_crc_h = 0
        cal_received_crc_l = 0
        if len(cal_received_pressure_crc_raw) == 5:
            cal_received_crc_h = cal_received_pressure_crc_raw[2]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_pressure_crc_raw[3:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        elif len(cal_received_pressure_crc_raw) == 6:
            cal_received_crc_h = cal_received_pressure_crc_raw[2:4]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_pressure_crc_raw[4:]  # 计算接收数据crc校验低位，原始crc的低位,字符串

        # 判断是否自己计算的校验码与原始校验码相等

        if (cal_received_crc_h == received_pressure_crc_raw_h
                and cal_received_crc_l == received_pressure_crc_raw_l):  # 判断是否自己计算的校验码
            print("\033[0;34m%s\033[0m" % '接收到的数据校验成功！')
            print("\033[0;34m%s\033[0m" % '液位上原始数据:', read_pressure_raw)
            print("\033[0;34m%s\033[0m" % '当前压力:%.2f MPa' % (pressure_raw * 1.6 / 2000))  # 转化为风速
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 插入数据---------------------------------------------
            print('即将写入数据库...')
            try:
                sqlinsert = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                    11, 'pressure', t, pressure_raw * 1.6 / 2000, 'z')
                db.ping(reconnect=True)
                cursor.execute(sqlinsert)  # 执行插入数据操作
                db.commit()
            except:
                pass
            print('*' * 40)
            return 1  # 正确，函数返回1
        else:
            return 0  # 错误，函数返回0
    else:
        return 0  # 错误，函数返回0


# 压力传感器11，用于线程
def f_pressure_sensor_th():
    read_pressure = [0x0B,0x03,0x00,0x00,0x00,0x01,0x84,0xA0]  # 读取压力帧命令
    lock.acquire()
    ser.write(read_pressure)
    read_pressure_raw = tuple(ser.read(20))  # 读取压力原始数据,读取20字节
    lock.release()
    if len(read_pressure_raw) >= 7:
        pressure_raw_h = read_pressure_raw[3] * 256  # 压力高字节
        pressure_raw_l = read_pressure_raw[4]  # 压力低字节
        pressure_raw = pressure_raw_h + pressure_raw_l

        received_pressure_crc_raw_h = hex(read_pressure_raw[5])[2:].upper()
        received_pressure_crc_raw_l = hex(read_pressure_raw[6])[2:].upper()

        # 接收数据校验
        received_pressure_crc = crc16()
        array = [0x0B, 0x03, 0x02, read_pressure_raw[3],
                 read_pressure_raw[4]]

        cal_received_pressure_crc_raw = hex(received_pressure_crc.createcrc(array)).upper()

        cal_received_crc_h = 0
        cal_received_crc_l = 0
        if len(cal_received_pressure_crc_raw) == 5:
            cal_received_crc_h = cal_received_pressure_crc_raw[2]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_pressure_crc_raw[3:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        elif len(cal_received_pressure_crc_raw) == 6:
            cal_received_crc_h = cal_received_pressure_crc_raw[2:4]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_pressure_crc_raw[4:]  # 计算接收数据crc校验低位，原始crc的低位,字符串

        # 判断是否自己计算的校验码与原始校验码相等

        if (cal_received_crc_h == received_pressure_crc_raw_h
                and cal_received_crc_l == received_pressure_crc_raw_l):  # 判断是否自己计算的校验码
            print("\033[0;34m%s\033[0m" % '接收到的数据校验成功！')
            print("\033[0;34m%s\033[0m" % '液位上原始数据:', read_pressure_raw)
            print("\033[0;34m%s\033[0m" % '当前压力:%.2f MPa' % (pressure_raw * 1.6 / 2000))  # 转化为风速
        return pressure_raw * 1.6 / 2000


# 流量计线程-开关用-不写入数据库
def th_read_flow_meter():
    # global flow_meter_instant1
    flow_meter_instant1 = 0
    read_flow_meter = [0x09, 0x03, 0x01, 0x00, 0x00, 0x06, 0xC5, 0x7C]  # 读取流量计帧命令
    lock.acquire()
    ser.write(read_flow_meter)
    read_flow_meter_raw = tuple(ser.read(20))  # 读取流量计原始数据,读取20字节
    lock.release()
    if len(read_flow_meter_raw) >= 17:
        flow_meter_instant_raw = read_flow_meter_raw[9:11] + read_flow_meter_raw[7:9]
        flow_meter_instant1 = bytes2float(flow_meter_instant_raw)

        received_flow_meter_crc_raw_h = hex(read_flow_meter_raw[15])[2:].upper()
        received_flow_meter_crc_raw_l = hex(read_flow_meter_raw[16])[2:].upper()

        # 接收数据校验
        received_flow_meter_crc = crc16()
        array = [0x09, 0x03, 0x0C, read_flow_meter_raw[3], read_flow_meter_raw[4], read_flow_meter_raw[5]
            , read_flow_meter_raw[6], read_flow_meter_raw[7], read_flow_meter_raw[8], read_flow_meter_raw[9]
            , read_flow_meter_raw[10], read_flow_meter_raw[11], read_flow_meter_raw[12], read_flow_meter_raw[13]
            , read_flow_meter_raw[14]]

        cal_received_flow_meter_crc_raw = hex(received_flow_meter_crc.createcrc(array)).upper()
        cal_received_crc_h = 0
        cal_received_crc_l = 0
        if len(cal_received_flow_meter_crc_raw) == 5:
            cal_received_crc_h = cal_received_flow_meter_crc_raw[2]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_flow_meter_crc_raw[3:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        elif len(cal_received_flow_meter_crc_raw) == 6:
            cal_received_crc_h = cal_received_flow_meter_crc_raw[2:4]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_flow_meter_crc_raw[4:]  # 计算接收数据crc校验低位，原始crc的低位,字符串

        # 判断是否自己计算的校验码与原始校验码相等

        if (cal_received_crc_h == received_flow_meter_crc_raw_h
                and cal_received_crc_l == received_flow_meter_crc_raw_l):  # 判断是否自己计算的校验码
            print("\033[0;34m%s\033[0m" % '接收到的数据校验成功！')
            print("\033[0;34m%s\033[0m" % '流量计原始数据:', read_flow_meter_raw)
            print("\033[0;34m%s\033[0m" % '当前流量瞬时值:%.2f m³/h' % flow_meter_instant1)  # 打印流量瞬时值
    return flow_meter_instant1


# 摄像头-10
def camera():
    time_picture = time.strftime("%Y%m%d_%H%M%S", time.localtime())  # 拍照时间 %Y%m%d_%H%M%S
    picture_flags = 1
    print(time_picture)
    picture_flags = os.system("streamer -s 640x480 -o /home/arm/python/picture/" + time_picture + ".jpeg")
    print('picture_flags =',picture_flags)
    if picture_flags == 0:   # 拍照成功标志位
        print('----拍照成功，即将将文件名-%s-写入数据库------！' % time_picture)
        sqlinsert10 = "insert into pictures values(default,'%s')" % (time_picture + '.jpeg')
        db.ping(reconnect=True)
        cursor.execute(sqlinsert10)  # 执行插入数据操作
        #cursor.execute("insert into pictures values(default,'%s')" % (time_picture + '.jpeg'))
        db.commit()
        picture_flags = 1
    else:
        print('拍照失败')

    # try:
    print('图片写入成功-----------------------------------')


# def camera_windows():
#     cap = cv2.VideoCapture(0)
#     # while True:
#     #     # get a frame
#     ret, frame = cap.read()
#     cv2.imshow('img', frame)
#     # time.sleep(0)
#     picture_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
#     cv2.imwrite("./picture/{0}.png".format(picture_time), frame)
#     cap.release()
#     cv2.destroyAllWindows()


# 杀菌灯-11
def uv_light():
    pass


# 读取土壤参数的函数，形参为当前传感器地址20-44
def read_soil(addr):
    # 发送数据校验
    read_soil_crc = crc16()
    array = [addr, 0x03, 0x00, 0x02, 0x00, 0x01]
    read_soil_crc_raw = hex(read_soil_crc.createcrc(array)).upper()
    read_soil_crc_h = 0
    read_soil_crc_l = 0
    if len(read_soil_crc_raw) == 5:
        read_soil_crc_h = read_soil_crc_raw[2]  # 发送crc校验高位，原始crc的低位
        read_soil_crc_l = read_soil_crc_raw[3:]  # 发送crc校验低位，原始crc的高位
    elif len(read_soil_crc_raw) == 6:
        read_soil_crc_h = read_soil_crc_raw[2:4]  # 发送crc校验高位，原始crc的低位
        read_soil_crc_l = read_soil_crc_raw[4:]  # 发送crc校验低位，原始crc的高位
    # 读取土壤温湿度数据
    read_soil_humidity_temperature = [addr, 0x03, 0x00, 0x02, 0x00, 0x01,
                                      int(read_soil_crc_h,16), int(read_soil_crc_l,16)]  # 20号土壤
    lock.acquire()
    ser.write(read_soil_humidity_temperature)
    read_soil_humidity_temperature_raw = tuple(ser.read(20))  # 土壤湿度温度
    lock.release()
    if len(read_soil_humidity_temperature_raw) > 6:  # 判断接受的数据是否正常
        soil_humidity = (read_soil_humidity_temperature_raw[3] * 256
                         + read_soil_humidity_temperature_raw[4])  # 土壤湿度=高字节*256+低字节

        received_soil_crc_raw_h = hex(read_soil_humidity_temperature_raw[5])[2:].upper()  # 接收数据的crc高
        received_soil_crc_raw_l = hex(read_soil_humidity_temperature_raw[6])[2:].upper()  # 接收数据的crc低
        # 接收数据校验
        received_soil_crc = crc16()
        array = [addr, 0x03, 0x02, read_soil_humidity_temperature_raw[3],
                 read_soil_humidity_temperature_raw[4]]

        cal_received_soil_crc_raw = hex(received_soil_crc.createcrc(array)).upper()
        cal_received_crc_h = 0
        cal_received_crc_l = 0
        if len(cal_received_soil_crc_raw) == 5:
            cal_received_crc_h = cal_received_soil_crc_raw[2]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_soil_crc_raw[3:]  # 计算接收数据crc校验低位，原始crc的高位,字符串
        elif len(cal_received_soil_crc_raw) == 6:
            cal_received_crc_h = cal_received_soil_crc_raw[2:4]  # 计算接收数据crc校验高位，原始crc的低位,字符串
            cal_received_crc_l = cal_received_soil_crc_raw[4:]  # 计算接收数据crc校验低位，原始c
        # 判断是否自己计算的校验码与原始校验码相等
        if (cal_received_crc_h == received_soil_crc_raw_h
                and cal_received_crc_l == received_soil_crc_raw_l):  # 判断是否自己计算的校验码
            print("\033[0;34m%s\033[0m" % '接收数据校验成功！')
            print("\033[0;34m%s\033[0m" % '土壤湿度原始数据：', read_soil_humidity_temperature_raw)
            print("\033[0;34m%s\033[0m" % '土壤湿度：%.1f %%RH' % (soil_humidity * 0.1))
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 插入数据---------------------------------------------
            print('即将写入数据库...')
            try:
                sqlinsert1 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                    addr, 'soil_humidity', t, soil_humidity * 0.1, 'z')
                db.ping(reconnect=True)
                cursor.execute(sqlinsert1)  # 执行插入数据操作
                db.commit()
            except:
                pass
            print('*'*40)
            return 1  # 正确，函数返回1
        else:
            return 0  # 错误，函数返回0
    else:
        return 0  # 错误，函数返回0


# 降雨量函数线程05
def th_rainfall():
    j = 0
    while True:
        if j > 3:
            print("\033[0;31m%s\033[0m" % '降雨量传感器异常！')
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 插入数据---------------------------------------------
            print('异常数据即将写入数据库...')
            # try:
            sqlinsert = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
            5, 'rainfall', t, 888, 'y')
            db.ping(reconnect=True)
            cursor.execute(sqlinsert)  # 执行插入数据操作
            db.commit()
            # except:
            #     pass
            print('*' * 40)
            break
        rainfall_flag = f_read_rainfall()  # 调用读降雨量函数
        j = j + 1
        if rainfall_flag == 1:
            print('数据库写入成功')
            break


# 继电器关函数
def switch1(ad,st,cr):
    i = 1
    while True:
        lock.acquire()
        ser.write([0xff, 0xff, ad, st, cr])
        read_relay = tuple(ser.read(20))  # 读取单片机返回值
        lock.release()
        if read_relay == (0xff, 0xff, ad, st, cr):
            print('单片机收到指令！关闭',ad,'号继电器')
            print('*' * 40)
            break
        else:
            i = i + 1
        if i > 3:
            print('电磁阀',ad,'数据异常！')
            break


# 继电器开函数
def switch2(ad,st,cr):
    i = 1
    while i < 3:
        lock.acquire()
        ser.write([0xff, 0xff, ad, st, cr])
        read_relay = tuple(ser.read(20))  # 读取单片机返回值
        lock.release()
        if read_relay == (0xff, 0xff, ad, st, cr):
            print('单片机收到指令！打开', ad, '号继电器')
            print('*'*40)
            break
        else:
            i = i + 1
        if i > 3:
            print('电磁阀', ad, '数据异常！')
            break


# 控制电磁阀开断模块
def water_switch():
    db = pymysql.connect("localhost", "root", "password", "green")  # 连接数据库
    db.autocommit(True)
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    # while True:
    a = time.time()
    try:
        # sleep = 0
        water_reservoir = 0
        water_tapwater = 0
        water_pump_down = 0
        sqlslect8 = "select * from command1"  # 查询电磁阀地址表信息命令
        db.ping(reconnect=True)
        cursor.execute(sqlslect8)
        db.commit()
        water_switch_addr_table = cursor.fetchall()  # 查询电磁阀地址表信息
        water_switch_addr = []  # 需要开的
        water_switch_off_addr = []  # 需要关的
        sd = 0
        # 判断系统模式
        for water_addr in water_switch_addr_table:
            if water_addr[16] == 'Y':
                sd = 1
                # print('进入手动模式！')
                if water_addr[17] == 1:
                    water_switch_addr.append(water_addr[1])
                if water_addr[17] == 0:
                    water_switch_off_addr.append(water_addr[1])
            else:
                if water_addr[3] == 1:
                    water_switch_addr.append(water_addr[1])
                if water_addr[3] == 0:
                    water_switch_off_addr.append(water_addr[1])
        if sd == 1:
            print('进入手动模式！')
        print('需要打开的开关：',water_switch_addr)
        print('需要关闭的开关：',water_switch_off_addr)
        # 关闭水泵开关循环（先关后开避免同时开）
        water_flag = 0
        # 判断总得电磁阀是否关闭
        for water_off_addr in water_switch_off_addr:
            if 81 <= water_off_addr <= 86:
                water_flag += 1
        if water_flag == 6:
            # 关89号蓄水池水泵
            i = 1
            while True:
                lock.acquire()
                ser.write([0xff,0xff,89,00,87])
                read_relay = tuple(ser.read(20))  # 读取单片机返回值
                lock.release()
                if read_relay != (0xff,0xff,89,00,87):
                    i += 1
                else:
                    print('单片机收到指令！关闭89号蓄水池继电器')
                    break
                if i > 3:
                    break
            # 关88号蓄水池继电器
            i = 1
            while True:
                lock.acquire()
                ser.write([0xff, 0xff, 88, 00, 86])
                read_relay = tuple(ser.read(20))  # 读取单片机返回值
                lock.release()
                if read_relay != (0xff, 0xff, 88, 00, 86):
                    i += 1
                else:
                    print('单片机收到指令！关闭88号继电器')
                    break
                if i > 3:
                    break

            # 关90号自来水水源
            i = 1
            while True:
                lock.acquire()
                ser.write([0xff, 0xff, 90, 00, 88])
                read_relay = tuple(ser.read(20))  # 读取单片机返回值
                lock.release()
                if read_relay != (0xff, 0xff, 90, 00, 88):
                    i += 1
                else:
                    print('单片机收到指令！关闭90号自来水水泵')
                    break
                if i > 3:
                    break
            print('关闭总得电磁阀（关掉加压水泵以及水源水泵！）')
        # 关闭电磁阀循环
        for water_off_addr in water_switch_off_addr:
            if water_off_addr == 81:
                switch1(81, 00, 79)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff,0xff,81,00,79])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff,0xff,81,00,79):
                #         i += 1
                #     else:
                #         print('单片机收到指令！关闭81号继电器')
                #         break
                #     if i > 3:
                #         break

            if water_off_addr == 82:
                switch1(82,00,80)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff,0xff,82,00,80])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff,0xff,82,00,80):
                #         i += 1
                #     else:
                #         print('单片机收到指令！关闭82号继电器')
                #         break
                #     if i > 3:
                #         break

            if water_off_addr == 83:
                switch1(83,00,81)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff,0xff,83,00,81])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff,0xff,83,00,81):
                #         i += 1
                #     else:
                #         print('单片机收到指令！关闭83号继电器')
                #         break
                #     if i > 3:
                #         break

            if water_off_addr == 84:
                switch1(84, 00, 82)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff, 0xff, 84, 00, 82])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff, 0xff, 84, 00, 82):
                #         i += 1
                #     else:
                #         print('单片机收到指令！关闭84号继电器')
                #         break
                #     if i > 3:
                #         break

            if water_off_addr == 85:
                switch1(85, 00, 83)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff, 0xff, 85, 00, 83])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff, 0xff, 85, 00, 83):
                #         i += 1
                #     else:
                #         print('单片机收到指令！关闭85号继电器')
                #         break
                #     if i > 3:
                #         break

            if water_off_addr == 86:
                switch1(86, 00, 84)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff, 0xff, 86, 00, 84])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff, 0xff, 86, 00, 84):
                #         i += 1
                #     else:
                #         print('单片机收到指令！关闭86号继电器')
                #         break
                #     if i > 3:
                #         break

            if water_off_addr == 87:
                switch1(87, 00, 85)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff, 0xff, 87, 00, 85])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff, 0xff, 87, 00, 85):
                #         i += 1
                #     else:
                #         print('单片机收到指令！关闭87号继电器')
                #         break
                #     if i > 3:
                #         break

            if water_off_addr == 88:
                switch1(88, 00, 86)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff, 0xff, 88, 00, 86])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff, 0xff, 88, 00, 86):
                #         i += 1
                #     else:
                #         print('单片机收到指令！关闭88号继电器')
                #         break
                #     if i > 3:
                #         break

            if water_off_addr == 91:
                switch1(91, 00, 89)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff, 0xff, 91, 00, 89])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff, 0xff, 91, 00, 89):
                #         i += 1
                #     else:
                #         print('单片机收到指令！关闭91号继电器抽水电磁阀')
                #         break
                #     if i > 3:
                #         break

            if water_off_addr == 92:
                switch1(92, 00, 90)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff, 0xff, 92, 00, 90])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff, 0xff, 92, 00, 90):
                #         i += 1
                #     else:
                #         print('单片机收到指令！关闭92号继电器排水电磁阀')
                #         break
                #     if i > 3:
                #         break

            if water_off_addr == 91 and water_off_addr == 92:
                switch1(95, 00, 93)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff, 0xff, 95, 00, 93])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff, 0xff, 95, 00, 93):
                #         i += 1
                #     else:
                #         print('单片机收到指令！关闭95号继电器抽水水泵')
                #         break
                #     if i > 3:
                #         break

            if water_off_addr == 93:
                switch1(93, 00, 91)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff, 0xff, 93, 00, 91])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff, 0xff, 93, 00, 91):
                #         i += 1
                #     else:
                #         print('单片机收到指令！关闭93号继电器（灭菌灯）')
                #         break
                #     if i > 3:
                #         break
            if water_off_addr == 101:
                switch1(101, 00, 99)
            if water_off_addr == 91:
                switch1(102, 00, 100)

        # 水泵开关开循环
        for water in water_switch_addr:  # 水泵开关循环
            if water == 89:  # 蓄水池模式
                water_reservoir = 1
            if water == 90:  # 自来水模式
                water_tapwater = 1
            # if water == 91 or water == 92:  # 打开下蓄水池水泵
            #     water_pump_down = 1
        # 继电器开循环
        for water1 in water_switch_addr:  # 继电器开循环
            if water1 == 81:
                switch2(81,1,80)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff,0xff,81,1,80])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff,0xff,81,1,80):
                #         i += 1
                #     else:
                #         print('单片机收到指令！打开81号继电器')
                #         break
                #     if i > 3:
                #         break

            if water1 == 82:
                switch2(82,1,81)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff,0xff,82,1,81])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff,0xff,82,1,81):
                #         i += 1
                #     else:
                #         print('单片机收到指令！打开82号继电器')
                #         break
                #     if i > 3:
                #         break

            if water1 == 83:
                switch2(83,1,82)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff,0xff,83,1,82])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff,0xff,83,1,82):
                #         i += 1
                #     else:
                #         print('单片机收到指令！打开83号继电器')
                #         break
                #     if i > 3:
                #         break

            if water1 == 84:
                switch2(84,1,83)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff,0xff,84,1,83])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff,0xff,84,1,83):
                #         i += 1
                #     else:
                #         print('单片机收到指令！打开84号继电器')
                #         break
                #     if i > 3:
                #         break

            if water1 == 85:
                switch2(85,1,84)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff,0xff,85,1,84])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff,0xff,85,1,84):
                #         i += 1
                #     else:
                #         print('单片机收到指令！打开85号继电器')
                #         break
                #     if i > 3:
                #         break

            if water1 == 86:
                switch2(86,1,85)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff,0xff,86,1,85])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff,0xff,86,1,85):
                #         i += 1
                #     else:
                #         print('单片机收到指令！打开86号继电器')
                #         break
                #     if i > 3:
                #         break

            if water1 == 91:
                switch2(91, 1, 90)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff, 0xff, 91, 1, 90])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff, 0xff, 91, 1, 90):
                #         i += 1
                #     else:
                #         print('单片机收到指令！打开91号抽水水泵')
                #         break
                #     if i > 3:
                #         break

            if water1 == 92:
                switch2(92, 1, 91)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff, 0xff, 92, 1, 91])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff, 0xff, 92, 1, 91):
                #         i += 1
                #     else:
                #         print('单片机收到指令！打开92号排水水泵')
                #         break
                #     if i > 3:
                #         break

            if water1 == 93:
                switch2(93, 1, 92)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff, 0xff, 93, 1, 92])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff, 0xff, 93, 1, 92):
                #         i += 1
                #     else:
                #         print('单片机收到指令！打开93号继电器（灭菌灯）')
                #         break
                #     if i > 3:
                #         break

            if water1 == 94:
                print('打开94号，摄像头')
                camera()  # 调用拍照函数
                # camera_windows()
                # print('关闭94号，摄像头，修改数据库')
                update3 = "update command1 set switch1=0 where name = 'camera'"
                update4 = "update command1 set manswitch=0 where name = 'camera'"
                # if sd == 1:  # 手动模式
                db.ping(reconnect=True)
                cursor.execute(update4)
                db.commit()
                print('关闭94号，摄像头，修改数据库')
                # if sd == 0: # 自动模式
                db.ping(reconnect=True)
                cursor.execute(update3)
                db.commit()
                print('关闭94号，摄像头，修改数据库')

            if water1 == 101:
                switch2(101,1,100)

            if water1 == 91:
                switch2(102,1,101)

        # 蓄水池水泵开关条件
        if water_reservoir == 1 and water_flag != 6:
            switch2(88, 1, 87)
            # i = 1
            # while True:
            #     lock.acquire()
            #     ser.write([0xff, 0xff, 88, 1, 87])
            #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
            #     lock.release()
            #     if read_relay != (0xff, 0xff, 88, 1, 87):
            #         i += 1
            #     else:
            #         print('单片机收到指令！打开88号继电器（蓄水池继电器）')
            #         break
            #     if i > 3:
            #         break

            switch2(89, 1, 88)
            # i = 1
            # while True:
            #     lock.acquire()
            #     ser.write([0xff, 0xff, 89, 1, 88])
            #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
            #     lock.release()
            #     if read_relay != (0xff, 0xff, 89, 1, 88):
            #         i += 1
            #     else:
            #         print('单片机收到指令！打开89号继电器（蓄水池水泵）')
            #         break
            #     if i > 3:
            #         break

        # 自来水水泵开关条件
        if water_tapwater == 1 and water_flag != 6:
            switch2(90, 1, 89)
            # i = 1
            # while True:
            #     lock.acquire()
            #     ser.write([0xff, 0xff, 90, 1, 89])
            #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
            #     lock.release()
            #     if read_relay != (0xff, 0xff, 90, 1, 89):
            #         i += 1
            #     else:
            #         print('单片机收到指令！打开90号继电器（自来水）')
            #         break
            #     if i > 3:
            #         break

            print('检测自来水压力，如果压力过小，打开89号继电器（加压水泵）')
            # time.sleep(5)  # 等待水流稳定，测量流速
            # sleep = 1
            pressure_sensor = f_pressure_sensor_th()  # 调用流量计函数，不写入数据库的
            print('压力：',pressure_sensor)
            # 自来水压力过小，打开加压水泵.............（检测的前几次流量不做参考）
            if pressure_sensor <= 0.1:  # 自来水压力过小，打开加压水泵
                pass
                # switch2(89, 1, 88)
                # i = 1
                # while True:
                #     lock.acquire()
                #     ser.write([0xff, 0xff, 89, 1, 88])
                #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
                #     lock.release()
                #     if read_relay != (0xff, 0xff, 89, 1, 88):
                #         i += 1
                #     else:
                #         print('单片机收到指令！打开89号继电器（加压水泵）')
                #         break
                #     if i > 3:
                #         break

        # 抽水水泵开关条件
        if water_pump_down == 1:
            switch2(95, 1, 94)
            # i = 1
            # while True:
            #     lock.acquire()
            #     ser.write([0xff, 0xff, 95, 1, 94])
            #     read_relay = tuple(ser.read(20))  # 读取单片机返回值
            #     lock.release()
            #     if read_relay != (0xff, 0xff, 95, 1, 94):
            #         i += 1
            #     else:
            #         print('单片机收到指令！打开95号继电器（抽水水泵）')
            #         break
            #     if i > 3:
            #         break

        # if sleep == 0:
        time.sleep(0.1)  # 循环读取数据库时间
        b = time.time()
        print('开关运行时间', b - a)
    except:
        pass


def th_sensor():
    global jyl
    # lock.acquire()
    db = pymysql.connect("localhost", "root", "password", "green")  # 连接数据库
    db.autocommit(True)
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    # lock.release()
    # j = 0  # 降雨量次数，标志位
    # while True:
        # try:
    i = 0  # 测量次数
    sqlslect1 = "select * from device"  # 查询传感器地址表信息命令
    db.ping(reconnect=True)
    cursor.execute(sqlslect1)
    db.commit()
    sensor_addr_table = cursor.fetchall()  # 查询传感器地址表信息
    print('传感器原始值：',sensor_addr_table)
    sensor_addr = []
    for sensor_flag in sensor_addr_table:
        if sensor_flag[5] == 1:
            sensor_addr.append(sensor_flag[1])
    print('所有要测量的传感器：',sensor_addr)
    for select_addr in sensor_addr:
        print(select_addr)
        # 调用读取风速函数,并接收函数返回值
        if select_addr == 3:
            while True:
                if i > 3:
                    print("\033[0;31m%s\033[0m" % '风速传感器异常！')
                    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    # 插入数据---------------------------------------------
                    print('异常数据即将写入数据库...')
                    try:
                        sqlinsert = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                            3, 'wind_speed', t, 888, 'y')
                        db.ping(reconnect=True)
                        cursor.execute(sqlinsert)  # 执行插入数据操作
                        db.commit()
                    except:
                        pass
                    print('*' * 40)
                    i = 0
                    break
                wind_speed_flag = f_read_wind_speed()  # 调用读风速函数
                i = i + 1
                if wind_speed_flag == 1:
                    i = 0
                    break

        # 调用读取方向函数,并接收函数返回值
        if select_addr == 4:
            while True:
                if i > 3:
                    print("\033[0;31m%s\033[0m" % '方向传感器异常！')
                    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    # 插入数据---------------------------------------------
                    print('异常数据即将写入数据库...')
                    try:
                        sqlinsert = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                            4, 'wind_direction', t, 888, 'y')
                        db.ping(reconnect=True)
                        cursor.execute(sqlinsert)  # 执行插入数据操作
                        db.commit()
                    except:
                        pass
                    print('*' * 40)
                    i = 0
                    break
                wind_direction_flag = f_read_wind_direction()  # 调用读风向函数
                i = i + 1
                if wind_direction_flag == 1:
                    i = 0
                    break

        # 调用读取降雨量函数,并接收函数返回值
        if select_addr == 5:
            jyl = jyl + 1
            print(jyl)
            if jyl % 2 == 0:
                print('等待1min...')
                thread1 = threading.Thread(target=th_rainfall)  # 建立降雨量线程
                thread1.start()  # 开始降雨量线程，以下代码继续执行，降雨量测量完毕后输出
                time.sleep(1)
                jyl = 0

        # 调用读取光照温湿度函数,并接收函数返回值
        if select_addr == 6:
            while True:
                if i > 3:
                    print("\033[0;31m%s\033[0m" % '光照传感器异常！')
                    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    # 插入数据---------------------------------------------
                    print('异常数据即将写入数据库...')
                    # try:
                    #     sqlinsert1 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                    #         6, 'humidity_t_l', t, 888, 'y')
                    #     db.ping(reconnect=True)
                    #     cursor.execute(sqlinsert1)  # 执行插入humidity数据操作
                    #     db.commit()
                    # except:
                    #     pass
                    try:
                        sqlinsert1 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                            6, 'humidity', t, 888, 'y')
                        sqlinsert2 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                            6, 'temperature', t, 888, 'y')
                        sqlinsert3 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                            6, 'light_intensity', t, 888, 'y')
                        db.ping(reconnect=True)
                        cursor.execute(sqlinsert1)  # 执行插入humidity数据操作
                        db.ping(reconnect=True)
                        cursor.execute(sqlinsert2)  # 执行插入temperature数据操作
                        db.ping(reconnect=True)
                        cursor.execute(sqlinsert3)  # 执行插入light数据操作
                        db.commit()
                    except:
                        pass
                    print('*' * 40)
                    i = 0
                    break
                light_flag = f_read_humidity_temperature_light()  # 调用读光照温湿度函数
                i = i + 1
                if light_flag == 1:
                    i = 0
                    break

        # 调用读取液位上函数,并接收函数返回值
        if select_addr == 7:
            while True:
                if i > 3:
                    print("\033[0;31m%s\033[0m" % '液位上传感器异常！')
                    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    # 插入数据---------------------------------------------
                    print('异常数据即将写入数据库...')
                    try:
                        sqlinsert = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                            7, 'water_up', t, 888, 'y')
                        db.ping(reconnect=True)
                        cursor.execute(sqlinsert)  # 执行插入数据操作
                        db.commit()
                    except:
                        pass
                    print('*' * 40)
                    i = 0
                    break
                water_up_flag = f_read_water_up()  # 调用读液位上函数
                i = i + 1
                if water_up_flag == 1:
                    i = 0
                    break

        # 调用读取液位下函数,并接收函数返回值
        if select_addr == 8:
            while True:
                if i > 3:
                    print("\033[0;31m%s\033[0m" % '液位下传感器异常！')
                    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    # 插入数据---------------------------------------------
                    print('异常数据即将写入数据库...')
                    try:
                        sqlinsert = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                            8, 'water_down', t, 888, 'y')
                        db.ping(reconnect=True)
                        cursor.execute(sqlinsert)  # 执行插入数据操作
                        db.commit()
                    except:
                        pass
                    print('*' * 40)
                    i = 0
                    break
                water_down_flag = f_read_water_down()  # 调用读液位下函数
                i = i + 1
                if water_down_flag == 1:
                    i = 0
                    break

        # 调用读取流量计函数（蓄水池）,并接收函数返回值
        # if select_addr == 9 and threading_flow_meter != 1:
        if select_addr == 9:
            while True:
                if i > 3:
                    print("\033[0;31m%s\033[0m" % '流量计传感器异常！')
                    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    # 插入数据---------------------------------------------
                    print('异常数据即将写入数据库...')
                    try:
                        sqlinsert1 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                            9, 'flow_meter_reservoir_total', t, 888, 'y')
                        sqlinsert2 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                            9, 'flow_meter_reservoir_instant', t, 888, 'y')
                        db.ping(reconnect=True)
                        cursor.execute(sqlinsert1)  # 执行插入数据操作
                        db.ping(reconnect=True)
                        cursor.execute(sqlinsert2)  # 执行插入数据操作
                        db.commit()
                    except:
                        pass
                    print('*' * 40)
                    i = 0
                    break
                flow_meter_flag = f_read_flow_meter()  # 调用读液位上函数
                i = i + 1
                if flow_meter_flag == 1:
                    i = 0
                    break

        # 调用读取流量计函数（自来水）,并接收函数返回值
        if select_addr == 10:
            while True:
                if i > 3:
                    print("\033[0;31m%s\033[0m" % '流量计传感器异常！')
                    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    # 插入数据---------------------------------------------
                    print('异常数据即将写入数据库...')
                    try:
                        sqlinsert1 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                            10, 'flow_meter_tapwater_total', t, 888, 'y')
                        sqlinsert2 = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                            10, 'flow_meter_tapwater_instant', t, 888, 'y')
                        db.ping(reconnect=True)
                        cursor.execute(sqlinsert1)  # 执行插入数据操作
                        db.ping(reconnect=True)
                        cursor.execute(sqlinsert2)  # 执行插入数据操作
                        db.commit()
                    except:
                        pass
                    print('*' * 40)
                    i = 0
                    break
                flow_meter_flag = f_read_flow_meter1()  # 调用读液位上函数
                i = i + 1
                if flow_meter_flag == 1:
                    i = 0
                    break

        if select_addr == 11:
            while True:
                if i > 3:
                    print("\033[0;31m%s\033[0m" % '压力传感器异常！')
                    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    # 插入数据---------------------------------------------
                    print('异常数据即将写入数据库...')
                    try:
                        sqlinsert = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                            11, 'pressure', t, 888, 'y')
                        db.ping(reconnect=True)
                        cursor.execute(sqlinsert)  # 执行插入数据操作
                        db.commit()
                    except:
                        pass
                    print('*' * 40)
                    i = 0
                    break
                pressure_flag = f_pressure_sensor()  # 调用读液位上函数
                i = i + 1
                if pressure_flag == 1:
                    i = 0
                    break

        # 调用读取土壤温湿度函数,并接收函数返回值
        if select_addr >= 20:
            while True:
                ID = select_addr
                soil_flag = read_soil(ID)  # 调用读取土壤温湿度函数,并接收函数返回值
                i = i + 1
                if soil_flag == 1:
                    i = 0
                    break
                elif i >= 3:
                    print("\033[0;31m%s\033[0m" % '%d号土壤传感器异常！' % ID)
                    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    # 插入数据---------------------------------------------
                    print('异常数据即将写入数据库...')
                    try:
                        sqlinsert = "insert into data values(default,'%d','%s','%s','%.1f','%s')" % (
                            ID, 'soil_humidity', t, 888, 'y')
                        db.ping(reconnect=True)
                        cursor.execute(sqlinsert)  # 执行插入数据操作
                        db.commit()
                    except:
                        pass
                    print('*' * 40)
                    i = 0
                    break
        # 更新数据库命令标志位为0
        update1 = "update device set send=0 where address = '%d'" % (select_addr)
        db.ping(reconnect=True)
        cursor.execute(update1)
        db.commit()
        # time.sleep(10)  # 循环读取数据库的时间,要求>1min一测
        # except:
        #     pass


# 主程序
if __name__ == '__main__':
    lock = threading.RLock()
    jyl = 0  # 降雨量次数，标志位
    while True:
        a = time.time()
        water_switch()
        th_sensor()
        b = time.time()
        print('总得开关运行时间', b - a)
    # try:
    # 控制电磁阀开断模块
    # thread0 = threading.Thread(target=water_switch)  # 建立开关线程
    # thread0.start()  # 开始开关线程
    # time.sleep(1)
    # # 传感器测量、传输、储存模块
    # thread4 = threading.Thread(target=th_sensor)  # 建立传感器线程
    # thread4.start()  # 开始传感器线程
    # time.sleep(1)
    # except:
    #     pass

