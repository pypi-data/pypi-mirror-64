import tornado.web

from middleware import MiddlewareManager, MiddlewareType
from config import load_config_dir


class Application(tornado.web.Application):
    """Loquat Application"""

    def __init__(self, handlers=None, middlewares=[], transforms=None):

        config = load_config_dir()
        default_host = config['default_host']
        app_settings = config['app_settings']
        _middlewares = config['middleware_classes'] + middlewares

        self.middleware_manager = MiddlewareManager()
        if _middlewares:
            self.middleware_manager.register_all(_middlewares)
            self.middleware_manager.run_middleware_type(MiddlewareType.INIT_APPLICATION, self)

        super(Application, self).__init__(handlers=handlers, default_host=default_host, transforms=transforms,
                                          **app_settings)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)
