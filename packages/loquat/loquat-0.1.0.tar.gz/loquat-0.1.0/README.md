# lettuce

A simple web framework based on Tornado.

## Introduce

Loquat is a web framework based on Tornado.

## Installation

## Simple uses

```python
import loquat
from loquat import web
from loquat.handlers.base import BaseHandler


class IndexHandler(BaseHandler):
    def get(self):
        print(">>>")
        self.render('index.html')


class UntitledApplication(loquat.web.Application):

    def __init__(self):
        handlers = [
            (r"/", IndexHandler)
        ]
        app_settings = {
        }
        super().__init__(port=8000, handlers=handlers, **app_settings)


def main():
    app = UntitledApplication()
    web.run(application=app)

if __name__ == "__main__":
    main()
```