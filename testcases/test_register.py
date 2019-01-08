# -*- coding: utf-8 -*-
# @time     : 2018/12/26 0026 下午 17:34
# @Author   : yuxuan
# #file     : test_register.py
import unittest
from common.do_excel import DoExcel
from common.http_requests_api import HttpRequest
from common import contants
import json
from common.mylogger1 import MyLog
from common.seek_replace import SeekReplace
from common.do_mysql_tool import MysqlTool
from common.read_config import ReadConfig
from ddt import ddt,data      #data 可以控制读取单个数据/多个数据，fiel_data读取文件数据
# 如其中一个用例失败，后面的用例不执行，可采用ddt数据驱动
#编写登录请求测试类

do_excel = DoExcel(contants.data_dir)
cases = do_excel.get_case('register')  #列表外包字符串

my_logger = MyLog()

@ddt
class TestRegister(unittest.TestCase):

    def setUp(self):
        self.sql = ReadConfig().get('SQL', 'mobile_sql')
        self.mysql_tool = MysqlTool()

    @data(*cases)
    def test_login(self, case):

            max_mobilephone = str(int(self.mysql_tool.fetch_one(self.sql)['MobilePhone']) + 1)  # 查询数据库最大手机号+1
            ReadConfig().write_value('MobilePhone', 'max_phone', max_mobilephone)  # 最大手机号写入配置文件
            my_logger.info('目前正在执行第{0}条用例:{1}'.format(case.case_id, case.title))
            my_logger.info('----------开始检查url请求地址--------')
            url = ReadConfig().get('test_api', 'url_pre') + case.url
            my_logger.info('url接口地址是:{0}'.format(url))
            #将excel读取出来的字符串转换成字典
            my_logger.info('----------开始检查请求参数------------')
            data = case.data
            data = json.loads(SeekReplace().seek_replace(data))
            my_logger.info('开始检查请求参数:{0}'.format(data))
            resp = HttpRequest(method=case.method, url=url, data=data)
            try:
                self.assertEqual(case.expected,resp.get_text())
                Test_result = 'Pass'
            except AssertionError as e:
                Test_result = 'Failed'
                print('断言出错了%s:', e)
                raise e

            my_logger.info('本条用例的测试结果:{}'.format(Test_result))

            # 数据验证

            if int(resp.get_json()['code']) == 10001:   # 注册成功，数据库查询有记录
                sql = 'SELECT * FROM future.member where MobilePhone="{0}"'.format(max_mobilephone)
                expected = max_mobilephone
                resp = self.mysql_tool.fetch_one(sql)
                if resp is not None:    # 判断查找数据库数据非空
                    self.assertEqual(expected, resp['MobilePhone'])
                    my_logger.info('注册成功，数据库查询正确')
                else:    # 如果查询为空，
                    my_logger.info('注册成功，数据库查询无数据')
                    raise AssertionError

            else:   # 注册不成功，数据库查询为空
                sql = 'SELECT * FROM future.member where MobilePhone="{0}"'.format(max_mobilephone)
                member = self.mysql_tool.fetch_one(sql)
                if member is None:    # 如果查询数据库为空
                    expected = None
                    self.assertEqual(expected,member)
                    my_logger.info('注册不成功，数据库查询无增加数据')
                else:  # 查询数据库非空
                    my_logger.info('注册不成功，数据库查询增加数据')
                    raise AssertionError

    def tearDown(self):
        self.mysql_tool.close()



