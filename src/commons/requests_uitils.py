import requests
from commons.yaml_utils import YamlOpt
from config.utils import CaseEnum, FileEnum
from log.log_utils import get_log
from validate.assert_utils import assertions


class RequestsUtils:
    """请求工具类"""
    def __init__(self):
        # session对象
        self.sess = requests.session()
        # 日志对象
        self.logger = get_log('requests_utils.log', 'r')

    def seed_requests(self, **kwargs):
        """统一发送请求和异常处理"""
        # info=[data["feature"], data["story"], data["title"]]
        print('-*-' * 20 + kwargs["data"][CaseEnum.TITLE.value] + '-*-' * 20)
        data = kwargs["data"]
        url = kwargs["base_url"] + data[CaseEnum.REQUESTS.value][CaseEnum.PATH.value]
        req = self.sess.request(
            method=data[CaseEnum.REQUESTS.value][CaseEnum.METHOD.value],
            url=url,
            headers=data[CaseEnum.REQUESTS.value][CaseEnum.HEADER.value],
            params=data[CaseEnum.REQUESTS.value][CaseEnum.PARAMS.value]
        )
        YamlOpt().write_yaml(req.json())  # 写入响应数据
        self.logger.info(f'\n请求地址:{req.url}'
                         f'\n请求头:{data[CaseEnum.REQUESTS.value][CaseEnum.HEADER.value]}'
                         f'\n响应信息:{req.text}')
        return req

    def module_method(self, base_url, index):
        """
        用例执行步骤的示例
        :param base_url: pytest配置文件中设置的base_url,固定用法
        :param index: 用例id
        :return:
        """
        # 读取接口用例文件
        data = YamlOpt().read_test_case(FileEnum.CREATE.value, index)
        # 发送请求
        req = self.seed_requests(base_url=base_url, data=data)
        # 断言
        result = assertions(request_obj=req, validate_data=data[CaseEnum.VALIDATE.value], index=index)
        self.logger.info(f'断言结果：{result}')
        return data['title']

    def for_test(self, base_url, index):
        """浅浅测试一下"""
        data = YamlOpt().read_test_case(FileEnum.DEBUG.value, index)
        req = self.seed_requests(base_url=base_url, data=data)
        result = assertions(request_obj=req, validate_data=data[CaseEnum.VALIDATE.value], index=index)
        self.logger.info(f'断言结果：{result}')
