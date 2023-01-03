from config.utils import CaseEnum


def validate_main(request_obj, validate_data):
    """
    断言主函数
    :param validate_data: 用例文件validate重新赋值后的数据
    :param request_obj: 传入request对象
    """
    actual = validate_data[CaseEnum.ACTUAL]
    method = validate_data[CaseEnum.COMPARE]
    expect = validate_data[CaseEnum.EXPECT]

    for payload in actual:
        if actual[payload] == CaseEnum.CODE:
            assert_status(payload, request_obj, method, expect)
        else:
            assert_data(payload, actual, method, expect)


def assert_status(payload, request_obj, method, expect):
    """断言响应状态码"""
    if method[payload] == CaseEnum.IS:  # 相等
        assert request_obj.status_code.equals(expect[payload])
    elif method[payload] == CaseEnum.NOT:  # 不等
        assert request_obj.status_code != expect[payload]


def assert_data(payload, actual, method, expect):
    """断言响应数据"""
    if method[payload] == CaseEnum.IS:  # 相等
        assert actual[payload].equals(expect[payload])
    elif method[payload] == CaseEnum.NOT:  # 不等
        assert actual[payload] != expect[payload]
    elif method[payload] == CaseEnum.CONTAIN:  # 包含
        assert actual[payload].contains(expect[payload])
