# -*- coding: utf-8 -*-
# @time     : 2018/12/14 0014 下午 19:52
# @Author   : yuxuan
# #file     : http_requests_api.py

# 其中：requests封装类，需要实现的功能是一个函数就可以负责模拟全部请求方法的调用。

# 配置文件读取类，实现加载配置文件项

# 完成http的请求

import requests

class HttpRequest:
    #定义http请求方法
    def __init__(self,method,url,data = None,cookies = None,headers = None):
        try:
            if method == "get":
                self.res=requests.get(url=url,params=data,cookies=cookies,headers=headers)
            elif method == "post":
                self.res=requests.post(url=url,data=data,cookies=cookies,headers=headers)
            elif method == 'delete':
                self.res = requests.delete(url=url, data=data, cookies=cookies, headers=headers)
            elif method == 'options':
                self.res = requests.options(url=url, data=data, cookies=cookies, headers=headers)
            elif method == 'head':
                self.res = requests.head(url=url, data=data, cookies=cookies, headers=headers)
            elif method == 'put':
                self.res = requests.put(url=url, data=data, cookies=cookies, headers=headers)
            elif method == 'patch':
                self.res = requests.patch(url=url, data=data, cookies=cookies, headers=headers)

        except Exception as e:
            raise e

    def get_status_code(self):
        return self.res.status_code

    def get_text(self):
        return self.res.text

    def get_json(self):
        return self.res.json()

    def get_cookie(self,key=None):
        if key:
            return self.res.cookies[key]   # 返回cookie对应的key值
        else:
            return self.res.cookies     # 返回整个cookie对象

    def get_headers(self):
        return self.res.headers













