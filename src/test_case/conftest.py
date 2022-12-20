import pytest

from commons.yaml_utils import clear_yaml


# @pytest.fixture(scope='session', autouse=True, params=['test1', 'test2'], name='cm')
@pytest.fixture(scope='session', autouse=True)
def case_control():
    """用例执行管理"""
    clear_yaml()  # 清空yaml
    # yield request.param
    yield

# def test_case_01(self, cm):
#     print('测试用例')
