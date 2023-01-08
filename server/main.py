import json
import select
import socket
import struct
import sys
import threading
import time

from PyQt5 import QtWidgets

from server.gui import root

BUFFSIZE = 1024
MAX_LISTEN = 5
threadList = []
cards = [i for i in range(1, 111)]


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.isRun = True

    def endThread(self):
        self.isRun = False

    def openTcpServer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # 绑定服务器地址和端口
            s.setblocking(False)  # 设为非阻塞
            s.bind((self.host, self.port))
            # 启动服务监听
            s.listen(MAX_LISTEN)
            inputs = [s, ]
            outputs = []
            message_dict = {}

            while True:
                if self.isRun == False:  # thread exit flag
                    break
                r_list, w_list, e_list = select.select(inputs, outputs, inputs, 1)
                for sk1_or_conn in r_list:
                    # 每一个连接对象
                    if sk1_or_conn == s:
                        # 表示有新用户来连接
                        conn, address = sk1_or_conn.accept()
                        inputs.append(conn)
                        message_dict[conn] = []
                    else:
                        # 有老用户发消息了
                        try:
                            data_bytes = sk1_or_conn.recv(1024)
                        except Exception as ex:
                            # 如果用户终止连接 (实际上在正常的连接结束中没有作用)
                            inputs.remove(sk1_or_conn)
                        else:
                            data_str = str(data_bytes, encoding='utf-8')
                            if len(data_str)<=0:  # 判断连接是否断开，避免错误
                                inputs.remove(sk1_or_conn)
                            else:
                                message_dict[sk1_or_conn].append(data_str)
                                outputs.append(sk1_or_conn)

                # w_list中仅仅保存了谁给我发过消息
                for conn in w_list:
                    recv_str = message_dict[conn][0]
                    if len(recv_str) <= 0:
                        del message_dict[conn][0]
                        outputs.remove(conn)
                        continue
                    del message_dict[conn][0]
                    recv_json = json.loads(recv_str)
                    try:
                        if recv_json['name'] == 'sendFile':
                            getFile(conn)
                            conn.send(bytes(json.dumps({'message': 'success'}), encoding='utf-8'))
                        else:
                            conn.send(bytes(json.dumps({'message': 'unkown singal'}), encoding='utf-8'))
                    except TypeError:
                        conn.send(bytes(json.dumps({'message': 'TypeError'}), encoding='utf-8'))
                    outputs.remove(conn)

                for sk in e_list:
                    inputs.remove(sk)


def respondServer(conn):
    conn.setblocking(0)
    print("accept")
    with conn:
        while True:
            # 接收请求信息
            data = conn.recv(BUFFSIZE)  # 这是一个阻塞函数
            if len(data) <= 0:
                break
            print('data=%s' % data)
            data = json.loads(data)
            if data['name'] == 'getCid':
                outData = {'cards': 123}
            elif data['name'] == 'sendFile':
                getFile(conn)
                outData = {'message': 'success'}
            # 发送请求数据
            conn.send(json.dumps(outData).encode('utf-8'))


def getFile(conn):  # 传输文件
    conn.setblocking(True)
    conn.send('Hi, Welcome to the server!'.encode('utf-8'))
    while 1:
        # 申请相同大小的空间存放发送过来的文件名与文件大小信息
        fileinfo_size = struct.calcsize('128sl')
        # 接收文件名与文件大小信息
        buf = conn.recv(fileinfo_size)
        # 判断是否接收到文件头信息
        if buf:
            # 获取文件名和文件大小
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.strip(b'\00')
            fn = fn.decode()
            print('file new name is {0}, filesize if {1}'.format(str(fn), filesize))

            recvd_size = 0  # 定义已接收文件的大小
            # 存储在该脚本所在目录下面
            fp = open('../' + str(fn), 'wb')
            print('start receiving...')

            # 将分批次传输的二进制流依次写入到文件
            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print('end receive...')
        # 传输结束断开连接
        break
    conn.setblocking(False)


class MyWindow(QtWidgets.QWidget, root.Ui_Form):  # 修改main_ui.Ui_MainWindow
    def __init__(self):
        super(MyWindow, self).__init__()
        self.isListen = False  # 是否正在监听的判断
        self.listenThread = threading.Thread(target=S.openTcpServer)
        self.setupUi(self)
        self.ini()

    def ini(self):
        self.openButton.clicked.connect(self.startListen)

    def startListen(self):
        if not self.isListen:
            self.stateLable.setText("开始监听")
            self.listenThread = threading.Thread(target=S.openTcpServer)
            self.listenThread.start()
            self.openButton.setText("暂停")
            self.isListen = True
        else:
            self.openButton.setText("正在关闭")
            S.endThread()
            time.sleep(2)
            print(self.listenThread.is_alive())
            self.stateLable.setText("未在监听")
            self.openButton.setText("开始")
            self.isListen = False


if __name__ == "__main__":
    S = Server("localhost", 9001)  # 10.0.4.15
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())
