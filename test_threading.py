import threading
import time
import os
import multiprocessing

lock = threading.Lock()
event = threading.Event()


def th_a():
    lock.acquire()
    addr = 90
    state = 0
    print(hex((addr+state)-0x2))
    print('西北-'*1000)
    lock.release()
    print('aaa',os.getpid())


def th_b():
    lock.acquire()
    time.sleep(3)
    print("i am no.b")
    lock.release()
    event.wait(5)
    print('bbb',os.getpid())


if __name__ == '__main__':
    while True:
        print('i am main----------------')
        th1 = threading.Thread(target=th_a)
        th1.start()
        th2 = multiprocessing.Process(target=th_b)
        th2.start()
        time.sleep(3)
        print('main',os.getppid())