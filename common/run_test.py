# -*- coding: utf-8 -*-
# @time     : 2018/12/20 0020 下午 23:34
# @Author   : yuxuan
# #file     : run_test.py
# 1，设计一个run_test 模块完成收集用例--执行用例--回写测试结果
# 2，封装配置文件读取类，根据环境设计配置文件，实现多套环境灵活切换,url修改成配置文件拼接


from common.do_excel import DoExcel
from common.http_requests_api import HttpRequest
from common.read_config import ReadConfig
from common import contants
import json

do_excel = DoExcel(contants.data_dir)
sheet_names = do_excel.get_sheet_names()
print('sheet 名称列表：', sheet_names)
case_list = ['register', 'login']  # 定义一个执行测试用例的列表
for sheet_name in sheet_names:
    if sheet_name in case_list:  # 如果sheet_name不在case_list列表里，就不执行
        cases = do_excel.get_case(sheet_name)
        print(sheet_name + '测试用例个数:', len(cases))
        for case in cases:
            # print('case信息:',case.__dict__)   # 使用__dict__方法，把每一个case元素放在字典里，打印case信息
            data = eval(case.data)
            url = ReadConfig().get('test_api','url_pre')+case.url    # url接口地址拼接
            # print('url接口地址:', url)
            req = HttpRequest(method=case.method, url=url, data=data)
            resp_dict = req.get_json()  # 获取请求响应，字典
            # 通过json.dumps函数将字典转换成字符串
            resp_text = json.dumps(req.get_json(), ensure_ascii=False, indent=4)
            print(resp_text)
            # 判断接口响应是否和excel里面的expected的值是否一致
            if case.expected == req.get_text():
                print('result:PASS')
                do_excel.write_by_case_id(sheet_name=sheet_name, case_id=case.case_id, actual=req.get_text(), result='PASS')
            else:
                print('result:FAILED')
                do_excel.write_by_case_id(sheet_name=sheet_name, case_id=case.case_id, actual=req.get_text(), result='FAILED')




