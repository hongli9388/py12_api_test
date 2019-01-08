# -*- coding: utf-8 -*-
# @time     : 2019/1/2 0002 上午 10:01
# @Author   : yuxuan
# #file     : test_get_Loan_investrecoed.py

from testcases.base_case import BaseCase
from common.basic_data import DoRegex,Context
from common.http_requests_api import HttpRequest
from common import contants
from common.do_excel import DoExcel
from common.do_mysql_tool import MysqlTool
import json
from common.read_config import ReadConfig
from ddt import ddt,data
from common.mylogger1 import MyLog


# 获取标的所有投资记录

do_excel = DoExcel(contants.data_dir)
cases = do_excel.get_case('get_loan_invest_record')
my_logger = MyLog()

@ddt
class TestGetLoanInvestRecord(BaseCase):

    @classmethod
    def setUpClass(cls):
        global mysql
        mysql = MysqlTool()

    @data(*cases)
    def test_get_Loan_invest_record(self, case):
        my_logger.info('正在执行第{0}条用例{1}'.format(case.case_id, case.title))
        url = ReadConfig().get('test_api', 'url_pre') + case.url
        my_logger.info('检查url接口地址:{0}'.format(url))
        if hasattr(Context, 'cookies'):
            cookies = getattr(Context, 'cookies')
        else:
            cookies = None

        data = DoRegex().replace(case.data)
        data = json.loads(data)

        my_logger.info('---------开始http请求-----------')
        resp = HttpRequest(method=case.method, url=url, data=data, cookies=cookies)
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
        if resp.get_json()['msg'] == '获取记录成功':
            seek_invest_record = 'SELECT COUNT(Id) FROM future.invest where LoanId={0};'.format(data['loanId'])
            actual = mysql.fetch_one(seek_invest_record)['COUNT(Id)']
            expected = len(resp.get_json()['data'])
            self.assertEqual(expected, actual)
            my_logger.info('请求返回获取标的所有投资记录数与查询数据库Invest表中记录数一致')


    @classmethod
    def tearDownClass(cls):
        mysql.close()


