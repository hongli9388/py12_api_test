# -*- coding: utf-8 -*-
# @time     : 2019/1/1 0001 下午 15:42
# @Author   : yuxuan
# #file     : test_audit.py

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
cases = do_excel.get_case('audit')
my_logger = MyLog()
Cookies = None


@ddt
class TestAudit(unittest.TestCase):

    def setUp(self):
        self.mysql = MysqlTool()

    @data(*cases)
    def test_audit(self, case):
        global Cookies
        my_logger.info('正在执行第{0}条用例{1}'.format(case.case_id, case.title))
        url = ReadConfig().get('test_api','url_pre') + case.url
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
            my_logger.error('出错了{0}'.format(e))
            raise e

        if resp.get_cookie():
            Cookies = resp.get_cookie()

        my_logger.info('执行本条用例测试结果:{0}'.format(Test_result))

        # 数据验证
        # 当加标成功，根据借款人Id查询数据库load表是否有一条项目记录
        if resp.get_json()['msg'] == '加标成功':
            expected = data
            seek_load_sql = 'select * from future.loan where MemberID={0} ORDER BY CreateTime DESC;'.format(
                Context.borrow_member_id)
            loan = self.mysql.fetch_one(seek_load_sql)
            if loan:  # 查询标的记录非空
                actual = {'memberId': str(loan['MemberID']), 'title': loan['Title'], 'amount': int(loan['Amount']),
                          'loanRate': int(loan['LoanRate']), 'loanTerm': loan['LoanTerm'],
                          'loanDateType': loan['LoanDateType'],
                          'repaymemtWay': loan['RepaymemtWay'], 'biddingDays': loan['BiddingDays']}
                self.assertDictEqual(expected, actual)
                my_logger.info('加标成功！查询load表新增一条项目记录')
                setattr(Context,'loanId',str(loan['Id']))
            else:  # 如果查询标的记录为空，测试不通过
                raise AssertionError

        # 当审核通过，验证数据库表中loan表Status字段
        if resp.get_json()['msg'] == '更新状态成功：竞标开始，当前标为竞标中状态':
            seek_load_sql = 'select * from future.loan where MemberID={0} ORDER BY CreateTime DESC;'.format(ReadConfig().get('basic', 'borrow_member_id'))
            loan_status = self.mysql.fetch_one(seek_load_sql)['Status']
            if loan_status:  #查询非空
                self.assertEqual(4, loan_status)
                my_logger.info('新增标的审核通过!数据库loan表Status字段更改为4正确')
            else:
                raise AssertionError


    def tearDown(self):
        self.mysql.close()





