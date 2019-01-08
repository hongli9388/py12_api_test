# -*- coding: utf-8 -*-
# @time     : 2019/1/5 0005 下午 16:33
# @Author   : yuxuan
# #file     : test_payment.py
# 待测点：
# 1正确用户信息，扣款成功
# 2.正确用户信息，扣款失败
# 3.超时再请求成功
# 4.超时再请求失败


import unittest
from learn_mock.payment import Payment
from unittest import mock

class TestPayment(unittest.TestCase):

    def setUp(self):
        self.payment = Payment()

    def test_success(self):
        # 模拟payment.requestOutoSystem的返回值是200
        self.payment.requestOutoSystem = mock.Mock(return_value=200)
        resp = self.payment.dopay(user_id='1101', card_num='123456', amount=100)
        self.assertEqual('Success', resp, '测试支付成功')

    def test_fail(self):
        # 模拟payment.requestOutoSystem的返回值是200
        self.payment.requestOutoSystem = mock.Mock(return_value=500)
        resp = self.payment.dopay(user_id='1102', card_num='1234567900', amount=10000)
        self.assertEqual('Fail', resp, '测试支付失败')

    def test_retry_success(self):
        # 模拟payment.requestOutoSystem的返回超时再请求成功是(TimeoutError,200)
        self.payment.requestOutoSystem = mock.Mock(return_value=500, side_effect=[TimeoutError, 200])   # return_value不起作用，side_effect必须是可迭代对象，按下标取值
        resp = self.payment.dopay(user_id='1103', card_num='1234562578', amount=2000)
        self.assertEqual('Success', resp, '测试支付成功')
        print('模拟对象是否被调用',self.payment.requestOutoSystem.called)
        print('模拟对象被调用的次数', self.payment.requestOutoSystem.call_count)
        print('最近一次调用传的参数', self.payment.requestOutoSystem.call_args)
        self.payment.requestOutoSystem.assert_called_with('1234562578', 2000)   # 断言调用参数是否正确,要用位置传参

    def test_retry_fail(self):
        # 模拟payment.requestOutoSystem的返回超时再请求失败是(TimeoutError,200)
        self.payment.requestOutoSystem = mock.Mock(side_effect=[TimeoutError,500])  # return_value不起作用，side_effect必须是可迭代对象，按下标取值
        resp = self.payment.dopay(user_id='1105', card_num='12345100078', amount=5000)
        self.assertEqual('Fail', resp, '测试支付失败')
        print('模拟对象是否被调用', self.payment.requestOutoSystem.called)
        print('模拟对象被调用的次数', self.payment.requestOutoSystem.call_count)
        print('最近一次调用传的参数', self.payment.requestOutoSystem.call_args)
        # self.payment.requestOutoSystem.assert_has_calls()
        self.assertEqual(2, self.payment.requestOutoSystem.call_count)    #断言被调用2次


    def tearDown(self):
        pass

