# Loquat

A simple web framework based on Tornado.

## Introduce

Loquat is a web framework based on Tornado.

## Installation

```shell
pip install loquat
```

## Simple uses

```python
from loquat.middleware import BaseMiddleware, MiddlewareType
from loquat.server import Server
from loquat.web import Application

from handler import BaseHandler


class BeforeRequestMW(BaseMiddleware):

    def __init__(self, mw_order=0, mw_type=MiddlewareType.BEFORE_REQUEST):
        super().__init__(mw_order, mw_type)

    def should_run(self, handler, *args, **kwargs) -> bool:
        return True

    def run(self, handler, *args, **kwargs):
        print('run before_request_mw')


class AfterResponseMW(BaseMiddleware):

    def __init__(self, mw_order=0, mw_type=MiddlewareType.AFTER_RESPONSE):
        super().__init__(mw_order, mw_type)

    def should_run(self, handler, *args, **kwargs) -> bool:
        return True

    def run(self, handler, *args, **kwargs):
        print('run after_response_mw')


class IndexHandler(BaseHandler):

    def initialize(self, database):
        self.database = database

    def get(self):
        self.write("hello world!")


class TestApplication(Application):

    def __init__(self, handlers=None, middlewares=None, transforms=None):
        super().__init__(handlers, middlewares, transforms)


def main():
    handlers = [
        (r"/", IndexHandler, dict(database="this is database"))
    ]

    middlewares = [
        BeforeRequestMW,
        AfterResponseMW,
    ]

    application = TestApplication(handlers=handlers, middlewares=middlewares)
    server = Server(application, config={'port': 9000})
    server.start()


if __name__ == "__main__":
    main()

```