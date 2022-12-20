from prepose.createSession import HandleClientApi


class TaskClientApi:
    """
    业务场景串联：
            返回值形式：字典{"wx_uid": 请求头数据， "resul": 响应文本}
                      字典{"ali_uid": 请求头数据， "resul": 响应文本}
    """

    def __init__(self):
        # 初始化操作层对象(发送请求)
        self.task = HandleClientApi()

    def return_get_wxdata(self, path, **kwargs):
        """获取微信渠道uid的get请求响应数据"""
        data = self.task.handle_wx_get(path=path, **kwargs)
        return data

    def return_post_wxdata(self, path, **kwargs):
        """获取微信渠道uid的post请求响应数据"""
        data = self.task.handle_wx_post(path=path, **kwargs)
        return data

    def return_get_alidata(self, path, **kwargs):
        """获取支付宝渠道uid的get请求响应数据"""
        data = self.task.handle_ali_get(path=path, **kwargs)
        return data

    def return_post_alidata(self, path, **kwargs):
        """获取支付宝渠道uid的post请求响应数据"""
        data = self.task.handle_ali_post(path=path, **kwargs)
        return data

    def return_no_header_get(self, path, **kwargs):
        """获取无请求头get请求的响应数据"""
        data = self.task.handle_no_header_get(path=path, **kwargs)
        return data

    def return_no_header_post(self, path, **kwargs):
        """获取无请求头post请求的响应数据"""
        data = self.task.handle_no_header_post(path=path, **kwargs)
        return data

#
# if __name__ == "__main__":
#     # 扫码接口
#     TaskClientApi().test_scan_code()
#
