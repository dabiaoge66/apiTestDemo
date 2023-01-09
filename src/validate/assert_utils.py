from commons.yaml_utils import YamlOpt
from config.utils import CaseEnum
from log.log_utils import get_log


def assertions(request_obj, validate_data, index):
    """
    断言函数主入口，为便于调用写为方法
    :return: 返回断言结果（bool）
    """
    return Assertions().validate_main(request_obj, validate_data, index)


class Assertions:
    """断言操作类"""
    def __init__(self):
        # 日志对象
        self.logger = get_log('test.log', 'r')

    def validate_main(self, request_obj, validate_data, index):
        """
        断言主函数
        :param index: 数据索引
        :param validate_data: 用例数据validate重新赋值后的数据
        :param request_obj: 传入request对象
        """
        result = True  # 若断言数据为None，默认返回True
        if validate_data is not None:
            self.logger.debug('正在执行断言')
            actual = validate_data[CaseEnum.ACTUAL.value]
            YamlOpt().reassignment(actual, index + 1)  # 重新赋值
            method = validate_data[CaseEnum.COMPARE.value]
            expect = validate_data[CaseEnum.EXPECT.value]
            YamlOpt().reassignment(actual, index + 1)  # 重新赋值

            for payload in actual:
                if actual[payload] == CaseEnum.CODE.value:
                    result = self.assert_status(payload, request_obj, method, expect)
                else:
                    result = self.assert_data(payload, actual, method, expect)
        return result

    def assert_status(self, payload, request_obj, method, expect):
        """
        断言响应状态码
        :param payload: 当前遍历的键
        :param request_obj: request对象
        :param method: 用例数据请求方式的键名
        :param expect: 用例数据预期结果的键名
        :return: 返回断言结果
        """
        # 重新赋值时为了不影响startwith的判断的执行，yaml响应码要给字符串
        result = True
        try:
            self.logger.debug('正在校对响应码')
            if method[payload] == CaseEnum.IS.value:  # 相等
                assert request_obj.status_code == expect[payload]
            elif method[payload] == CaseEnum.NOT.value:  # 不等
                assert request_obj.status_code != expect[payload]
        except AssertionError as e:
            self.logger.debug('响应码断言未通过')
            result = False
            raise e
        finally:
            return result

    def assert_data(self, payload, actual, method, expect):
        """
        断言响应数据
        :param payload: 当前遍历的键
        :param actual: 用例数据实际结果的键名
        :param method: 用例数据请求方式的键名
        :param expect: 用例数据预期结果的键名
        :return: 返回断言结果
        """
        result = True
        try:
            if method[payload] == CaseEnum.IS.value:  # 相等
                assert actual[payload] == expect[payload]
            elif method[payload] == CaseEnum.NOT.value:  # 不等
                assert actual[payload] != expect[payload]
            elif method[payload] == CaseEnum.IN.value:  # 包含
                assert expect[payload] in actual[payload]
        except AssertionError as e:
            self.logger.debug(f'响应数据断言未通过,预期结果：{expect[payload]}, 实际结果：{actual[payload]}')
            result = False
            raise e
        finally:
            return result
