import logging
import yaml
from logging.handlers import RotatingFileHandler
import colorlog
from config.utils import get_project_path, FileEnum, LogEnum, str_operation


def read_conf(index, path=FileEnum.LOG_COF.value):
    """
    读配置文件
    :param index: 配置id
    :param path: 配置文件路径
    :return: 返回读取结果
    """
    with open(get_project_path(path), encoding="utf-8", mode="r") as f:
        value = yaml.load(f, yaml.FullLoader)[index]
    return value


def get_log(name, channel=None):
    """
    初始化日志配置主入口，便于调用写成方法
    :param name: 日志名称
    :param channel: 打日志的方式：
    为空时，日志既写入文件，也输出到控制台；
    传入 ‘w’ 时，日志仅写入文件
    传入 ‘r’ 时，日志仅在控制台打印
    :return: 返回一个logging对象
    """
    if channel is None:
        return LogInit().main_log(name)
    elif channel == 'r' or channel == 'w':
        return LogInit().main_log(name=name, channel=channel)
    else:
        get_log('value_log').error('channel不存在')
        raise ValueError


class LogInit:

    def __init__(self):
        # 初始化日志配置文件(索引为日志id)
        self.data = read_conf(0)
        # 初始化日志格式
        self.formate = self.data[LogEnum.FMT.value]
        # 配置日志颜色
        log_colors_config = self.data[LogEnum.COLOR.value]
        # self.log_formate = logging.Formatter(self.formate)
        self.log_formate = colorlog.ColoredFormatter(self.formate, log_colors=log_colors_config)

    def main_log(self, name, channel=None):
        """
        日志初始化主函数
        :param name: 日志名称
        :param channel: 日志的打印方式
        :return: 返回一个logging对象
        """
        # 创建日志对象
        logger = logging.getLogger(name)
        # 设置日志级别
        logger.setLevel(self.data[LogEnum.LOG_LV.value])
        # 判断打日志的方式
        self.mode_log(logger=logger, channel=channel)
        # 返回logging对象
        return logger

    def mode_log(self, logger, channel):
        """
        判断日志渠道
        :param logger: logging对象
        :param channel: 日志的打印方式
        :return:
        """
        # channel为空则日志既做写入也做输出
        if channel is None:
            # logging对象加入handle
            logger.addHandler(self.file_log(self.data[LogEnum.FILE_COF.value][LogEnum.LOG_PATH.value]))
            logger.addHandler(self.console_log())
        elif channel == 'w':
            logger.addHandler(self.file_log(self.data[LogEnum.FILE_COF.value][LogEnum.LOG_PATH.value]))
        elif channel == 'r':
            logger.addHandler(self.console_log())
        else:
            logger.error('channel不存在')
            raise ValueError

    def file_log(self, path):
        """
        日志写入的配置函数
        :return: 返回一个处理好的handle对象
        """
        # 指定日志写入路径
        log_path = get_project_path(path)
        file_handle = RotatingFileHandler(
            log_path,
            maxBytes=str_operation(self.data[LogEnum.FILE_COF.value][LogEnum.SIZE.value]),
            backupCount=self.data[LogEnum.FILE_COF.value][LogEnum.COUNT.value],
            encoding=self.data[LogEnum.FILE_COF.value][LogEnum.ENCODE.value]
        )
        # 指定日志写入级别
        file_handle.setLevel(self.data[LogEnum.FILE_LV.value])
        # 指定日志写入格式
        file_handle.setFormatter(self.log_formate)
        return file_handle

    def console_log(self):
        """
        日志输出的配置函数
        :return: 返回一个处理好的handle对象
        """
        # 指定日志输出级别
        console_handle = logging.StreamHandler()
        console_handle.setLevel(self.data[LogEnum.OUT_LV.value])
        # 指定日志输出格式
        console_handle.setFormatter(self.log_formate)
        return console_handle
