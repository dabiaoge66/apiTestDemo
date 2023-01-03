from enum import Enum


class CaseEnum(Enum):
    # 用例要素
    FEATURE = 'feature'
    STORY = 'story'
    TITLE = 'title'
    REQUESTS = 'requests'
    VALIDATE = 'validate'

    # 请求要素
    METHOD = 'method'
    PATH = 'path'
    HEADER = 'headers'
    PARAMS = 'params'

    # 断言要素
    ACTUAL = 'assert_method'
    COMPARE = 'compare_method'
    EXPECT = 'assert_field'

    # 比较方法
    CODE = 'code'
    IS = 'is'
    NOT = 'not'
    IN = 'in'

    # sql关键字
    SQL = 'sql'
    PRINT = 'sql_print'
    ASSIGNMENT = 'sql_assignment'
    HANDLE = 'sql_handle'

