import socket, json
from time import ctime

HOST = '127.0.0.1'
PORT = 9001
ADDR = (HOST, PORT)
ENCODING = 'utf-8'
BUFFSIZE = 1024


def tcpClient():
    # 创建客户套接字
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        # 尝试连接服务器
        s.connect(ADDR)
        print('连接服务成功！！')
        # 通信循环
        while True:
            dataDict = {'time': ctime(), 'name': 'sendFile', 'num': 2}
            # 发送数据到服务器
            Data = json.dumps(dataDict)
            s.send(Data.encode(ENCODING))
            print('发送成功！')
            # 接收返回数据
            outData = s.recv(BUFFSIZE)
            print('返回数据信息：{!r}'.format(outData))
            break
        s.close()


if __name__ == '__main__':
    print('服务已启动')
    tcpClient()
