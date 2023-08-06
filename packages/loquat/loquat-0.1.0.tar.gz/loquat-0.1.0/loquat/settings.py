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

default_config = {
    'port': 8000,
    'env': 'SOLO',
    'handlers': [],
    'app_settings': {}
}
