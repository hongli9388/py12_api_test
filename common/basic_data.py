# -*- coding: utf-8 -*-
# @time     : 2018/12/25 0025 下午 21:21
# @Author   : yuxuan    上下文作用:从上面取到放在Context里面，下面要用,再从上下文取
# #file     : basic_data.py
import re
from common.do_mysql_tool import MysqlTool

#正则查找并替换
class DoRegex:

    @staticmethod    #不需要传递变量，属性共享，采用静态方法
    def replace(target):
        pattern = '\$\{(.*?)\}'
        while re.search(pattern, target):  # 在目标字符串找到就循环
            resp5 = re.search(pattern, target)
            key = resp5.group(1)   # 取第一个分组里面的字符，也就是context里面的key
            from common.basic_data import Context
            user = getattr(Context, key)
            target = re.sub(pattern, user, target, count=1)
        return target


from common.read_config import ReadConfig

class Context:
    config = ReadConfig()
    normal_phone = config.get('basic','normal_phone')   # 从配置文件读取放在context中
    pwd = config.get('basic','pwd')
    memberId = config.get('basic','memberId')
    password = config.get('basic','password')
    admin_user = config.get('basic', 'admin_user')
    admin_pwd = config.get('basic', 'admin_pwd')
    borrow_member_id = config.get('basic', 'borrow_member_id')
