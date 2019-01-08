# -*- coding: utf-8 -*-
# @time     : 2019/1/5 0005 下午 16:11
# @Author   : yuxuan
# #file     : payment.py
import requests

class Payment:   # 支付类
    def requestOutoSystem(self, card_num, amount):

        """请求第三方外部支付接口，并返回响应码
        :param  card_num:
        :param  amount:
        :return  :返回状态码， 200 代表支付成功， 500代表支付异常失败"""
        url = 'http://192.168.2.222.payment.com'
        data = {"card_num":card_num, "amount":amount}
        resp = requests.post(url,data)
        return resp.status_code    # 返回状态码


    def dopay(self, user_id, card_num, amount):
        # user_id 用户id，card_num 卡号,amount 金额

        try:    #调用第三方支付接口
            resp = self.requestOutoSystem(card_num, amount)
        except TimeoutError:   # 如果超时再重新调用一次
            resp = self.requestOutoSystem(card_num, amount)

        if resp == 200:
            print('{0}支付{1}成功!进行扣款并有支付记录'.format(user_id, amount))
            return 'Success'

        elif resp == 500:
            print('{0}支付{1}失败!不进行扣款'.format(user_id, amount))
            return 'Fail'

