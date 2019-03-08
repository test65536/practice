# 利用shell获取本机的MAC地址，传给变量
import os
MAC = os.popen('sudo ifconfig | grep eth0').read()[-20:-3]
print('MAC为:', MAC)
print('MAC type:', type(MAC))  # str
