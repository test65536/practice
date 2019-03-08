import time
picture_time = time.strftime("%Y%m%d_%H%M", time.localtime())  # 拍照时间 %Y%m%d_%H%M%S
print(picture_time)
time.sleep(10)
print(picture_time)
