from oslo_config import cfg
from oslo_config import types
import socket


OPTS = [
    cfg.StrOpt('host',
               default=socket.gethostname(),
               help='name of this node'),
    cfg.IntOpt('collector_workers',
               default=1,
               help='Number of workers for collector service')
]

cfg.CONF.register_opts(OPTS)


if __name__ == '__main__':

    cfg.CONF(default_config_files=['my.conf'])

    a = cfg.CONF.host
    b = cfg.CONF.collector_workers

    print(b)


