import socket
def tcp_srv():

    # 1. 创建socket
    # SOCK_STREAM表示其为TCP 模式
    sock =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    adr = ("127.0.0.1", 8997)
    # 2. 绑定socket
    sock.bind(adr)

    # 3. 监听访问的socket
    sock.listen(5)

    while True:
        print(1)
        # 4.接收访问的socket,建立通信链路
        skt,adr = sock.accept()

        # 5, 接收对方发送的内容，500 表示buffer
        msg = skt.recv(500)
        msg =msg.decode()

        print(msg)

        rst = "this is server,rec from {0}".format(adr)
        # 6. 反馈消息
        skt.send(rst.encode())
        # 关闭连接通路

if __name__ == '__main__':
    tcp_srv()