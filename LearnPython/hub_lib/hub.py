# -*- coding: UTF-8 -*-



import os



# We don't bother to use cfg.py because monkey patch needs to be
# called very early. Instead, we use an environment variable to
# select the type of hub_lib.
# 获取环境变量，默认为eventlet
HUB_TYPE = os.getenv('RYU_HUB_TYPE', 'eventlet')

if HUB_TYPE == 'eventlet':
    import eventlet
    # HACK:
    # sleep() is the workaround for the following issue.
    # https://github.com/eventlet/eventlet/issues/401
    eventlet.sleep()
    import eventlet.event
    import eventlet.queue
    import eventlet.semaphore
    import eventlet.timeout
    import eventlet.wsgi
    from eventlet import websocket
    import greenlet
    import ssl
    import socket
    import traceback

    getcurrent = eventlet.getcurrent
    # 在全局中为指定的系统模块打补丁，补丁后的模块是“绿色线程友好的”，关键字参数指示哪些模块需要被打补丁，
    patch = eventlet.monkey_patch
    # 暂停当前greenthread，允许其他线程处理
    sleep = eventlet.sleep
    listen = eventlet.listen
    connect = eventlet.connect

    # 类似一个装饰器函数，增加了异常处理功能，装饰eventlet.spawn
    def spawn(*args, **kwargs):
        # **kwargs 为字典类型，删除其‘raise_error ’，如果无键值，则返货False
        raise_error = kwargs.pop('raise_error', False)

        def _launch(func, *args, **kwargs):
            # Mimic gevent's default raise_error=False behaviour
            # by not propagating an exception to the joiner.
            try:
                return func(*args, **kwargs)
            # TaskExit - greenlet.GreenletExit
            except TaskExit:
                pass
            except BaseException as e:
                if raise_error:
                    raise e


        return eventlet.spawn(_launch, *args, **kwargs)

    # 类似一个装饰器函数，增加了异常处理功能，装饰eventlet.spawn_after
    def spawn_after(seconds, *args, **kwargs):
        raise_error = kwargs.pop('raise_error', False)

        def _launch(func, *args, **kwargs):
            # Mimic gevent's default raise_error=False behaviour
            # by not propagating an exception to the joiner.
            try:
                return func(*args, **kwargs)
            except TaskExit:
                pass
            except BaseException as e:
                if raise_error:
                    raise e
                # Log uncaught exception.
                # Note: this is an intentional divergence from gevent
                # behaviour; gevent silently ignores such exceptions.


        return eventlet.spawn_after(seconds, _launch, *args, **kwargs)

    def kill(thread):
        thread.kill()

    # join 列表中的线程
    def joinall(threads):
        for t in threads:
            # This try-except is necessary when killing an inactive
            # greenthread.
            try:
                t.wait()
            # TaskExit 为强制退出异常
            except TaskExit:
                pass

    # http://eventlet.net/doc/modules/semaphore.html
    #
    # This is a variant of Queue that behaves mostly like the standard Stdlib_Queue.
    # It differs by not supporting the task_done or join methods,
    # and is a little faster for not having that overhead.
    # Queue的变体，类似于标准的Stdlib_Queue。
    # 但不支持task_done或join方法，速度更快。
    Queue = eventlet.queue.LightQueue
    # Return True if the queue is empty, False otherwise.
    QueueEmpty = eventlet.queue.Empty
    # An unbounded semaphore.有限信号量
    Semaphore = eventlet.semaphore.Semaphore
    # A bounded semaphore checks to make sure its current value doesn’t exceed its initial value.
    # 有限信号量，即信号量总数不得超过设定值
    BoundedSemaphore = eventlet.semaphore.BoundedSemaphore
    # 强制退出异常
    TaskExit = greenlet.GreenletExit

