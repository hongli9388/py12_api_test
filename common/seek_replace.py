# -*- coding: utf-8 -*-
# @time     : 2018/12/22 0022 下午 22:00
# @Author   : yuxuan
# #file     : seek_replace.py

import re
from common.read_config import ReadConfig
import json

# 正则表达式完成字符串的查找


# s = 'world hello'
# pattern = 'hello'
# res = re.match(pattern=pattern, string=s)   #match查找最开始位置
# print(res)
# res1 = re.findall(pattern=pattern, string=s)   #findall查找所有位置，返回列表
# print(res1)
# res2 = re.search(pattern=pattern,string=s)   #search从任意位置找
# print(res2)

# s1 = '{"mobilephone":"${normal_phone}","pwd":"1234abcd"}'  #目标字符串
# resp = re.findall(pattern='(\d{11})',string=s1)     #pattern可以为:(\d{11})
# resp2 = re.findall(pattern='\$\{(.*?)\}',string=s1)[0]
# mobilephone = resp[0]
# ss = s1.replace(mobilephone,'18655668989')
# print(ss)
# print(resp2)

import re
from common.read_config import ReadConfig
import json

class SeekReplace:

    def seek_replace(self, target):
        p = '\$\{(.*?)\}'#正则搜索匹配到${normal_phone}
        max_phone = ReadConfig().get('MobilePhone','max_phone')
        print(max_phone)
        resp = re.sub(p,max_phone,target)
        return resp




# if __name__ == '__main__':
    # target = '{"mobilephone":"${normal_phone}","pwd":"1234abcd"}'
    # p = '\$\{(.*?)\}'  # 正则搜索匹配到${normal_phone}
    # max_phone = ReadConfig().get('MobilePhone','max_phone')
    # res = SeekReplace().seek_replace(target)
    # print(res)












#
# s = '{"mobilephone":"${normal_phone}","pwd":"${pwd}"}'
# p = '\$\{(.*?)\}'
# while re.search(p,s):  # 在目标字符串找到就循环
#     resp5 = re.search('\$\{(.*?)\}',s)
#     print(resp5.group())
#     print(resp5.group(1))   #取第一个分组里面的字符，也就是context里面的key
#     key = resp5.group(1)
#     from common.basic_data import Context
#     user = getattr(Context,key)
#     print(user)
#     s = re.sub(p,user,s,count=1)
#     print(s)
#







    # def seek_replace(self, old_str):
    #     s = old_str
    #     s1 = re.findall(pattern='(\$\{.*?\})', string=s)[0]   #正则搜索匹配到${normal_phone}
    #     normal_phone = ReadConfig().get('MobilePhone','normal_phone')
    #     ss = s.replace(str(s1), normal_phone)
    #     return ss
