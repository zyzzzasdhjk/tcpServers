import socket, threading
from time import ctime
import json, random
import time, tkinter as tk

HOST = 'localhost'
PORT = 9001
ADDR = (HOST, PORT)
BUFFSIZE = 1024
MAX_LISTEN = 5
threadList = []
cards = [i for i in range(1, 111)]


def getCid(num):
    global cards
    l = []
    for _ in range(num):
        l.append(cards.pop(random.randint(0, len(cards))))
    return l


def respondServer(s):
    conn, addr = s
    global threadList
    threadList.append(str(addr))
    label1['text'] = '\n'.join(threadList)
    with conn:
        while True:
            # 接收请求信息
            data = conn.recv(BUFFSIZE)  # 这是一个阻塞函数
            if len(data)<=0:
                break
            print('data=%s' % data)
            data = json.loads(data)
            if data['name'] == 'getCid':
                outData = {'cards':getCid(data['num'])}
            # 发送请求数据
            conn.send(json.dumps(outData).encode('utf-8'))
    threadList.remove(str(addr))


def tcpServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 绑定服务器地址和端口
        s.bind(ADDR)
        # 启动服务监听
        s.listen(MAX_LISTEN)
        print('等待用户接入。。。。。。。。。。。。')
        while True:
            # 等待客户端连接请求,获取connSock
            t = threading.Thread(target=respondServer, args=(s.accept(),))
            t.start()


if __name__ == '__main__':
    print('服务已启动')
    root = tk.Tk()  # 生成一个主窗口对象
    userText = tk.StringVar()
    label = tk.Label(root, text='在线')
    label.pack()  # 将标签添加到窗口中
    label1 = tk.Label(root, text=userText)
    label1.pack()
    label1['text'] = 'None'
    tcpThread = threading.Thread(target=tcpServer)
    tcpThread.start()
    root.mainloop()  # 进入消息循环
