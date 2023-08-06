import logging
import signal
import time

import tornado.escape
import tornado.ioloop
import tornado.locks
import tornado.web

logger = logging.getLogger(__name__)


class Application(tornado.web.Application):
    def __init__(self, port=8000, handlers=[], **app_settings):
        super(Application, self).__init__(handlers, **app_settings)

        self._port = port

        logger.debug('Init loquat.Application')

    @property
    def port(self):
        return self._port


def shutdown_sig_handler(sig, frame):
    """
    处理关闭服务的信号
    :param sig:
    :param frame:
    """
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


def _init_default_application():
    from loquat.settings import default_config

    port = default_config['port']
    handlers = default_config['handlers']
    app_settings = default_config['app_settings']

    return Application(port=port, handlers=handlers, **app_settings)


def run(application: Application) -> object:
    global server

    if not application:
        application = _init_default_application()

    server = tornado.httpserver.HTTPServer(application, xheaders=True)
    server.listen(application.port)

    logger.info("Started on port %s." % (application.port,))

    signal.signal(signal.SIGTERM, shutdown_sig_handler)
    signal.signal(signal.SIGINT, shutdown_sig_handler)
    tornado.ioloop.IOLoop.instance().start()
