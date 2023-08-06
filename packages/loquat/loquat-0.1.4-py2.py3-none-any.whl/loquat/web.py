import tornado.web

from .config import load_config_dir


class Application(tornado.web.Application):
    """Loquat Application"""

    def __init__(self, handlers=None, middlewares=None, transforms=None):

        config = load_config_dir()
        default_host = config['default_host']
        app_settings = config['app_settings']

        if middlewares:
            self._init_middlewares(middlewares)  # 初始化中间件

        super(Application, self).__init__(handlers=handlers, default_host=default_host, transforms=transforms,
                                          **app_settings)

    def _init_middlewares(self, middleware_classes):
        """
        初始化中间件
        """
        self.middlewares = []
        for middleware_cls in middleware_classes:
            middleware_instance = middleware_cls()
            self.middlewares.append(middleware_instance)
        self.middlewares = sorted(self.middlewares, key=lambda m: m.mw_order)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)
