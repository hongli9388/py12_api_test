# -*- coding: utf-8 -*-
# @time     : 2019/1/2 0002 上午 09:08
# @Author   : yuxuan
# #file     : test_loanlist.py


# 获取标的列表
from testcases.base_case import BaseCase
from common.basic_data import DoRegex,Context
from common.http_requests_api import HttpRequest
from common import contants
from common.do_excel import DoExcel
from common.do_mysql_tool import MysqlTool
from common.read_config import ReadConfig
from ddt import ddt,data
from common.mylogger1 import MyLog


do_excel = DoExcel(contants.data_dir)
cases = do_excel.get_case('getLoanList')
my_logger = MyLog()


@ddt
class TestGetLoanList(BaseCase):


    @classmethod
    def setUpClass(cls):
        global mysql
        mysql = MysqlTool()

    @data(*cases)
    def test_get_loan_list(self, case):

        my_logger.info('正在执行第{0}条用例{1}'.format(case.case_id, case.title))
        url = ReadConfig().get('test_api', 'url_pre') + case.url
        my_logger.info('检查url接口地址:{0}'.format(url))
        if hasattr(Context, 'cookies'):
            cookies = getattr(Context, 'cookies')
        else:
            cookies = None
        my_logger.info('---------开始http请求-----------')
        resp = HttpRequest(method=case.method, url=url, data=case.data, cookies=cookies)
        my_logger.info('---------结束http请求-----------')
        my_logger.info('请求接口结果是:{0}'.format(resp.get_json()))

        try:
            self.assertEqual(case.expected,int(resp.get_json()['code']))
            Test_result = 'Pass'
        except AssertionError as e:
            Test_result = 'Failed'
            my_logger.error('出错了{0}'.format(e))
            raise e

        my_logger.info('本条用例执行结果:{0}'.format(Test_result))

        # 数据验证
       # 如果获取标的列表成功，请求返回参数中记录数与查询数据库是否一致
        if resp.get_json()['code'] == '10001':
            seek_loan_list = 'SELECT COUNT(Id) FROM future.loan;'
            actual = mysql.fetch_one(seek_loan_list)['COUNT(Id)']
            expected = len(resp.get_json()['data'])
            self.assertEqual(expected, actual)
            my_logger.info('请求返回获取标列表记录数与查询数据库loan表记录数一致')

    @classmethod
    def tearDownClass(cls):
        mysql.close()


