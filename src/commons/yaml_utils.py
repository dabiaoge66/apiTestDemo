import json
import os
import time
import jsonpath as jsonpath
import yaml


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
    :param index: 索引
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
        # 给header重新赋值
        # uid_index = random.randint(0, 2)  # 随机索引
        if index is None:
            index = 0
        header = value[index]["requests"]["headers"]
        params = value[index]["requests"]["params"]
        for payload in header:
            if header[payload].startswith('$'):
                try:
                    header[payload] = read_json(header[payload])
                except TypeError:
                    header[payload] = read_yaml(header[payload].replace('$', f'$[{index}]'))
                    continue
        # 给params重新赋值
        for payload in params:
            if params[payload].startswith('$'):
                try:
                    params[payload] = read_json(params[payload])
                except TypeError:
                    # 取上一个接口响应值，所以索引-1
                    params[payload] = read_yaml(params[payload].replace('$', f'$[{index - 1}]'))
                    continue
            elif params[payload] == 'time':
                params[payload] = round(time.time() * 1000)
        return value[index]


# 清空数据
def clear_yaml():
    with open(get_project_path() + "/extract.yaml", encoding="utf-8", mode="w") as f:
        f.truncate()
