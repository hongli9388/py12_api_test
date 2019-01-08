# -*- coding: utf-8 -*-
# @time     : 2019/1/1 0002 下午 14:54
# @Author   : yuxuan
# #file     : run_test_case.py

# 运行所有的接口测试用例

import unittest
from testcases.test_recharge import TestRecharge
from common import contants
from common import project_path
import HTMLTestRunnerNew

#方法一：需要一个一个接口功能加载
# suite = unittest.TestSuite()
# loader = unittest.TestLoader()
# suite.addTest(loader.loadTestsFromTestCase(TestRecharge))
# with open(contants.report_dir,'wb+') as file:
#     runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, title='前程贷充值接口测试', description='完成用户充值操作',tester='yuxuan')
#     runner.run(suite)

#方法二：  指定从testcases目录中匹配去找,可以一次执行所有用例
discover = unittest.defaultTestLoader.discover(project_path.test_dir, pattern='test*.py', top_level_dir=None)  # 如果只有一级目录指定为none
with open(contants.report_dir,'wb+') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, title='前程贷充值接口测试', description='完成用户充值操作',tester='yuxuan')
    runner.run(discover)


