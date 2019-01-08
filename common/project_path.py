# -*- coding: utf-8 -*-
# @time     : 2018/12/14 0014 下午 22:58
# @Author   : yuxuan
# #file     : project_path.py

# 项目路径
import os
# 基础路径
base_path=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

#配置文件
conf_path=os.path.join(base_path,'conf','test_api.conf')

# 测试数据
data_path=os.path.join(base_path,'datas','py12前程贷接口测试数据.xlsx')

# 本地日志
log_path=os.path.join(base_path,'log','test_api_log.txt')

# 测试报告
report_path=os.path.join(base_path,'reports','py12前程贷接口测试报告.html')

#测试用例目录
test_dir = os.path.join(base_path,'testcases')




