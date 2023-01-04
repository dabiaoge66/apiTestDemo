import os
from enum import Enum


class CaseEnum(Enum):
    """用例文件必要字段的枚举类"""
    # 用例要素
    FEATURE = 'feature'
    STORY = 'story'
    TITLE = 'title'
    REQUESTS = 'requests'
    VALIDATE = 'validate'

    # 请求要素
    METHOD = 'method'
    PATH = 'path'
    HEADER = 'headers'
    PARAMS = 'params'

    # 断言要素
    ACTUAL = 'assert_method'
    COMPARE = 'compare_method'
    EXPECT = 'assert_field'

    # 比较方法
    CODE = 'code'
    IS = 'is'
    NOT = 'not'
    IN = 'in'

    # sql关键字
    SQL = 'sql'
    PRINT = 'sql_print'
    ASSIGNMENT = 'sql_assignment'
    HANDLE = 'sql_handle'


class FileEnum(Enum):
    """必要配置文件的路径枚举类"""
    # 数据库配置文件路径
    DB_CONF = "/data/database_conf.yaml"
    # 接口数据中转文件路径
    EXTRACT = "/extract.yaml"
    # json数据文件路径
    DATA = "/data/data.json"
    # createOrder接口用例文件路径
    CREATE = "/test_case/createOrder.yaml"
    # 用于调试的用例文件路径
    DEBUG = "/test_case/forTest.yaml"
    # 日志文件存放路径
    LOG_PATH = '/logs/log'


class LogEnum(Enum):
    """
    日志配置必要字段的枚举类
    日志等级说明: debug < info < warning < warn < error < exception < critical
    """
    # 日志等级
    LOG_LV = 'INFO'
    # 写入等级
    FILE_LV = 'INFO'
    # 输出等级
    OUT_LV = 'INFO'
    # 日志格式
    FMT = '%(asctime)s -%(name)s -%(levelname)s -%(filename)s -%(levelno)s -%(message)s'


def get_project_path(path):
    """
    获取项目文件路径
    :param path:文件相对路径
    """
    # 项目路径
    project_path = os.path.join(
        os.path.dirname(__file__),
        "..",
    )
    # 返回拼接的路径
    return project_path + path
