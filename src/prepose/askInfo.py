class InitClientApi:
    """定义请求信息"""

    def __init__(self):
        # 初始化数据
        self.address = utils.read_test_data("test_url")[0]
        self.wx_uid = utils.read_test_data("wx_uid")[0]  # 先写死,后续造数据random随机取值
        self.ali_uid = utils.read_test_data("ali_uid")[0]  # 先写死,后续造数据random随机取值

    def init_wx_params(self, path, **kwargs):
        """微信渠道uid请求"""
        # url
        url = self.address + path
        # 请求头
        headers = {
            "uid": self.wx_uid
        }
        # 参数
        params = {}
        for payload in kwargs:
            params[payload] = kwargs[payload]
        # 字典传递定义的请求信息
        info = {'url': url, 'headers': headers, 'params': params}
        return info

    def init_ali_params(self, path, **kwargs):
        """支付宝渠道uid请求"""
        # url
        url = self.address + path
        # 请求头
        headers = {
            "uid": self.ali_uid
        }
        # 参数
        params = {}
        for payload in kwargs:
            params[payload] = kwargs[payload]
        # 字典传递定义的请求信息
        info = {'url': url, 'headers': headers, 'params': params}
        return info

    def init_no_header(self, path, **kwargs):
        """无请求头请求"""
        # url
        url = self.address + path
        # 参数
        params = {}
        for payload in kwargs:
            params[payload] = kwargs[payload]
        # 字典传递定义的请求信息
        info = {'url': url, 'params': params}
        return info
