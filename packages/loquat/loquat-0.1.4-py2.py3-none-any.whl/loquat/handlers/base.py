import logging
from typing import Optional, Awaitable, Any, Union

import tornado.web
from tornado import httputil

from middlewares.base import MiddlewareType

logger = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):
    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    def __init__(self, application: "Application", request: httputil.HTTPServerRequest, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)

        # 拷贝一份中间件列表
        self.middleware_list = self.application.middlewares

    def prepare(self) -> Optional[Awaitable[None]]:
        """
        在每个请求的最开始的时候被调用, 在 get/post/等方法之前.
        """
        super().prepare()
        return self._process_middlewares(mw_type=MiddlewareType.BEFORE_REQUEST)

    def on_finish(self) -> None:
        """在一个请求结束后被调用."""
        super().on_finish()
        self._process_middlewares(mw_type=MiddlewareType.FINISHED)

    def finish(self, chunk: Union[str, bytes, dict] = None) -> "Future[None]":
        """完成响应后调用."""
        self._process_middlewares(MiddlewareType.AFTER_RESPONSE, chunk)
        return super().finish(chunk)

    def _process_middlewares(self, mw_type, *args, **kwargs):
        for middleware in self.middleware_list:
            try:
                if middleware.mw_type is mw_type:
                    should_run_method = getattr(middleware, 'should_run', None)
                    if should_run_method and callable(should_run_method):
                        should_run = should_run_method(self, *args, **kwargs)  # 执行中间件的should_run方法
                        if should_run:
                            run_method = getattr(middleware, 'run', None)
                            if run_method and callable(run_method):
                                run_method(self, *args, **kwargs)  # 执行中间件的run方法
            except Exception as e:
                logger.exception(e)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass
