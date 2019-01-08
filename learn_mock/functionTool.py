# -*- coding: utf-8 -*-
# @time     : 2019/1/7 0007 下午 12:36
# @Author   : yuxuan
# #file     : functionTool.py

# 自己写一个类，然后使用mock模拟调用这个类的属性，和方法，增加一些断言

# 计算工具类
class FunctionTool:

    def add(self, a, b):
        add = a+b
        multiplication = self.multiplication(a, b)
        return (add, multiplication)


    def  multiplication(self,a, b):
        return a*b






