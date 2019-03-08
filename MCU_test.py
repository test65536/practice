import serial
ser = serial.Serial('com4', baudrate=9600, bytesize=8, timeout=0.5)
ser.write([0xff,0xff,81,1,80])
read_relay = tuple(ser.read(20))  # 读取单片机返回值
print(read_relay)
i = 1
while True:
    if read_relay != (0xff,0xff,81,1,80):
        i = i + 1
    else:
        print('单片机收到指令！')
        break
    if i > 3:
        print('单片机灭有收到指令！')
        break
