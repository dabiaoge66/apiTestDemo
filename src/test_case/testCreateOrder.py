import time
# import pytest
import allure

from commons.requests_uitils import RequestsUtils
from config.utils import CaseEnum
from log.log_utils import get_log


@allure.feature('扫码下单')
class TestCreateOrder(object):
    """扫码下单测试类（传入的索引为用例id）"""
    logger = get_log('testcase.log', 'r')
    feature = CaseEnum.FEATURE.value
    story = CaseEnum.STORY.value
    title = CaseEnum.TITLE.value
    step = ''
    info = {feature: '', story: '', title: '', step: ''}

    @allure.title('info[title]')
    def step(self, base_url, index):
        self.info = RequestsUtils().module_method(base_url, index)
        allure.dynamic.title(self.info[self.title])  # 动态设置用例标题
        self.logger.info(f'当前用例步骤-{self.title}')

    @allure.story(info[story])
    def test_nothing_balance(self, base_url):
        self.step(base_url, 0)
        allure.dynamic.story(self.info[self.story])  # 动态设置用例模块
        self.step(base_url, 1)
        self.logger.info('等待2s....')
        time.sleep(2)

    @allure.story('无卡券无活动(纯微信)')
    def test_nothing_wx(self, base_url):
        allure.dynamic.story(self.info[self.story])  # 动态设置用例模块
        self.step(base_url, 2)
        self.step(base_url, 3)
        self.logger.info('等待2s....')
        time.sleep(2)
        self.step(base_url, 4)

    @allure.story('无卡券无活动(纯支付宝)')
    def test_nothing_ali(self, base_url):
        allure.dynamic.story(self.info[self.story])  # 动态设置用例模块
        self.step(base_url, 5)
        self.step(base_url, 6)
        self.logger.info('等待2s....')
        time.sleep(2)
        self.step(base_url, 7)

# if __name__ == '__main__':
#     pytest.main(['-vs', 'testCreateOrder.py'])
