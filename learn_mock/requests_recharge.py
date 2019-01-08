# -*- coding: utf-8 -*-
# @time     : 2019/1/6 0006 下午 23:10
# @Author   : yuxuan
# #file     : requests_recharge.py

# 使用mock模拟充值接口的返回
import requests

class Recharge:


    def requestsRecharge(self, mobilephone, amount):
        # 充值接口
        url = 'http://test.lemonban.com/futureloan/mvc/api/member/recharge'
        data = {"mobilephone":mobilephone, "amount":amount}
        resp = requests.post(url, data)
        return resp.json()   # 返回请求json字符串


    def do_recharge(self, memberId, mobilephone, amount):
        # memberId 用户id，mobilephone 手机号，amount 金额
        try:
            resp = self.requestsRecharge(mobilephone, amount)
        except TimeoutError:   #如果超时再请求一次
            resp = self.requestsRecharge(mobilephone, amount)

        if int(resp['code']) == 10001:
            print('{0}用户充值{1}成功，并同步保存有支付记录，用户可用余额增加！'.format(memberId,amount))
            return 'success'

        elif int(resp['code']) != 10001:
            print('{0}用户充值{1}失败，没有支付记录，账户可用余额未变动！'.format(memberId, amount))
            return 'fail'


