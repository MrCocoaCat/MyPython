# -*-coding:utf-8-*-
# config.py
# Author: LiYubo

from oslo_config import cfg


CONF = cfg.CONF
# 声明配置项模式
# 单个配置项模式
enabled_apis_opt = cfg.ListOpt('enabled_apis',
                               default=['ec2', 'osapi_compute'],
                               help='List of APIs to enable by default.')

# 注册单个配置项模式
CONF.register_opt(enabled_apis_opt)

test_opt = cfg.IntOpt('mytest',
                      default=1,
                      help='my test')

CONF.register_opt(test_opt)


# 多个配置项组成一个模式
common_opts = [
    cfg.StrOpt('bind_host',
               default='0.0.0.0',
               help='IP address to listen on.'),

    cfg.IntOpt('bind_port',
               default=9292,
               help='Port number to listen on.')
]

# 注册含有多个配置项的模式
CONF.register_opts(common_opts)

# 配置组
rabbit_group = cfg.OptGroup(
    name='rabbit',
    title='RabbitMQ options'
)

# 配置组必须在其组件被注册前注册！
CONF.register_group(rabbit_group)


# 配置组中的模式，通常以配置组的名称为前缀（非必须）
rabbit_ssl_opt = cfg.BoolOpt('use_ssl',
                             default=False,
                             help='use ssl for connection')
# 配置组中的多配置项模式
rabbit_Opts = [
    cfg.StrOpt('host',
               default='localhost',
               help='IP/hostname to listen on.'),
    cfg.IntOpt('port',
               default=5672,
               help='Port number to listen on.')
]


# 注册配置组中含有多个配置项的模式，必须指明配置组
CONF.register_opts(rabbit_Opts, rabbit_group)

# 注册配置组中的单配置项模式，指明配置组
CONF.register_opt(rabbit_ssl_opt, rabbit_group)


# 接下来打印使用配置项的值
if __name__ == "__main__":
    # 调用容器对象，传入要解析的文件（可以多个）
    CONF(default_config_files=['my.conf'])

    for i in cfg.CONF.enabled_apis:
        print("DEFAULT.enabled_apis: " + i)
        print("DEFAULT.bind_host: " + cfg.CONF.bind_host)
        print("DEFAULT.bind_port: " + str(cfg.CONF.bind_port))
        print("rabbit.use_ssl: " + str(cfg.CONF.rabbit.use_ssl))
        print("rabbit.host: " + cfg.CONF.rabbit.host)
        print("rabbit.port: " + str(cfg.CONF.rabbit.port))
        print(cfg.CONF.mytest)
