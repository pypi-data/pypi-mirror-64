import os


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


# Make filepaths relative to settings.
here = os.path.dirname(os.path.abspath(__file__))
pardir = os.path.abspath(os.path.join(here, os.path.pardir))


class AppConfig(object):
    def __init__(self, *args, **kwargs):
        self.app_name = ''
        self.port = 8000
        self.env = 'SOLO'
        self.handlers = []
        self.error_handler = None
        self.app_setting = {}

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
            self.error_handler = config['error_handler']
            del config['error_handler']
        except KeyError:
            pass

        try:
            self.app_setting = config['app_setting']
            del config['app_setting']
        except KeyError:
            pass
