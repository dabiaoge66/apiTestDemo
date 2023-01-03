import time
import pytest
from commons.requests_uitils import RequestsUtils


class TestCreateOrder(object):
    """
    扫码下单测试类
    索引：代表用例文件索引
    """

    def test_nothing_balance(self, base_url):
        """无卡券无活动(纯余额)"""
        RequestsUtils().module_method(base_url, 0)  # 扫码
        RequestsUtils().module_method(base_url, 1)  # 下单
        time.sleep(2)

    def test_nothing_wx(self, base_url):
        """无卡券无活动(纯微信)"""
        RequestsUtils().module_method(base_url, 2)  # 扫码
        RequestsUtils().module_method(base_url, 3)  # 下单
        time.sleep(2)
        RequestsUtils().module_method(base_url, 4)  # 回调

    def test_nothing_ali(self, base_url):
        """无卡券无活动(纯支付宝)"""
        RequestsUtils().module_method(base_url, 5)  # 扫码
        RequestsUtils().module_method(base_url, 6)  # 下单
        time.sleep(2)
        RequestsUtils().module_method(base_url, 7)  # 回调


if __name__ == '__main__':
    pytest.main(['-vs', 'testCreateOrder.py'])
