import cv2
import time
import numpy

cap = cv2.VideoCapture(0)
# while True:
#     # get a frame
ret, frame = cap.read()
cv2.imshow('img', frame)
# time.sleep(0)
picture_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
cv2.imwrite("./picture/{0}.png".format(picture_time), frame)
cap.release()
cv2.destroyAllWindows()