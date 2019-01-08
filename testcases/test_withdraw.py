# -*- coding: utf-8 -*-
# @time     : 2019/1/2 0002 下午 13:25
# @Author   : yuxuan
# #file     : test_withdraw.py


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


# 取现

do_excel = DoExcel(contants.data_dir)
cases = do_excel.get_case('withdraw')
my_logger = MyLog()

@ddt
class TestWithDraw(BaseCase):


    def setUp(self):
        self.mysql = MysqlTool()
        # 取现前用户可用余额
        self.seek_leaveamount_sql = 'SELECT LeaveAmount FROM future.member where MobilePhone={0};'.format(Context.normal_phone)
        self.before_amount = self.mysql.fetch_one(self.seek_leaveamount_sql)['LeaveAmount']   # 取现前用户可用余额

    @data(*cases)
    def test_withdraw(self, case):
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
        #  提现成功后，用户的可用余额减少
        if resp.get_json()['msg'] == '取现成功':
            withdraw_amount = data['amount']   # 取现金额
            actual = float(self.mysql.fetch_one(self.seek_leaveamount_sql)['LeaveAmount'])   # 提现后金额
            expected = float(self.before_amount) - float(withdraw_amount)   # 提现前用户可用金额 - 提现金额
            self.assertEqual(expected,actual)
            setattr(Context,'after_withdraw_mount',actual)   # 提现后金额放上下文中，为后面查流水记录准备
            my_logger.info('提现成功后!查询数据库member表中用户减少余额和提现金额一致')

            # 验证新增一条流水记录
            seek_financeLog_sql = 'SELECT * FROM future.financelog where PayMemberId={0}  and Amount={1} ' \
                                  'and PayMemberMoney={2} ORDER BY CreateTime DESC;'.format(Context.memberId,data['amount'],getattr(Context,'after_withdraw_mount'))
            seek_financeLog = self.mysql.fetch_one(seek_financeLog_sql)
            my_logger.info(seek_financeLog)
            if seek_financeLog is not None:
                expected = {'PayMemberId':int(Context.memberId), 'Amount': int(data['amount']),'PayMemberMoney': float(getattr(Context, 'after_withdraw_mount'))}
                actual = {'PayMemberId': seek_financeLog['PayMemberId'], 'Amount': int(seek_financeLog['Amount']),'PayMemberMoney': float(seek_financeLog['PayMemberMoney'])}
                self.assertEqual(expected,actual)
                my_logger.info('查询financeLog表新增流水记录与提现请求参数一致')
            else:
                raise AssertionError

        else:   # 提现失败，用户可用余额不变
            actual = float(self.mysql.fetch_one(self.seek_leaveamount_sql)['LeaveAmount'])  # 提现后可用余额
            expected = float(self.before_amount)    # 提现前可用余额
            self.assertEqual(expected,actual)

    def tearDown(self):
        self.mysql.close()








