import socket
def tco_srv():

    # 1. 创建socket
    # SOCK_STREAM表示其为TCP 模式
    sock =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    addr = ("127.0.0.1", 8998)
    # 2. 绑定socket
    sock.bind(addr)

    # 3. 监听访问的socket
    sock.listen()

    while True:
        # 4.接收访问的socket,建立通信链路
        skt,addr = sock.accept()
        # 5, 接收对方发送的内容，500 表示buffer
        msg = skt.recv(500)
        msg =msg.decode()

        print(msg)

        rst =