import oslo_messaging
from oslo_config import cfg
import time

#获取transport对象
transport = oslo_messaging.get_transport(cfg.CONF)

# 消息最终目的信息
# topic 为暴露的接口信息
# server 为指定的特定服务器
target = oslo_messaging.Target(topic='test', server='server1')


# 定义方法
class ServerControlEndpoint(object):
    target = oslo_messaging.Target(namespace='control',
                                   version='2.0')

    def __init__(self, server):
        self.server = server

    def stop(self, ctx):
        if self.server:
            self.server.stop()


# 定义方法
class TestEndport(object):
    def test(self, ctx, arg):
        return arg


# endpoint 包含一组方法
endpoints = [ServerControlEndpoint(None),
             TestEndport(),
             ]

# 创建server对象
server = oslo_messaging.get_rpc_server(transport,
                                       target,
                                       endpoints,
                                       executor='blocking')

try:
    server.start()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("ending server")

server.wait()


