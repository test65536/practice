# 每次插拔USB串口会导致串口不同，先读取串口号，当做参数传给serial.Serial
import os
usb = os.popen('ls /dev/ttyUSB*').read()[:-1]
print('端口为', usb)
