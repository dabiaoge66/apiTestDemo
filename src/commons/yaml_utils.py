import json
import time
import jsonpath as jsonpath
import yaml
from config.utils import CaseEnum, get_project_path, FileEnum
from data.database_utils import check_data, OperateDB


def read_yaml(file_path=FileEnum.EXTRACT, path=None):
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
            # jsonpath返回的是一个列表，取第一个值返回，方便操作
            return jsonpath.jsonpath(value, path)[0]


def write_yaml(data, file_path=FileEnum.EXTRACT):
    """
    写入数据(a+:追加)
    :param data:
    :param file_path:
    :return:
    """
    with open(get_project_path(file_path), encoding="utf-8", mode="a+") as f:
        yaml.dump([data], stream=f, allow_unicode=True)


def clear_yaml(file_path=FileEnum.EXTRACT):
    """
    清空yaml文件
    :param file_path:
    """
    with open(get_project_path(file_path), encoding="utf-8", mode="w") as f:
        f.truncate()


#
def read_json(path, file_path=FileEnum.DATA):
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
        return jsonpath.jsonpath(data_list, path)[0]


def read_test_case(file_path, index=None):
    """
    读取用例文件并实现ddt数据驱动
    :param index: 用例索引
    :param file_path:yaml文件的路径
    :return: 返回一个用例内容
    """
    with open(get_project_path(file_path), encoding="utf-8", mode="r") as f:
        value = yaml.load(f, yaml.FullLoader)
        # uid_index = random.randint(0, 2)  # 随机索引
        if index is None:
            index = 0
        # 给header重新赋值
        header = value[index][CaseEnum.REQUESTS.value][CaseEnum.HEADER.value]
        reassignment(header, index)
        # 给params重新赋值
        params = value[index][CaseEnum.REQUESTS.value][CaseEnum.PARAMS.value]
        reassignment(params, index)
        # 给assert_path重新赋值
        assert_path = value[index][CaseEnum.VALIDATE.value][CaseEnum.ACTUAL.value]
        reassignment(assert_path, index)
        # 给assert_field重新赋值
        assert_field = value[index][CaseEnum.VALIDATE.value][CaseEnum.EXPECT.value]
        reassignment(assert_field, index)
        # 返回用例数据
        return value[index]


def reassignment(parameter, index):
    """用例数据重新赋值"""
    # 创建数据库处理对象
    opdb = OperateDB()
    for payload in parameter:
        if parameter[payload].startswith('$'):  # $开头则去data.json获取上一个接口返回值里取值
            handle_value(parameter=parameter, payload=payload, index=index)
            continue
        elif parameter[payload].startswith(CaseEnum.SQL.value):  # sql开头则去操作数据库
            handle_sql(params=parameter, payload=payload, opdb=opdb)
        elif parameter[payload] == 'time':  # 值为time则赋值当前时间戳
            parameter[payload] = round(time.time() * 1000)


def handle_value(parameter, payload, index):
    """重新赋值"""
    try:
        parameter[payload] = read_json(parameter[payload])
    except TypeError:
        # data.json没取到则取上一个接口响应值，索引-1
        parameter[payload] = read_yaml(path=parameter[payload].replace('$', f'$[{index - 1}]'))


def handle_sql(params, payload, opdb):
    """处理sql"""
    if params[payload].split(',')[0] == CaseEnum.PRINT.value:  # 打印sql执行结果
        check_data(opdb.handle_db(params[payload].split(',')[1]))
    elif params[payload].split(',')[0] == CaseEnum.ASSIGNMENT.value:  # 赋值当前查询结果
        params[payload] = opdb.handle_db(params[payload].split(',')[1])[0]
    elif params[payload].split(',')[0] == CaseEnum.HANDLE.value:  # 仅执行
        opdb.handle_db(params[payload].split(',')[1])
    else:
        raise 'sql类型错误，检查用例文件'
