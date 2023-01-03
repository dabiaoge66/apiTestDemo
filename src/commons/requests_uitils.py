import requests
from commons.yaml_utils import write_yaml, read_test_case
from config.utils import CaseEnum
from validate.assert_result import validate_main


class RequestsUtils:
    """请求工具类"""
    sess = requests.session()

    @staticmethod
    def seed_requests(**kwargs):
        """统一发送请求和异常处理"""
        # info=[data["feature"], data["story"], data["title"]]
        print('-*-' * 20 + kwargs["data"][CaseEnum.TITLE.value] + '-*-' * 20)
        data = kwargs["data"]
        url = kwargs["base_url"] + data[CaseEnum.REQUESTS.value][CaseEnum.PATH.value]
        req = RequestsUtils.sess.request(
            method=data[CaseEnum.REQUESTS.value][CaseEnum.METHOD.value],
            url=url,
            headers=data[CaseEnum.REQUESTS.value][CaseEnum.HEADER.value],
            params=data[CaseEnum.REQUESTS.value][CaseEnum.PARAMS.value]
        )
        write_yaml(req.json())  # 写入响应数据
        print(f'request:{req.url}')
        print(f'request:{data[CaseEnum.REQUESTS.value][CaseEnum.HEADER.value]}')
        print(f'response:{req.text}')
        return req

    @staticmethod
    def module_method(base_url, index):
        # 读取接口用例文件
        data = read_test_case("test_case/createOrder.yaml", index)
        # 发送请求
        req = RequestsUtils.seed_requests(data=data, base_url=base_url)
        # 断言
        validate_main(request_obj=req, validate_data=data[CaseEnum.VALIDATE.value])

    @staticmethod
    def for_test(base_url, index):
        # 读取接口用例文件
        data = read_test_case("test_case/forTest.yaml", index)
        # 发送请求
        req = RequestsUtils.seed_requests(data=data, base_url=base_url)
        # 断言
        validate_main(request_obj=req, validate_data=data[CaseEnum.VALIDATE.value])
