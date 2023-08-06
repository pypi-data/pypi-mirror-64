import logging
from typing import Optional, Awaitable, Any

import tornado.web
from tornado import httputil

logger = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):
    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    def __init__(self, application: "Application", request: httputil.HTTPServerRequest, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass
