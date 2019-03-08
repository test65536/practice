import cv2
import time
# cap = cv2.VideoCapture("rtsp://admin:adminWLQYRU@10.0.0.102:554")
# ret,frame = cap.read()
# C26364520
while True:
    cap = cv2.VideoCapture("rtsp://admin:adminWLQYRU@10.0.0.102:554")
    ret,frame = cap.read()
    # cv2.imshow("frame",frame)
    take_pic_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    cv2.imwrite("D:/PycharmProjects/untitled/picture/" + take_pic_time+ ".jpg",frame)
    print("123")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(1)
    cv2.destroyAllWindows()
    cap.release()

