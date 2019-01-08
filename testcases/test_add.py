# -*- coding: utf-8 -*-
# @time     : 2019/1/1 0001 下午 15:12
# @Author   : yuxuan
# #file     : test_add.py


import unittest
from common.http_requests_api import HttpRequest
from common import contants
from common.do_excel import DoExcel
import json
from common.do_mysql_tool import MysqlTool
from common.read_config import ReadConfig
from common.basic_data import DoRegex,Context
from ddt import ddt,data
from common.mylogger1 import MyLog



do_excel = DoExcel(contants.data_dir)
cases = do_excel.get_case('addLoan')
my_logger = MyLog()

Cookies = None

@ddt
class TestAddLoan(unittest.TestCase):

    def setUp(self):
        self.mysql = MysqlTool()

    @data(*cases)
    def test_add(self, case):
        global Cookies
        my_logger.info('正在执行第{0}条用例{1}'.format(case.case_id,case.title))
        url = ReadConfig().get('test_api', 'url_pre') + case.url
        my_logger.info('检查url接口地址:{0}'.format(url))
        data = DoRegex().replace(case.data)
        data = json.loads(data)
        my_logger.info('检查请求参数{0}'.format(data))
        my_logger.info('---------开始http请求-----------')
        resp = HttpRequest(method=case.method, url=url, data=data, cookies=Cookies)
        my_logger.info('---------结束http请求-----------')
        my_logger.info('请求接口结果是:{0}'.format(resp.get_json()))
        try:
            self.assertEqual(case.expected,int(resp.get_json()['code']))
            Test_result = 'Pass'
        except AssertionError as e:
            Test_result = 'Failed'
            my_logger.error('出错了,{0}'.format(e))
            raise e

        if resp.get_cookie():
            Cookies = resp.get_cookie()

        my_logger.info('执行本条用例测试结果:{0}'.format(Test_result))

        # 数据验证
        # 当加标成功，根据借款人Id查询数据库load表是否有一条项目记录
        if resp.get_json()['msg'] =='加标成功':
            expected = case.data
            seek_load_sql = 'select * from future.loan where MemberID={0} ORDER BY CreateTime DESC;'.format(
                Context.borrow_member_id)
            loan = self.mysql.fetch_one(seek_load_sql)
            if loan:   # 查询标的记录非空
                actual = {'memberId':str(loan['MemberID']),'title':loan['Title'],'amount':int(loan['Amount']),'loanRate':float(loan['LoanRate']),'loanTerm':loan['LoanTerm'],'loanDateType':loan['LoanDateType'],
                          'repaymemtWay':loan['RepaymemtWay'],'biddingDays':loan['BiddingDays']}
                self.assertDictEqual(expected, actual)
                my_logger.info('加标成功！查询load表新增一条项目记录')
            else:    # 如果查询标的记录为空，测试不通过
                raise AssertionError


    def tearDown(self):
        self.mysql.close()




