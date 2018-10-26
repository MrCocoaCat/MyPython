import socket

def clientFunc():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    text = "IT cilent message"

    data = text.encode(text)

    addr = ("127.0.0.1",7852)
    sock.sendto(data,addr)

    data.addr = sock.recvfrom(200)

    text = data.encode()

    print(text)

if __name__ == '__main__':
    clientFunc()


