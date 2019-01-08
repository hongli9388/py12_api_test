# -*- coding: utf-8 -*-
# @time     : 2019/1/1 0001 下午 22:44
# @Author   : yuxuan
# #file     : base_case.py



# 完成投资人登录，把cookies放到上下文中，为后面其他接口做准备

import unittest
from common.http_requests_api import HttpRequest
from common import contants
from common.do_excel import DoExcel
import json
from ddt import ddt,data
from common.read_config import ReadConfig
from common.basic_data import DoRegex,Context
from common.mylogger1 import MyLog

do_excel = DoExcel(contants.data_dir)
cases = do_excel.get_case('normal')
my_logger = MyLog()

@ddt
class BaseCase(unittest.TestCase):


    @data(*cases)
    def test_base(self,case):

        url = ReadConfig().get('test_api','url_pre') + case.url
        my_logger.info('请求地址:{0}'.format(url))
        data = DoRegex.replace(case.data)
        data = json.loads(data)
        my_logger.info('请求参数:{0}'.format(data))
        if hasattr(Context,'cookies'):
            cookies = getattr(Context, 'cookies')
        else:
            cookies = None
        resp = HttpRequest(method=case.method, url=url, data=data, cookies=cookies)
        my_logger.info('请求返回结果:{0}'.format(resp.get_json()))
        self.assertEqual(case.expected,int(resp.get_json()['code']))

        # 判断是否有cookies
        if resp.get_cookie():
            setattr(Context,'cookies',resp.get_cookie())





