import time
# import pytest
from commons.requests_uitils import RequestsUtils
from log.log_utils import get_log


class TestCreateOrder(object):
    """扫码下单测试类（传入的索引为用例id）"""
    logger = get_log('testcase.log', 'r')

    def test_nothing_balance(self, base_url):
        """无卡券无活动(纯余额)"""
        self.logger.info('执行用例步骤-扫码')
        RequestsUtils().module_method(base_url, 0)
        self.logger.info('执行用例步骤-下单')
        RequestsUtils().module_method(base_url, 1)
        self.logger.info('等待2s....')
        time.sleep(2)

    def test_nothing_wx(self, base_url):
        """无卡券无活动(纯微信)"""
        self.logger.info('执行用例步骤-扫码')
        RequestsUtils().module_method(base_url, 2)
        self.logger.info('执行用例步骤-下单')
        RequestsUtils().module_method(base_url, 3)
        self.logger.info('等待2s....')
        time.sleep(2)
        self.logger.info('执行用例步骤-回调')
        RequestsUtils().module_method(base_url, 4)

    def test_nothing_ali(self, base_url):
        """无卡券无活动(纯支付宝)"""
        self.logger.info('执行用例步骤-扫码')
        RequestsUtils().module_method(base_url, 5)
        self.logger.info('执行用例步骤-下单')
        RequestsUtils().module_method(base_url, 6)
        self.logger.info('等待2s....')
        time.sleep(2)
        self.logger.info('执行用例步骤-回调')
        RequestsUtils().module_method(base_url, 7)


# if __name__ == '__main__':
#     pytest.main(['-vs', 'testCreateOrder.py'])
