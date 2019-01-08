# -*- coding: utf-8 -*-
# @time     : 2018/12/27 0027 下午 22:41
# @Author   : yuxuan
# #file     : test_invest.py

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
cases = do_excel.get_case('invest')
my_logger = MyLog()
Cookies = None

@ddt
class TestInvest(unittest.TestCase):


    def setUp(self):

        self.mysql = MysqlTool()
        # 投资前用户余额
        self.seek_mount = ReadConfig().get('SQL', 'LeaveAmount')
        self.leaveamount1 = self.mysql.fetch_one(self.seek_mount)['LeaveAmount']   # 投资前余额
        my_logger.info('投资前用户账户余额:{0}'.format(self.leaveamount1))


    @data(*cases)
    def test_invest(self, case):
        my_logger.info('目前正在执行第{0}条用例:{1}'.format(case.case_id, case.title))
        my_logger.info('----------开始检查请求url地址------------')
        global Cookies
        url = ReadConfig().get('test_api', 'url_pre') + case.url
        my_logger.info(url)
        my_logger.info('-------------开始检查请求数据-----------')
        global data
        data = DoRegex().replace(case.data)
        data = json.loads(data)
        my_logger.info(data)
        my_logger.info('----------开始http接口请求----------')
        resp = HttpRequest(method=case.method, url=url, data=data, cookies=Cookies)
        my_logger.info('----------结束http接口请求----------')
        my_logger.info('请求结果是{0}'.format(resp.get_json()))
        try:
            self.assertEqual(case.expected,int(resp.get_json()['code']))
            Test_result = 'Pass'
        except AssertionError as e:
            my_logger.error('出错了，{0}'.format(e))
            Test_result = 'Failed'
            raise e

        if resp.get_cookie():   # 如果cookies非空
            Cookies = resp.get_cookie()

        my_logger.info('本条用例执行结果:{0}'.format(Test_result))

        # 数据验证
        #  当创建标的成功，根据借款人Id查询数据库load表是否添加一条记录
        if resp.get_json()['msg'] =='加标成功':
            seek_load_sql = 'select * from future.loan where MemberID={0} ORDER BY CreateTime DESC;'.format(Context.borrow_member_id)
            loan = self.mysql.fetch_one(seek_load_sql)
            actual = {'memberId':str(loan['MemberID']),'title':loan['Title'],'amount':int(loan['Amount']),'loanRate':float(loan['LoanRate']),'loanTerm':loan['LoanTerm'],'loanDateType':loan['LoanDateType'],
                      'repaymemtWay':loan['RepaymemtWay'],'biddingDays':loan['BiddingDays']}

            if loan:
                self.assertDictEqual(data, actual)  # 字典多个字段同时验证是否一致
                my_logger.info('创建标的成功，查询数据库loan表与请求参数一致')
                setattr(Context, 'loanId', str(loan['Id']))  #将新建的标的id放入上下文中，为后面审核和投资用例正则替换准备
            else:
                raise AssertionError   # 如果查询数据库为空，测试不通过
        # 当审核通过，验证数据库表中loan表Status字段更改
        if resp.get_json()['msg'] == '更新状态成功：竞标开始，当前标为竞标中状态':
            seek_load_sql = 'select * from future.loan where MemberID={0} ORDER BY CreateTime DESC;'.format(ReadConfig().get('basic', 'borrow_member_id'))
            loan_status = self.mysql.fetch_one(seek_load_sql)['Status']
            if loan_status:  #查询非空
                self.assertEqual(4, loan_status)
                my_logger.info('新增标的审核通过!数据库loan表Status字段更改为4正确')
            else:
                raise AssertionError
        # 投资成功，验证数据库是否生成投资记录、用户余额减少、新增一条流水记录
        if resp.get_json()['msg'] == '竞标成功':
            invest_mount = data['amount']    # 投资金额
            # 查投资后用户账户余额
            actual = float(self.mysql.fetch_one(self.seek_mount)['LeaveAmount'])  # 投资后用户余额
            setattr(Context,'after_invest_mount', actual)   # 投资后金额放入上下文,为后面查流水记录准备
            expected = float(self.leaveamount1) - float(invest_mount)   # 投资前用户余额 - 投资金额
            self.assertEqual(expected, actual)
            my_logger.info('投资成功!查询数据库member表用户账户减少余额和投资金额一致')
            # 查投资记录invest表是否有记录
            seek_invest_sql = 'SELECT * FROM future.invest where MemberID={0} and LoanId ={1} and Amount={2} ' \
            'ORDER BY CreateTime DESC;'.format(ReadConfig().get('basic', 'memberId'), getattr(Context,'loanId'), data['amount'])
            invest_record = self.mysql.fetch_one(seek_invest_sql)
            if invest_record:   # 如果数据库查询有记录  ，判断数据库中记录与请求参数是否一致
                expected = {'MemberID':int(data['memberId']), 'LoanId':int(data['loanId']), 'Amount':int(data['amount'])}
                actual = {'MemberID':invest_record['MemberID'], 'LoanId':invest_record['LoanId'], 'Amount':invest_record['Amount']}
                self.assertDictEqual(expected,actual)
                my_logger.info('invest表新增一条记录与请求参数一致')
                #查流水记录表financeLog是否有记录
                seek_financeLog_sql = 'SELECT * FROM future.financelog where PayMemberId={0} and IncomeMemberId={1} and Amount={2} ' \
                                  'and PayMemberMoney={3} ORDER BY CreateTime DESC;'.format(Context.memberId,Context.borrow_member_id, data['amount'], getattr(Context,'after_invest_mount'))
                seek_financeLog = self.mysql.fetch_one(seek_financeLog_sql)
                if seek_financeLog:  #如果查询流水记录表有数据
                    expected ={'PayMemberId':int(data['memberId']), 'Amount':int(data['amount']), 'IncomeMemberId':int(Context.borrow_member_id), 'PayMemberMoney':float(getattr(Context,'after_invest_mount'))}
                    actual = {'PayMemberId':seek_financeLog['PayMemberId'], 'Amount':int(seek_financeLog['Amount']), 'IncomeMemberId':seek_financeLog['IncomeMemberId'], 'PayMemberMoney':float(seek_financeLog['PayMemberMoney'])}
                    self.assertDictEqual(expected,actual)
                    my_logger.info('查询financeLog表新增流水记录与投资请求参数一致')
                else:    # 如果查询流水记录表为空
                    raise AssertionError
            else:
                raise AssertionError

        else:    # 投资失败 ，用户余额不变
            actual = float(self.mysql.fetch_one(self.seek_mount)['LeaveAmount'])  # 投资后用户余额
            expected = float(self.leaveamount1)    #投资前用户余额
            self.assertEqual(expected, actual)


    def tearDown(self):
        self.mysql.close()







