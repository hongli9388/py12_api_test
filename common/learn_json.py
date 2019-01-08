# -*- coding: utf-8 -*-
# @time     : 2018/12/18 0018 下午 21:50
# @Author   : yuxuan
# #file     : learn_json.py

import json
# str_test = '{"status":0,"code":"20111","data":null,"msg":"用户名或密码错误"}'
# str2 = '{"a":[1,2],"b":["c","d"]}'  #json是一个跨语言的数据类型，python,Java,C
# json字符串转dict
# dict_test = json.loads(str2)
# print(type(dict_test))
# print(dict_test['msg'])
# print(type(dict_test))


# python中字典序列化成json的字符串
# dict_obj={"status":0,"code":"20111","data":None,"msg":"用户名或密码错误"}
# str_obj=json.dumps(dict_obj,ensure_ascii=False,indent=4)   #加入到日志中，返回成json格式缩进便于查看
# print(str_obj)

# dump将字典写入到文件，序列化成json字符串
dict_obj = {"status":0,"code":"20111","data":None,"msg":"用户名或密码错误"}
f = open('../datas/data.json','w+')
json.dump(dict_obj,f)

# load将文件里面的json反序列化成dict
# f = open('../datas/data.json')
# d=json.load(f)
# print(type(d))
