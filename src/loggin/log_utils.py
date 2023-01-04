import logging
from logging.handlers import RotatingFileHandler
from config.utils import get_project_path, FileEnum, LogEnum


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
    return LogInit().main_log(name, channel)


class LogInit:
    def __init__(self):
        # 初始化日志格式
        self.formate = LogEnum.FMT.value
        self.log_formate = logging.Formatter(self.formate)
        # 初始化日志等级
        self.log_level = LogEnum.LOG_LV.value
        self.file_level = LogEnum.FILE_LV.value
        self.out_level = LogEnum.OUT_LV.value

    def main_log(self, name, channel=None):
        """
        日志初始化主函数
        :param name: 日志名称
        :param channel: 打日志的方式
        :return: 返回一个logging对象
        """
        # 创建日志对象
        logger = logging.getLogger(name)
        # 设置日志级别
        logger.setLevel(self.log_level)
        # 判断打日志的方式
        self.mode_log(logger=logger, channel=channel)
        # 返回logging对象
        return logger

    def mode_log(self, logger, channel):
        """
        判断日志渠道
        :param logger: logging对象
        :param channel: 打日志的方式
        :return:
        """
        # channel为空则日志既做写入也做输出
        if channel is None:
            # logging对象加入handle
            logger.addHandler(self.file_log())
            logger.addHandler(self.console_log())
        elif channel == 'w':
            logger.addHandler(self.file_log())
        elif channel == 'r':
            logger.addHandler(self.console_log())
        else:
            logger.error('channel不存在')
            raise ValueError

    def file_log(self):
        """
        日志写入的配置函数
        :return: 返回一个处理好的handle对象
        """
        # 指定日志写入路径
        log_path = get_project_path(FileEnum.LOG_PATH.value)
        file_handle = RotatingFileHandler(log_path, maxBytes=20 * 1024 * 1024, backupCount=10, encoding='UTF-8')
        # 指定日志写入级别
        file_handle.setLevel(self.file_level)
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
        console_handle.setLevel(self.out_level)
        # 指定日志输出格式
        console_handle.setFormatter(self.log_formate)
        return console_handle
