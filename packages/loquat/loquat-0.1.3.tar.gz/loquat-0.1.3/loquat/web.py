import os
import signal
import time

import tornado.escape
import tornado.ioloop
import tornado.locks
import tornado.web

from .log import loquat_logger

# Make filepaths relative to settings.
here = os.path.dirname(os.path.abspath(__file__))
pardir = os.path.abspath(os.path.join(here, os.path.pardir))


class DeploymentType:
    SOLO = "SOLO"  # 也就是本地模式
    DEV = "DEV"  # 开发环境
    QA = "QA"  # 测试环境
    UAT = "UAT"  # 预生产环境
    PROD = "PROD"  # 生产环境
    dict = {
        SOLO: "SOLO",
        DEV: "DEV",
        QA: "QA",
        UAT: "UAT",
        PROD: "PROD"
    }


class AppConfig(object):
    def __init__(self, *args, **kwargs):
        self.app_name = ''
        self.port = 8000
        self.env = 'SOLO'
        self.handlers = []
        self.app_settings = {}
        self.app_properties = {}
        self.middlewares = []

        if kwargs:
            self.set_config(**kwargs)

    def set_config(self, **kwargs):

        config = kwargs.copy()

        try:
            self.app_name = config['app_name']
            del config['app_name']
        except KeyError:
            pass  # Leave what was set or default

        try:
            self.port = config['port']
            del config['port']
        except KeyError:
            pass  # Leave what was set or default

        try:
            self.env = config['env']
            del config['env']
        except KeyError:
            pass

        try:
            self.handlers = config['handlers']
            del config['handlers']
        except KeyError:
            pass

        try:
            self.app_settings = config['app_settings']
            del config['app_settings']
        except KeyError:
            pass

        try:
            app_properties = config['app_properties'] if 'app_properties' in config.keys() else {}
            self.app_properties = {**self.app_properties, **app_properties}
            del config['app_properties']
        except KeyError:
            pass

        try:
            self.middlewares = config['middlewares']
            del config['middlewares']
        except KeyError:
            pass


class Application(tornado.web.Application):
    """Loquat Application"""

    def __init__(self, app_config: AppConfig):

        super(Application, self).__init__(app_config.handlers, **app_config.app_settings)

        self.app_config = app_config  # 赋值app_config

        self._init_middlewares()  # 初始化中间件

        self._init_app_properties()  # 设置application的属性

        loquat_logger.debug('Inited Loquat Application')

    def _init_app_properties(self):
        """
        设置application的属性
        """
        for name in self.app_config.app_properties.keys():
            self.__setattr__(name, self.app_config.app_properties.get(name))

    def _init_middlewares(self):
        """
        初始化中间件
        """
        self.middlewares = []
        for middleware_cls in self.app_config.middlewares:
            middleware_instance = middleware_cls()
            self.middlewares.append(middleware_instance)
        self.middlewares = sorted(self.middlewares, key=lambda m: m.mw_order)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)


def shutdown_sig_handler(sig, frame):
    """handle shutdown signal"""

    loquat_logger.warning('caught signal: %s', sig)

    max_wait_seconds_before_shutdown = 1

    def shutdown():
        loquat_logger.info('stopping http server')
        server.stop()

        loquat_logger.info('will shutdown in %s seconds...', max_wait_seconds_before_shutdown)
        io_loop = tornado.ioloop.IOLoop.instance()

        deadline = time.time() + max_wait_seconds_before_shutdown

        def stop_loop():
            now = time.time()
            if now < deadline:
                io_loop.add_timeout(now + 1, stop_loop)
            else:
                loquat_logger.info('shutdown')
                io_loop.stop()

        stop_loop()

    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def run(app_config: AppConfig):
    """run web application"""

    global server
    if not app_config:
        app_config = AppConfig()

    application = Application(app_config)

    server = tornado.httpserver.HTTPServer(application, xheaders=True)
    server.listen(app_config.port)

    loquat_logger.info("%s started on port %s." % (app_config.app_name, app_config.port,))

    signal.signal(signal.SIGTERM, shutdown_sig_handler)
    signal.signal(signal.SIGINT, shutdown_sig_handler)

    tornado.ioloop.IOLoop.instance().start()
