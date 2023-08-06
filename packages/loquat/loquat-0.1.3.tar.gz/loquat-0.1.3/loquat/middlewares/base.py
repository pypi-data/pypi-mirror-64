from abc import ABCMeta, abstractmethod


class MiddlewareType:
    BEFORE_REQUEST = 'BEFORE_REQUEST'  # 在request之前
    AFTER_RESPONSE = 'AFTER_RESPONSE'  # 在response之后
    FINISHED = 'FINISHED'  # 在请求结束之后
    dict = {
        BEFORE_REQUEST: "BEFORE_REQUEST",
        AFTER_RESPONSE: "AFTER_RESPONSE",
        FINISHED: "FINISHED"
    }


class BaseMiddleware(object, metaclass=ABCMeta):

    def __init__(self, mw_order=0, mw_type=MiddlewareType.BEFORE_REQUEST):

        self._mw_order = mw_order
        self._mw_type = mw_type

    @property
    def mw_order(self):
        """middleware的执行顺序，值越小越靠前执行
        """
        return self._mw_order

    @mw_order.setter
    def mw_order(self, value):
        if not isinstance(value, int):
            raise ValueError('value must be an integer!')
        if value < 0:
            raise ValueError('value must bigger than 0!')
        self._mw_order = value

    @property
    def mw_type(self):
        """middleware的类型。有：MiddlewareType.FINISHED, MiddlewareType.AFTER_RESPONSE, MiddlewareType.BEFORE_REQUEST
        """
        return self._mw_type

    @mw_type.setter
    def mw_type(self, value):

        if value not in [MiddlewareType.FINISHED, MiddlewareType.AFTER_RESPONSE, MiddlewareType.BEFORE_REQUEST]:
            raise ValueError(
                'value must in [MiddlewareType.FINISHED, MiddlewareType.AFTER_RESPONSE, MiddlewareType.BEFORE_REQUEST]')

        self._mw_type = value

    @abstractmethod
    def should_run(self, handler, *args, **kwargs) -> bool:
        """
        是否需要运行中间件。True为运行，False为不运行
        @param handler: tornado.web.RequestHandler的子类
        @param args:
        @param kwargs:
        """
        pass

    @abstractmethod
    def run(self, handler, *args, **kwargs) -> None:
        """
        运行中间件
        @param handler: tornado.web.RequestHandler的子类
        @param args:
        @param kwargs:
        """
        pass
