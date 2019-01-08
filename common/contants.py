# -*- coding: utf-8 -*-
# @time     : 2018/12/14 0014 下午 22:58
# @Author   : yuxuan
# #file     : contants.py

# 项目路径
import os
# 基础路径  ,项目的根目录
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#配置文件
conf_dir = os.path.join(base_path,'conf')

# 测试数据
data_dir = os.path.join(base_path,'datas\py12期前程贷接口测试数据.xlsx')

# 本地日志
log_path = os.path.join(base_path,r'log\test_recharge_log.txt')

log_dir = os.path.join(base_path,'log')
# 测试报告
report_dir = os.path.join(base_path,r'reports\test_recharge测试报告.html')
print(report_dir)





