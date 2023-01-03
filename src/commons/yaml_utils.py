import json
import os
import time
import jsonpath as jsonpath
import yaml

from config.utils import CaseEnum
from data.database import handle_database, check_data


def get_project_path():
    """得到项目路径"""
    project_path = os.path.join(
        os.path.dirname(__file__),
        "..",
    )
    return project_path


# 写入数据(a+:追加)
def write_yaml(data):
    with open(get_project_path() + "/extract.yaml", encoding="utf-8", mode="a+") as f:
        yaml.dump([data], stream=f, allow_unicode=True)


# 读取数据
def read_yaml(path=None):
    """
    :param path:json路径表达式
    :return: 表达式为空返回整个对象，不为空，返回表达式下的值
    """
    with open(get_project_path() + "/extract.yaml", encoding="utf-8", mode="r") as f:
        value = yaml.load(f, yaml.FullLoader)
        if path is None:
            return value
        else:
            # jsonpath返回的是一个列表，取第一个值返回，方便操作
            return jsonpath.jsonpath(value, path)[0]


# 读取json数据
def read_json(path):
    """
    :param path: jsonpath
    :return: json对应键的值
    """
    with open(get_project_path() + '/data/data.json', encoding="utf-8", mode='r') as f:
        # 读取json
        data = json.dumps(eval(f.read()))
        data_list = json.loads(data)
        # 提取值
        return jsonpath.jsonpath(data_list, path)[0]


# 读取用例文件
def read_test_case(path, index=None):
    """
    :param index: 用例索引
    :param path:yaml文件的路径
    :return: 返回一个用例内容
    """
    with open(get_project_path() + '/' + path, encoding="utf-8", mode="r") as f:
        value = yaml.load(f, yaml.FullLoader)
        # uid_index = random.randint(0, 2)  # 随机索引
        if index is None:
            index = 0
        # 给header重新赋值
        header = value[index][CaseEnum.REQUESTS][CaseEnum.HEADER]
        reassignment(header, index)
        # 给params重新赋值
        params = value[index][CaseEnum.REQUESTS][CaseEnum.PARAMS]
        handle_params(params, index)
        # 给assert_path重新赋值
        assert_path = value[index][CaseEnum.VALIDATE][CaseEnum.ACTUAL]
        reassignment(assert_path, index)
        # 给assert_field重新赋值
        assert_field = value[index][CaseEnum.VALIDATE][CaseEnum.EXPECT]
        reassignment(assert_field, index)
        # 返回用例数据
        return value[index]


def reassignment(parameter, index):
    for payload in parameter:
        if parameter[payload].startswith('$'):
            try:
                parameter[payload] = read_json(parameter[payload])
            except TypeError:
                parameter[payload] = read_yaml(parameter[payload].replace('$', f'$[{index - 1}]'))
                continue


def handle_params(params, index):
    for payload in params:
        if params[payload].startswith('$'):  # $开头则去data.json获取上一个接口返回值里取值
            try:
                params[payload] = read_json(params[payload])
            except TypeError:
                # data.json没取到则取上一个接口响应值，索引-1
                params[payload] = read_yaml(params[payload].replace('$', f'$[{index - 1}]'))
                continue
        elif params[payload].startswith(CaseEnum.SQL):  # sql开头则去操作数据库
            if params[payload].split(',')[0] == CaseEnum.PRINT:  # 打印sql执行结果
                check_data(handle_database(params[payload].split(',')[1]))
            elif params[payload].split(',')[0] == CaseEnum.ASSIGNMENT:  # 赋值当前查询结果
                params[payload] = handle_database(params[payload].split(',')[1])[0]
            elif params[payload].split(',')[0] == CaseEnum.HANDLE:  # 仅执行
                handle_database(params[payload].split(',')[1])
            else:
                raise 'sql类型错误，检查用例文件'
        elif params[payload] == 'time':  # 值为time则赋值当前时间戳
            params[payload] = round(time.time() * 1000)


# 清空数据
def clear_yaml():
    with open(get_project_path() + "/extract.yaml", encoding="utf-8", mode="w") as f:
        f.truncate()
