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
    # 日志配置文件路径
    LOG_COF = '/log/log_conf.yaml'


class LogEnum(Enum):
    """
    日志配置必要字段的枚举类
    日志等级说明: debug < info < warning < warn < error < exception < critical
    """
    # 日志等级键名
    LOG_LV = 'log_level'
    # 写入等级键名
    FILE_LV = 'file_level'
    # 输出等级键名
    OUT_LV = 'out_level'
    # 日志格式键名
    FMT = 'formate'
    # 日志写入配置键名
    FILE_COF = 'file_conf'
    # 日志写入路径键名
    LOG_PATH = 'path'
    # 日志写入maxBytes键名
    SIZE = 'size'
    # 日志写入backupCount键名
    COUNT = 'count'
    # 日志写入encoding键名
    ENCODE = 'encoding'
    # 日志打印方式键名
    MODE = 'channel'
    # 日志颜色配置键名
    COLOR = 'color'


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


def str_operation(value_str):
    """
    运算字符串算式的结果
    :param value_str: 字符串形式的算式
    :return: 计算结果
    """
    result = 1
    value_list = value_str.split('*')
    for value in value_list:
        result *= int(value)
    # print(f'运算结果为{result}')
    return result
