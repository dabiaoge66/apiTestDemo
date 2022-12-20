import requests
from commons.yaml_utils import clear_yaml, write_yaml, read_test_case


class RequestsUtils:
    """请求工具类"""
    sess = requests.session()

    @staticmethod
    def seed_requests(**kwargs):
        """统一发送请求和异常处理"""
        # info=[data["feature"], data["story"], data["title"]]
        print('-*-' * 20 + kwargs["data"
                                  ""]["title"] + '-*-' * 20)
        data = kwargs["data"]
        url = kwargs["base_url"] + data["requests"]["path"]
        res = RequestsUtils.sess.request(
            method=data["requests"]["method"],
            url=url,
            headers=data["requests"]["headers"],
            params=data["requests"]["params"]
        )
        write_yaml(res.json())  # 写入响应数据
        print(res.raw)
        return res

    @staticmethod
    def module_method(base_url, index):
        # 读取扫码接口用例文件
        scan_data = read_test_case("test_case/createOrder.yaml")
        # 发送请求
        RequestsUtils.seed_requests(data=scan_data, base_url=base_url)
        # 读取下单接口用例文件
        create_data = read_test_case("test_case/createOrder.yaml", index)
        # 余额下单支付
        RequestsUtils.seed_requests(data=create_data, base_url=base_url)
