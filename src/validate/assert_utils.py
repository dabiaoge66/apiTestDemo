from config.utils import CaseEnum


def validate_main(request_obj, validate_data):
    """
    断言主函数
    :param validate_data: 用例文件validate重新赋值后的数据
    :param request_obj: 传入request对象
    """
    result = True  # 若断言数据为None，默认返回True
    if validate_data is not None:
        actual = validate_data[CaseEnum.ACTUAL.value]
        method = validate_data[CaseEnum.COMPARE.value]
        expect = validate_data[CaseEnum.EXPECT.value]

        for payload in actual:
            if actual[payload] == CaseEnum.CODE.value:
                result = assert_status(payload, request_obj, method, expect)
            else:
                result = assert_data(payload, actual, method, expect)
    return result


def assert_status(payload, request_obj, method, expect):
    """断言响应状态码"""
    # 为了方便读取，yaml不给int类型数据；因此将状态码转为str
    result = True
    try:
        if method[payload] == CaseEnum.IS.value:  # 相等
            assert str(request_obj.status_code) == expect[payload]
        elif method[payload] == CaseEnum.NOT.value:  # 不等
            assert str(request_obj.status_code) != expect[payload]
    except AssertionError:
        result = False
    finally:
        return result


def assert_data(payload, actual, method, expect):
    """断言响应数据"""
    result = True
    try:
        if method[payload] == CaseEnum.IS.value:  # 相等
            assert actual[payload] == expect[payload]
        elif method[payload] == CaseEnum.NOT.value:  # 不等
            assert actual[payload] != expect[payload]
        elif method[payload] == CaseEnum.IN.value:  # 包含
            assert expect[payload] in actual[payload]
    except AssertionError:
        result = False
    finally:
        return result
