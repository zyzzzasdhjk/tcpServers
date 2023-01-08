#!coding=utf-8
import json
import socket
import os
import struct

from PyQt5 import QtWidgets
import sys

class Client:
    def __init__(self,host,port):
        self.addr = (host,port)
        self.s = socket.socket()
        self.s.connect(self.addr)


def sendFile(conn, addr, filepath):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((conn, addr))
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


class MyWindow(QtWidgets.QWidget, clientRoot.Ui_Form):  # 修改main_ui.Ui_MainWindow
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.ini_window()

    def ini_window(self):
        self.fileLable.setAcceptDrops(True)
        self.openButton.clicked.connect()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())
