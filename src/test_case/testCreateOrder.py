import time
import pytest
from commons.requests_uitils import RequestsUtils
from commons.yaml_utils import read_test_case, clear_yaml, read_yaml, write_yaml


class TestCreateOrder(object):
    """扫码下单测试类"""

    def test_nothing_balance(self, base_url):
        """无卡券无活动(纯余额)"""
        RequestsUtils().module_method(base_url, 0)  # 读取用例1发送请求
        RequestsUtils().module_method(base_url, 1)  # 读取用例2发送请求

    def test_nothing_wx(self, base_url):
        """无卡券无活动(纯微信)"""
        RequestsUtils().module_method(base_url, 2)  # 读取用例1发送请求
        RequestsUtils().module_method(base_url, 3)  # 读取用例3发送请求


if __name__ == '__main__':
    pytest.main(['-vs', 'testCreateOrder.py'])
