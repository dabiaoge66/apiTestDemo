import json
import time
import jsonpath as jsonpath
import yaml
from config.utils import CaseEnum, get_project_path, FileEnum
from data.database_utils import check_data, OperateDB
from log.log_utils import get_log


class YamlOpt:
    """yaml操作类"""

    def __init__(self):
        pass
        # 日志对象
        self.logger = get_log('yaml_utils.log', 'r')

    def read_yaml(self, file_path=FileEnum.EXTRACT.value, path=None):
        """
        读取数据
        :param file_path: 文件路径
        :param path:json路径表达式
        :return: 表达式为空返回整个对象，不为空，返回表达式下的值
        """
        with open(get_project_path(file_path), encoding="utf-8", mode="r") as f:
            value = yaml.load(f, yaml.FullLoader)
            if path is None:
                return value
            else:
                try:
                    # jsonpath返回的是一个列表，取第一个值返回，方便操作
                    return jsonpath.jsonpath(value, path)[0]
                except TypeError:
                    self.logger.debug(jsonpath.jsonpath(value, path))
                    return jsonpath.jsonpath(value, path)

    def write_yaml(self, data, file_path=FileEnum.EXTRACT.value):
        """
        写入数据(a+:追加)
        :param data:
        :param file_path:
        :return:
        """
        self.logger.debug(f'写入{file_path}')
        with open(get_project_path(file_path), encoding="utf-8", mode="a+") as f:
            yaml.dump([data], stream=f, allow_unicode=True)

    def clear_yaml(self, file_path=FileEnum.EXTRACT.value):
        """
        清空yaml文件
        :param file_path:
        """
        self.logger.debug(f'清空{file_path}')
        with open(get_project_path(file_path), encoding="utf-8", mode="w") as f:
            f.truncate()

    def read_json(self, path, file_path=FileEnum.DATA.value):
        """
        读取json数据
        :param file_path: 文件路径
        :param path: jsonpath
        :return: json对应键的值
        """
        with open(get_project_path(file_path), encoding="utf-8", mode='r') as f:
            # 读取json
            data = json.dumps(eval(f.read()))
            data_list = json.loads(data)
            # 提取值
            try:
                return jsonpath.jsonpath(data_list, path)[0]
            except TypeError:
                self.logger.debug(f'jsonData:{jsonpath.jsonpath(data_list, path)}')
                return jsonpath.jsonpath(data_list, path)

    def read_test_case(self, file_path, index=None):
        """
        读取用例文件
        :param index: 用例id
        :param file_path:yaml文件的路径
        :return: 返回用例内容
        """
        with open(get_project_path(file_path), encoding="utf-8", mode="r") as f:
            value = yaml.load(f, yaml.FullLoader)
            # uid_index = random.randint(0, 2)  # 随机索引
            if index is None:
                index = 0
            # 给header重新赋值
            header = value[index][CaseEnum.REQUESTS.value][CaseEnum.HEADER.value]
            self.reassignment(header, index)
            # 给params重新赋值
            params = value[index][CaseEnum.REQUESTS.value][CaseEnum.PARAMS.value]
            self.reassignment(params, index)
            # 返回用例数据
            return value[index]

    def reassignment(self, parameter, index):
        """
        对用例数据进行数据驱动（根据不同数据类型重新赋值）
        :param parameter: yaml读出的用例数据
        :param index: 用例id
        :return:
        """
        for payload in parameter:
            if parameter[payload].startswith('$'):  # $开头则调赋值方法
                self.handle_value(parameter=parameter, payload=payload, index=index)
            elif parameter[payload].startswith(CaseEnum.SQL.value):  # sql开头则去操作数据库
                # 创建数据库处理对象
                opdb = OperateDB()
                self.handle_sql(parameter=parameter, payload=payload, opdb=opdb)
            elif parameter[payload] == 'time':  # 值为time则赋值当前时间戳
                parameter[payload] = round(time.time() * 1000)

    def handle_value(self, parameter, payload, index):
        """
        对使用json提取器的用例数据重新赋值
        :param parameter: yaml读出的用例数据
        :param payload: 当前遍历的键
        :param index: 用例id
        :return:
        """
        try:
            # 先读取data.json
            if self.read_json(parameter[payload]) is False:
                raise TypeError
            parameter[payload] = self.read_json(parameter[payload])
            self.logger.debug(f'参数：{parameter[payload]}')
        except TypeError:
            # data.json没取到则取上一个接口响应值，索引-1
            path = parameter[payload].replace('$', f'$[{index - 1}]')
            if self.read_yaml(path=path) is False:
                self.logger.debug('json和yaml都没读到数据')
                raise '数据读取异常'
            parameter[payload] = self.read_yaml(path=path)

    def handle_sql(self, parameter, payload, opdb):
        """
        对使用sql语句的的用例数据进行处理
        :param parameter: yaml读出的用例数据
        :param payload: 当前遍历的键
        :param opdb: 数据库处理对象
        :return:
        """
        self.logger.debug('处理sql中')
        if parameter[payload].split(',')[0] == CaseEnum.PRINT.value:  # 打印sql执行结果
            check_data(opdb.handle_db(parameter[payload].split(',')[1]))
        elif parameter[payload].split(',')[0] == CaseEnum.ASSIGNMENT.value:  # 赋值当前查询结果
            parameter[payload] = opdb.handle_db(parameter[payload].split(',')[1])[0]
        elif parameter[payload].split(',')[0] == CaseEnum.HANDLE.value:  # 仅执行
            opdb.handle_db(parameter[payload].split(',')[1])
        else:
            self.logger.debug('sql执行失败')
            raise 'sql类型错误，检查用例文件'
