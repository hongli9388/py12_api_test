# -*- coding: utf-8 -*-
# @time     : 2019/1/7 0007 下午 13:46
# @Author   : yuxuan
# #file     : test_mock_demo.py


# 自己写一个类，然后使用mock模拟调用这个类的属性，和方法，增加一些断言
import unittest
from unittest import mock
from unittest.mock import patch
from learn_mock.functionTool import FunctionTool


class TestToolDemo(unittest.TestCase):

    def setUp(self):
        self.func_tool = FunctionTool()

    @mock.patch.object(FunctionTool,'multiplication')
    def test_tool_demo(self,mock_multiply):
        mock_multiply.return_value = 10





    def tearDown(self):
        pass
