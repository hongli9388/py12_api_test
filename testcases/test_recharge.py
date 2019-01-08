# -*- coding: utf-8 -*-
# @time     : 2018/12/25 0025 下午 22:36
# @Author   : yuxuan
# #file     : test_recharge.py
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
# 读取配置文件基础数据--->放在context--->regex正则匹配替换---->request---拿到cookie放context cookie
# recharge接口---调用context数据--->充值完数据库校验

do_excel = DoExcel(contants.data_dir)
cases = do_excel.get_case('recharge')
mylogger = MyLog()

@ddt
class TestRecharge(unittest.TestCase):

    def setUp(self):    #获取期望结果放在setUp,充值前先取出leavemount
        sql = ReadConfig().get('SQL', 'LeaveAmount')
        global leavemount1
        global mysql
        mysql = MysqlTool()
        leavemount1 = mysql.fetch_one(sql)['LeaveAmount']
        mylogger.info('充值前账户余额:{0}'.format(leavemount1))
        return leavemount1


    @data(*cases)
    def test_recharge(self,case):

        mylogger.info('目前正在执行第{0}条用例:{1}'.format(case.case_id, case.title))
        mylogger.info('----------开始检查请求url地址------------')
        url = ReadConfig().get('test_api', 'url_pre') + case.url
        mylogger.info(url)
        #参数化处理
        mylogger.info('-------------开始检查请求数据-----------')
        global data
        data = DoRegex().replace(case.data)   #data由正则查找替换成配置文件中基础数据
        data = json.loads(data)
        mylogger.info('请求参数:{0}'.format(data))

        if hasattr(Context, 'cookies'):   #请求前判断Context类如果有cookies就获取值，否则cookies就为None
            cookies = getattr(Context, 'cookies')
        else:
            cookies = None

        mylogger.info('----------开始http接口请求----------')
        global resp
        resp = HttpRequest(method=case.method, url=url, data=data, cookies=cookies)
        mylogger.info('----------结束http接口请求----------')
        mylogger.info('请求结果是{0}'.format(resp.get_json()))
        #判断是否有cookie
        if resp.get_cookie():
            setattr(Context,'cookies',resp.get_cookie())    # 请求后如果有cookie就放在Context类中
        try:
            self.assertEqual(case.expected, int(resp.get_json()['code']))
            Test_result = 'Pass'
        except AssertionError as e:
            Test_result = 'Failed'
            mylogger.error('断言出错了{0}:'.format(e))
            raise e

        mylogger.info('本条用例执行测试结果{0}'.format(Test_result))


    # 完成数据校验，判断充值成功之后账户余额增加正确
    def tearDown(self):
        sql = ReadConfig().get('SQL', 'LeaveAmount')
        leavemount2 = mysql.fetch_one(sql)['LeaveAmount']
        mysql.close()
        mylogger.info('充值后账户余额:{0}'.format(leavemount2))
        if resp.get_json()['msg'] == '充值成功':
            recharge_mount = data['amount']
            mylogger.info('请求参数中充值金额:{0}'.format(recharge_mount))
            add_leavemount = leavemount2-leavemount1    #充值成功增加余额
            mylogger.info('账户余额增加金额:{0}'.format(add_leavemount))







