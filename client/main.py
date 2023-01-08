#!coding=utf-8
import json
import socket
import os
import struct
from gui import root
from PyQt5 import QtWidgets
import sys

C = None  # client类
CisIni = False  # 判断C是否初始化


class Client:
    def __init__(self, host, port):
        self.addr = (host, int(port))
        self.s = socket.socket()
        self.s.connect(self.addr)
        print("success")
        global CisIni
        CisIni = True

    def fileSend(self, filepath):
        sendFile(self.s, filepath)


def sendFile(s, filepath):
    try:
        d = {'name': 'sendFile'}
        s.send(json.dumps(d).encode('utf-8'))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print(s.recv(1024))
    # 需要传输的文件路径
    # 判断是否为文件
    if os.path.isfile(filepath):
        # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
        fileinfo_size = struct.calcsize('128sl')
        # 定义文件头信息，包含文件名和文件大小
        fhead = struct.pack('128sl', os.path.basename(filepath).encode('utf-8'), os.stat(filepath).st_size)
        # 发送文件名称与文件大小
        s.send(fhead)

        # 将传输文件以二进制的形式分多次上传至服务器
        fp = open(filepath, 'rb')
        while 1:
            data = fp.read(1024)
            if not data:
                print('{0} file send over...'.format(os.path.basename(filepath)))
                break
            s.send(data)
        # 关闭当期的套接字对象
        s.close()


class MyWindow(QtWidgets.QWidget, root.Ui_Form):  # 修改main_ui.Ui_MainWindow
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.filepath = ""
        self.ini_window()

    def ini_window(self):
        with open("data/ip.txt", 'r') as f:
            t = f.read()
            if t != "":
                ip, port = t.split(" ")
                self.ipEdit.setText(ip)
                self.portEdit.setText(port)
                f.close()
        self.fileLable.setAcceptDrops(True)
        self.openButton.clicked.connect(self.initIP)
        self.fileButton.clicked.connect(self.fileSend)

    def fileSend(self):
        if CisIni == True:
            print(self.fileLable.toPlainText())
            C.fileSend(self.fileLable.toPlainText())
        else:
            print("未初始化")

    def initIP(self):
        global C
        ip = self.ipEdit.text()
        port = self.portEdit.text()
        print(ip,port)
        C = Client(ip, port)
        with open("data/ip.txt", 'w') as f:
            f.write(ip + " " + port)
            f.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())
