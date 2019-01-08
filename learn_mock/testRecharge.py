# -*- coding: utf-8 -*-
# @time     : 2019/1/7 0007 下午 16:00
# @Author   : yuxuan
# #file     : testRecharge.py

# 2019.1.4作业
#测试mock模拟充值接口的返回


import unittest
from unittest import mock

from learn_mock.requests_recharge import Recharge
import json

class TestRecharge(unittest.TestCase):

    def setUp(self):
        self.recharge = Recharge()


    def test_success(self):
        # 测试充值接口返回成功
        self.recharge.requestsRecharge = mock.Mock(return_value={"status": 1,"code": "10001","data": {"id": 1113134,"regname": "小蜜蜂","pwd": "E10ADC3949BA59ABBE56E057F20F883E","mobilephone": "13456795500","leaveamount": "1000.00","type": "1","regtime": "2019-01-07 11:24:51.0"},"msg": "充值成功"})
        resp = self.recharge.do_recharge(memberId='1113134', mobilephone='13456795500', amount=1000)
        self.assertEqual('success', resp, '测试充值成功')


    def test_fail(self):
        # 测试充值接口返回失败
        self.recharge.requestsRecharge = mock.Mock(return_value=json.loads('{"status": 0,"code": "20104","data": null,"msg": "此手机号对应的会员不存在"}'))
        resp = self.recharge.do_recharge(memberId='111305', mobilephone='13055251020', amount=500)
        self.assertEqual('fail', resp, '测试充值失败')


    def test_retry_success(self):
        # 测试充值接口返回超时再成功
        self.recharge.requestsRecharge = mock.Mock(side_effect=[TimeoutError, {"status": 1,"code": "10001","data": {"id": 105790,"regname": "小蜜蜂","pwd": "E10ADC3949BA59ABBE56E057F20F883E","mobilephone": "15877556868","leaveamount": "5000.00","type": "1","regtime": "2019-01-07 11:24:51.0"},"msg": "充值成功"}])
        resp = self.recharge.do_recharge(memberId='105790', mobilephone='15877556868', amount=5000)
        print('是否被调用过:', self.recharge.requestsRecharge.called)
        print('被调用的次数:', self.recharge.requestsRecharge.call_count)
        resp_call = [mock.call.self.recharge.requestsRecharge('15877556868', 5000), mock.call.self.recharge.requestsRecharge('15877556868', 5000)]
        self.recharge.requestsRecharge.assert_has_calls(resp_call)  # 断言按照列表中正确的方法和参数调用过2次
        self.assertEqual('success', resp)



    def test_retry_fail(self):
        # 测试充值接口返回超时再成功
        self.recharge.requestsRecharge = mock.Mock(side_effect=[TimeoutError, json.loads('{"status": 0,"code": "20109","data": null,"msg": "手机号码格式不正确"}')])
        resp = self.recharge.do_recharge(memberId='120091', mobilephone='130558955687', amount=2000)
        print('是否被调用过:', self.recharge.requestsRecharge.called)
        print('被调用的次数:',self.recharge.requestsRecharge.call_count)
        resp_call = [mock.call.self.recharge.requestsRecharge('130558955687', 2000),
                     mock.call.self.recharge.requestsRecharge('130558955687', 2000)]
        self.recharge.requestsRecharge.assert_has_calls(resp_call)  # 断言按照列表中正确的方法和参数调用过2次
        self.assertEqual('fail', resp)


    def tearDown(self):
        pass


