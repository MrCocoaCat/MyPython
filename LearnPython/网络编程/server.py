import socket

def serverFunc():

    # 1. 建立socket
    # socket.AF_INET 使用ipv4 协议族
    # socket.SOCK_DGRAM 使用UDP
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    addr = ("127.0.0.1",7852)
    sock.bind(addr)

    # 等待对方发消息
    # recvfrom 返回值是一个tuple
    # 第一表示数据，后一项表示地址
    # 500 指缓冲区大小
    data,addr=sock.recvfrom(500)
    print(type(data))
    print(data)

    #将byte 数据反编码为str
    text = data.decode()
    print(type(text))
    print(text)

    rsp = "back data "
    # 编码为bytes 格式
    data = rsp.encode()
    sock.sendto(data,addr)

if __name__ == '__main__':

    print("Begin server")
    serverFunc()
    print("Ending server")

