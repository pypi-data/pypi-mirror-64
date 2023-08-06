import logging
import os
import signal
import time

import tornado.escape
import tornado.ioloop
import tornado.locks
import tornado.web

logger = logging.getLogger(__name__)

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


class Application(tornado.web.Application):
    """Loquat Application"""

    def __init__(self, app_config: AppConfig):
        self.app_config = app_config

        super(Application, self).__init__(app_config.handlers, **app_config.app_settings)

        logger.debug('Inited Loquat Application')


def shutdown_sig_handler(sig, frame):
    """handle shutdown signal"""

    logger.warning('caught signal: %s', sig)

    max_wait_seconds_before_shutdown = 1

    def shutdown():
        logger.info('stopping http server')
        server.stop()

        logger.info('will shutdown in %s seconds...', max_wait_seconds_before_shutdown)
        io_loop = tornado.ioloop.IOLoop.instance()

        deadline = time.time() + max_wait_seconds_before_shutdown

        def stop_loop():
            now = time.time()
            if now < deadline:
                io_loop.add_timeout(now + 1, stop_loop)
            else:
                logger.info('shutdown')
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
    logger.info("%s started on port %s." % (app_config.app_name, app_config.port,))

    signal.signal(signal.SIGTERM, shutdown_sig_handler)
    signal.signal(signal.SIGINT, shutdown_sig_handler)

    tornado.ioloop.IOLoop.instance().start()
