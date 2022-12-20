import requests
from prepose.askInfo import InitClientApi


class HandleClientApi:
    """发送请求"""

    def __init__(self):
        # 初始化数据层对象(定义请求信息)
        self.init = InitClientApi()

    def handle_wx_get(self, path, **kwargs):
        """微信渠道uid的get请求"""
        url, headers, params = map(self.init.init_wx_params(path=path, **kwargs).get,
                                   ("url", "headers", "params"))
        # 发送请求
        res = requests.get(url=url, headers=headers, params=params, verify=False)
        # 返回响应信息
        print(res.url + "\n" + res.text + "\n")
        return {"wx_uid": headers, "result": res.json()}

    def handle_wx_post(self, path, **kwargs):
        """微信渠道uid的post请求"""
        url, headers, params = map(self.init.init_wx_params(path=path, **kwargs).get,
                                   ("url", "headers", "params"))
        res = requests.post(url=url, headers=headers, params=params, verify=False)
        print(res.url + "\n" + res.text + "\n")
        return {"wx_uid": headers, "result": res.json()}

    def handle_ali_get(self, path, **kwargs):
        """支付宝渠道uid的get请求"""
        url, headers, params = map(self.init.init_ali_params(path=path, **kwargs).get,
                                   ("url", "headers", "params"))
        # 发送请求
        res = requests.get(url=url, headers=headers, params=params, verify=False)
        # 返回响应信息
        print(res.url + "\n" + res.text + "\n")
        return {"ali_uid": headers, "result": res.json()}

    def handle_ali_post(self, path, **kwargs):
        """支付宝渠道uid的post请求"""
        url, headers, params = map(self.init.init_ali_params(path=path, **kwargs).get,
                                   ("url", "headers", "params"))
        res = requests.post(url=url, headers=headers, params=params, verify=False)
        print(res.url + "\n" + res.text + "\n")
        return {"ali_uid": headers, "result": res.json()}

    def handle_no_header_get(self, path, **kwargs):
        """无请求头的的post请求"""
        url, params = map(self.init.init_no_header(path=path, **kwargs).get,
                          ("url", "params"))
        res = requests.get(url=url, params=params, verify=False)
        print(res.url + "\n" + res.text + "\n")
        return res.json()

    def handle_no_header_post(self, path, **kwargs):
        """无请求头的的post请求"""
        url, params = map(self.init.init_no_header(path=path, **kwargs).get,
                          ("url", "params"))
        res = requests.post(url=url, params=params, verify=False)
        print(res.url + "\n" + res.text + "\n")
        return res.json()
