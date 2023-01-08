# 使用socket模拟多线程，使多用户可以同时连接
import socket
import select

sk1 = socket.socket()
sk1.bind(('localhost', 8001))
sk1.listen()

inputs = [sk1, ]
outputs = []
message_dict = {}

while True:
    r_list, w_list, e_list = select.select(inputs, outputs, inputs, 1)
    print('正在监听的socket对象%d' % len(inputs))
    print(r_list)
    for sk1_or_conn in r_list:
        # 每一个连接对象
        if sk1_or_conn == sk1:
            # 表示有新用户来连接
            conn, address = sk1_or_conn.accept()
            inputs.append(conn)
            message_dict[conn] = []
        else:
            # 有老用户发消息了
            try:
                data_bytes = sk1_or_conn.recv(1024)
            except Exception as ex:
                # 如果用户终止连接
                inputs.remove(sk1_or_conn)
            else:
                data_str = str(data_bytes, encoding='utf-8')
                message_dict[sk1_or_conn].append(data_str)
                outputs.append(sk1_or_conn)

    # w_list中仅仅保存了谁给我发过消息
    for conn in w_list:
        recv_str = message_dict[conn][0]
        del message_dict[conn][0]
        conn.sendall(bytes(recv_str + '好', encoding='utf-8'))
        outputs.remove(conn)

    for sk in e_list:
        inputs.remove(sk)
