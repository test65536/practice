from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QApplication,QGroupBox,QGridLayout,QMessageBox
from PyQt5.QtGui import QPixmap,QFont,QIcon
from PIL import Image
import pymysql
import sys
import threading as td
import time
import psutil#用于检测U盘
import os
class window(QWidget):
    def initUi(self):
        self.if_break = True
        self.db = pymysql.connect('10.0.0.111', 'root', 'password', 'green')
        self.cursor = self.db.cursor()
        sql = "select name from pictures"
        self.cursor.execute(sql)
        self.file_ = self.cursor.fetchall()
        self.file_name = []
        for i in self.file_:
            m = i[0]  # 文件名字
            s = i[0].index('_')  # 日期与时刻划分线索引号
            self.year_ = m[:s - 4]
            montn_ = m[s - 4:s - 2]
            day_ = m[s - 2:s]
            hour = m[s + 1:s + 3]
            minute_ = m[s + 3:s + 5]
            second_ = m[s + 5:s + 7]
            n_name = montn_ + '月' + day_ + '日' + '\n' + hour + ':' + minute_ + ':' + second_
            self.file_name.append(n_name)
        n = len(self.file_name)
        print(n)
        print('全部文件名：\n', self.file_name)
        self.look_file = self.file_name[n - 8:]
        print('当前8个文件：\n', self.look_file)
        self.resize(800,500)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle('照片时间轴')
        self.setWindowIcon(QIcon('image/time_point.png'))
        bg_image = QPixmap('image/bg_time.png')
        bg_l = QLabel(self)
        bg_l.setPixmap(bg_image)
        bg_l.setGeometry(0,0,800,500)

        title_l = QLabel('点击时间点查看当时照片',self)
        title_l.setFont(QFont('楷体',20))
        title_l.setGeometry(200,50,400,50)
        btn_1 = QPushButton(self)
        btn_1.resize(18,18)
        btn_2 = QPushButton(self)
        btn_2.resize(18, 18)
        btn_3 = QPushButton(self)
        btn_3.resize(18, 18)
        btn_4 = QPushButton(self)
        btn_4.resize(18, 18)
        btn_5 = QPushButton(self)
        btn_5.resize(18, 18)
        btn_6 = QPushButton(self)
        btn_6.resize(18, 18)
        btn_7 = QPushButton(self)
        btn_7.resize(18, 18)
        btn_8 = QPushButton(self)
        btn_8.resize(18, 18)
        self.btns = [btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7, btn_8]
        l_1 = QLabel('%s'%(self.look_file[0]), self)
        l_2 = QLabel('%s'%(self.look_file[1]), self)
        l_3 = QLabel('%s'%(self.look_file[2]), self)
        l_4 = QLabel('%s'%(self.look_file[3]), self)
        l_5 = QLabel('%s'%(self.look_file[4]), self)
        l_6 = QLabel('%s'%(self.look_file[5]), self)
        l_7 = QLabel('%s'%(self.look_file[6]), self)
        l_8 = QLabel('%s'%(self.look_file[7]), self)
        self.l_s = [l_1,l_2,l_3,l_4,l_5,l_6,l_7,l_8]
        for i in range(8):
            self.btns[i].move(50+(i*90),195)
        for t in range(8):
            self.l_s[t].move(30+(t*90),220)
        for l in self.l_s:
            l.hide()
        self.time_l_show()
        btn_last = QPushButton('上一页')
        btn_next = QPushButton('下一页')
        btn_exit = QPushButton('退出')
        btn_save = QPushButton('保存照片')
        btn_exit.clicked.connect(self.exit_page)
        btn_last.clicked.connect(self.last_page)
        btn_next.clicked.connect(self.next_page)
        btn_save.clicked.connect(self.save_pics)
        layout_btn = QGridLayout()
        layout_btn.addWidget(btn_last, 0, 0)
        layout_btn.addWidget(btn_next, 0, 1)

        layout_btn.addWidget(btn_save,0,2)
        layout_btn.addWidget(btn_exit, 0, 3)
        group_btn = QGroupBox(self)
        group_btn.setLayout(layout_btn)
        group_btn.setGeometry(200, 350, 400, 100)

        self.do_jobs = [self.chose_pic_1,self.chose_pic_2,self.chose_pic_3,self.chose_pic_4,
                        self.chose_pic_5,self.chose_pic_6,self.chose_pic_7,self.chose_pic_8]
        for i in range(8):
            self.btns[i].clicked.connect(self.do_jobs[i])
        #定时更新照片
        thread_get_pics = td.Thread(target=self.get_the_pics)
        thread_get_pics.start()


        self.show()



    def chose_pic_1(self):
        print('照片时间:\n%s'%(self.l_s[0].text()))
        n = self.file_name.index(self.l_s[0].text())#取出当前要看的照片的索引
        print('选择文件：\n%s'%(self.file_[n][0]))
        pic_name = self.file_[n][0]
        pic = Image.open('D:/PycharmProjects/untitled/picture/%s'%(pic_name))
        m = pic_name.index('.')
        pic_ = pic_name.replace(pic_name[m:],'.png')
        pic.save('pic_change/%s'%(pic_))
        self.the_pic_window = Show_the_pic()
        self.the_pic_window.initUI(self.l_s[0].text(),'pic_change/%s'%(pic_))

    def chose_pic_2(self):
        print('照片时间:\n%s' % (self.l_s[1].text()))
        n = self.file_name.index(self.l_s[1].text())
        print('选择文件：\n%s' % (self.file_[n][0]))
        pic_name = self.file_[n][0]
        pic = Image.open('D:/PycharmProjects/untitled/picture/%s' % (pic_name))
        m = pic_name.index('.')
        pic_ = pic_name.replace(pic_name[m:], '.png')
        pic.save('pic_change/%s' % (pic_))
        self.the_pic_window = Show_the_pic()
        self.the_pic_window.initUI(self.l_s[1].text(), 'pic_change/%s' % (pic_))
    def chose_pic_3(self):
        print('照片时间:\n%s' % (self.l_s[2].text()))
        n = self.file_name.index(self.l_s[2].text())
        print('选择文件：\n%s' % (self.file_[n][0]))
        pic_name = self.file_[n][0]
        pic = Image.open('D:/PycharmProjects/untitled/picture/%s' % (pic_name))
        m = pic_name.index('.')
        pic_ = pic_name.replace(pic_name[m:], '.png')
        pic.save('pic_change/%s' % (pic_))
        self.the_pic_window = Show_the_pic()
        self.the_pic_window.initUI(self.l_s[2].text(), 'pic_change/%s' % (pic_))
    def chose_pic_4(self):
        print('照片时间:\n%s' % (self.l_s[3].text()))
        n = self.file_name.index(self.l_s[3].text())
        print('选择文件：\n%s' % (self.file_[n][0]))
        pic_name = self.file_[n][0]
        pic = Image.open('D:/PycharmProjects/untitled/picture/%s' % (pic_name))
        m = pic_name.index('.')
        pic_ = pic_name.replace(pic_name[m:], '.png')
        pic.save('pic_change/%s' % (pic_))
        self.the_pic_window = Show_the_pic()
        self.the_pic_window.initUI(self.l_s[3].text(), 'pic_change/%s' % (pic_))
    def chose_pic_5(self):
        print('照片时间:\n%s' % (self.l_s[4].text()))
        n = self.file_name.index(self.l_s[4].text())
        print('选择文件：\n%s' % (self.file_[n][0]))
        pic_name = self.file_[n][0]
        pic = Image.open('D:/PycharmProjects/untitled/picture/%s' % (pic_name))
        m = pic_name.index('.')
        pic_ = pic_name.replace(pic_name[m:], '.png')
        pic.save('pic_change/%s' % (pic_))
        self.the_pic_window = Show_the_pic()
        self.the_pic_window.initUI(self.l_s[4].text(), 'pic_change/%s' % (pic_))
    def chose_pic_6(self):
        print('照片时间:\n%s' % (self.l_s[5].text()))
        n = self.file_name.index(self.l_s[5].text())
        print('选择文件：\n%s' % (self.file_[n][0]))
        pic_name = self.file_[n][0]
        pic = Image.open('D:/PycharmProjects/untitled/picture/%s' % (pic_name))
        m = pic_name.index('.')
        pic_ = pic_name.replace(pic_name[m:], '.png')
        pic.save('pic_change/%s' % (pic_))
        self.the_pic_window = Show_the_pic()
        self.the_pic_window.initUI(self.l_s[5].text(), 'pic_change/%s' % (pic_))
    def chose_pic_7(self):
        print('照片时间:\n%s' % (self.l_s[6].text()))
        n = self.file_name.index(self.l_s[6].text())
        print('选择文件：\n%s' % (self.file_[n][0]))
        pic_name = self.file_[n][0]
        pic = Image.open('D:/PycharmProjects/untitled/picture/%s' % (pic_name))
        m = pic_name.index('.')
        pic_ = pic_name.replace(pic_name[m:], '.png')
        pic.save('pic_change/%s' % (pic_))
        self.the_pic_window = Show_the_pic()
        self.the_pic_window.initUI(self.l_s[6].text(), 'pic_change/%s' % (pic_))
    def chose_pic_8(self):
        print('照片时间:\n%s' % (self.l_s[7].text()))
        n = self.file_name.index(self.l_s[7].text())
        print('选择文件：\n%s' % (self.file_[n][0]))
        pic_name = self.file_[n][0]
        pic = Image.open('D:/PycharmProjects/untitled/picture/%s' % (pic_name))
        m = pic_name.index('.')
        pic_ = pic_name.replace(pic_name[m:], '.png')
        pic.save('pic_change/%s' % (pic_))
        self.the_pic_window = Show_the_pic()
        self.the_pic_window.initUI(self.l_s[7].text(), 'pic_change/%s' % (pic_))

    def time_l_show(self):
        for t in self.l_s:
            t.show()
    def last_page(self):

        n = self.file_name.index(self.look_file[0])
        print(n)
        if n >=8:
            print('上一页')
            self.look_file = self.file_name[n - 8:n]
            # print(self.look_file)
            l = len(self.look_file)
            # print('当前文件个数：\n', l)
            m = 0
            for i in self.l_s:
                i.setText('%s' % (self.look_file[m]))
                m += 1
            self.time_l_show()

        elif n == 0:
            print('已是第一页')
            for t in range(len(self.look_file)):
                self.l_s[t].setText('%s'%(self.look_file[t]))
            self.time_l_show()
        else:
            print('上一页不足')
            a = self.look_file
            self.look_file = self.file_name[:n]
            b = 8 - len(self.look_file)
            for i in range(b):
                self.look_file.append(a[i])
            # print('之前文件:\n',a)
            # print('当前文件：\n',self.look_file)
            for t in range(len(self.look_file)):
                self.l_s[t].setText('%s'%(self.look_file[t]))
            self.time_l_show()

    def next_page(self):

        m = len(self.file_name)
        n = self.file_name.index(self.look_file[-1])
        l = m-n-1#下一页剩余个数
        if l >= 8:
            print('下一页')
            self.look_file = self.file_name[n+1:n+9]
            print('当前文件个数',self.look_file)
            for i in range(8):
                self.l_s[i].setText('%s'%(self.look_file[i]))
            self.time_l_show()
        elif l == 1:
            print('已是最新时刻')
            for i in range(8):
                self.l_s[i].setText('%s'%(self.look_file[i]))
            self.time_l_show()

        else:
            print('下一页不足')
            a = self.look_file
            c = self.file_name[n+1:]
            print(m)
            print(n)
            print(len(c))
            print(l)
            self.look_file = a[l:]
            for t in range(l):
                self.look_file.append(c[t])
            # print('当前文件:',self.look_file)
            for i in range(8):
                self.l_s[i].setText('%s'%(self.look_file[i]))
            self.time_l_show()
    def exit_page(self):
        self.if_break = False
        self.close()
    def save_pics(self):
        print('保存照片')
        devices = psutil.disk_partitions()
        flag = 0

        for i in devices:
            if i.opts == 'rw,removable':
                U_path = i.device[:i.device.index('\\')]
                print('存在可移动磁盘：%s' % (U_path))

                if os.path.exists('%s/pics'%(U_path)):#判断该文件夹是否存在，若不存在则创建该文件夹
                    for m, n, pics in os.walk('../picture/'):
                        print(pics)
                        p_n = 0
                        for pic in pics:
                            if pic[pic.index('.'):] == '.png':
                                p_n += 1
                                img = Image.open('../picture/%s' % (pic))
                                img.save('%s/pics/%s' % (U_path, pic))
                                print('%s张照片保存成功！' % (p_n))
                    flag = 1
                    button = QMessageBox.information(self, '照片保存成功', '照片成功保存到可移动磁盘：%s\\pics 目录下！'%(U_path), QMessageBox.Ok, QMessageBox.Ok)
                    if button == QMessageBox.Ok:
                        return
                    else:
                        return
                else:
                    os.mkdir('%s/pics' % (U_path))
                    for m, n, pics in os.walk('../picture/'):
                        print(pics)
                        p_n = 0
                        for pic in pics:
                            if pic[pic.index('.'):] == '.png':
                                p_n += 1
                                img = Image.open('../picture/%s' % (pic))
                                img.save('%s/pics/%s' % (U_path, pic))
                                print('%s张照片保存成功！' % (p_n))
                    flag = 1
                    button = QMessageBox.information(self, '照片保存成功', '照片成功保存到可移动磁盘：%s\\pics 目录下！'%(U_path), QMessageBox.Ok, QMessageBox.Ok)
                    if button == QMessageBox.Ok:
                        return
                    else:
                        return


        if flag == 0:
            print('无可用磁盘')
            button = QMessageBox.warning(self, '无移动磁盘', '未检测到可移动磁盘，请插入U盘！', QMessageBox.Ok, QMessageBox.Ok)
            if button == QMessageBox.Ok:
                return
            else:
                return




    #定时更新照片
    def get_the_pics(self):
        db = pymysql.connect('10.0.0.111', 'root', 'password', 'green')
        db.autocommit(True)
        cursor = db.cursor()
        while self.if_break:
            print('************************定时更新照片**************************')
            sql = "select name from pictures"
            cursor.execute(sql)
            self.file_ = cursor.fetchall()
            self.file_name = []
            for i in self.file_:
                m = i[0]  # 文件名字
                s = i[0].index('_')  # 日期与时刻划分线索引号
                self.year_ = m[:s - 4]
                montn_ = m[s - 4:s - 2]
                day_ = m[s - 2:s]
                hour = m[s + 1:s + 3]
                minute_ = m[s + 3:s + 5]
                second_ = m[s + 5:s + 7]
                n_name = montn_ + '月' + day_ + '日' + '\n' + hour + ':' + minute_ + ':' + second_
                self.file_name.append(n_name)

            n = len(self.file_name)
            print('当前时间:',time.strftime("%Y/%m/%d %X", time.localtime()))
            print('总共文件数:',n)
            print('全部文件名：\n', self.file_name)
            self.look_file = self.file_name[n - 8:]
            print('当前8个文件：\n', self.look_file)
            print('************************定时更新照片**************************')
            time.sleep(2)

class Show_the_pic(QWidget):
    def initUI(self,name,addr):
        self.resize(700,500)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle('%s时的照片'%(name))
        self.setWindowIcon(QIcon('image/time_point.png'))
        pic = QPixmap(addr)
        pic_l = QLabel(self)
        pic_l.setPixmap(pic)
        pic_l.move(30,10)
        self.show()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = window()
    w.initUi()
    sys.exit(app.exec_())