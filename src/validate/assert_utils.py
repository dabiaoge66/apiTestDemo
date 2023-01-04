from config.utils import CaseEnum


def assertions(request_obj, validate_data):
    """
    断言函数主入口，为便于调用写为方法
    :return: 返回断言结果（bool）
    """
    return Assertions().validate_main(request_obj, validate_data)


class Assertions:
    """断言操作类"""
    def validate_main(self, request_obj, validate_data):
        """
        断言主函数
        :param validate_data: 用例数据validate重新赋值后的数据
        :param request_obj: 传入request对象
        """
        result = True  # 若断言数据为None，默认返回True
        if validate_data is not None:
            actual = validate_data[CaseEnum.ACTUAL.value]
            method = validate_data[CaseEnum.COMPARE.value]
            expect = validate_data[CaseEnum.EXPECT.value]

            for payload in actual:
                if actual[payload] == CaseEnum.CODE.value:
                    result = self.assert_status(payload, request_obj, method, expect)
                else:
                    result = self.assert_data(payload, actual, method, expect)
        return result

    @staticmethod
    def assert_status(payload, request_obj, method, expect):
        """
        断言响应状态码
        :param payload: 当前遍历的键
        :param request_obj: request对象
        :param method: 用例数据请求方式的键名
        :param expect: 用例数据预期结果的键名
        :return: 返回断言结果
        """
        # 为了方便读取，yaml不给int类型数据；因此将状态码转为str
        result = True
        try:
            if method[payload] == CaseEnum.IS.value:  # 相等
                assert str(request_obj.status_code) == expect[payload]
            elif method[payload] == CaseEnum.NOT.value:  # 不等
                assert str(request_obj.status_code) != expect[payload]
        except AssertionError as e:
            result = False
            raise e
        finally:
            return result

    @staticmethod
    def assert_data(payload, actual, method, expect):
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
            result = False
            raise e
        finally:
            return result
