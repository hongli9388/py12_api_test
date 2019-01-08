# -*- coding: utf-8 -*-
# @time     : 2018/12/22 0022 上午 11:27
# @Author   : yuxuan
# #file     : test_login.py

import unittest
from common.do_excel import DoExcel
from common.http_requests_api import HttpRequest
from common import contants
import json
from common.basic_data import DoRegex
from common.read_config import ReadConfig
from common.mylogger1 import MyLog
from ddt import ddt,data      #data 可以控制读取单个数据/多个数据，fiel_data读取文件数据
# 如其中一个用例失败，后面的用例不执行，可采用ddt数据驱动
#编写登录请求测试类

do_excel = DoExcel(contants.data_dir)
cases = do_excel.get_case('login')  #列表外包字符串

my_logger = MyLog()
@ddt
class TestLogin(unittest.TestCase):

    def setUp(self):
        print('测试开始，环境准备')

    @data(*cases)   # *为去列表外字符串
    def test_login(self,case):
            my_logger.info('正在执行第{0}条用例{1}'.format(case.case_id,case.title))
            my_logger.info('------开始检查url接口地址--------------')
            url = ReadConfig().get('test_api','url_pre')+case.url
            my_logger.info('url地址:{0}'.format(url))
            my_logger.info('------------开始检查请求参数-----------')
            data = DoRegex().replace(case.data)     # 完成数据库匹配替换
            # 将excel读取出来的字符串转换成字典
            data = json.loads(data)
            my_logger.info(data)
            my_logger.info('请求参数是:{0}'.format(data))
            my_logger.info('----------开始http接口请求----------')
            resp = HttpRequest(method=case.method, url=url, data=data)
            my_logger.info('----------结束http接口请求----------')
            try:
                self.assertEqual(case.expected,resp.get_text())
                Test_result = 'Pass'
            except AssertionError as e:
                Test_result = 'Failed'
                print('断言出错了%s:', e)
                raise e

            my_logger.info('本条用例执行的测试结果是:{0}'.format(Test_result))

    def tearDown(self):
        print('测试完成，环境还原')


