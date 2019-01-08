# -*- coding: utf-8 -*-
# @time     : 2018/12/22 0022 下午 17:12
# @Author   : yuxuan
# #file     : do_mysql_tool.py

# 1.连接数据库 ，查询数据最大的手机号，得到返回   --查询后的数据放在一个地方
# 2.测试数据替换  ---字符串的查找+1并替换
# 3.然后再去请求   （以上整个过程手机号替换，是在测试用例执行期间完成查询、替换）

# 1.连接数据库
#2. 编写一个sql
#3.创建游标
# 4.执行excute

import pymysql
from common.read_config import ReadConfig


class MysqlTool:

    #连接数据库放在初始化函数里
    def __init__(self):
        host = ReadConfig().get('mysql','host')
        post = ReadConfig().get_int('mysql', 'post')   #post是一个数值，用getint()方法获取
        usr = ReadConfig().get('mysql', 'usr')
        pwd = ReadConfig().get('mysql', 'pwd')
        try:
            self.db = pymysql.connect(host=host, user=usr, password=pwd, port=post,cursorclass=pymysql.cursors.DictCursor)
        except ConnectionRefusedError as e:
            print('mysql数据库连接错误')
            raise e

    def fetch_one(self, sql):  #根据sql查询数据并返回
        cursor = self.db.cursor()   #建立一个游标

        cursor.execute(sql)   #游标根据sql查询
        data = cursor.fetchone()   #这里需要返回一条数据
        # self.db.close()    #查询完关闭连接数据库
        return data

    def fetch_all(self, sql):
        cursor = self.db.cursor()

        cursor.execute(sql)
        data = cursor.fetchall()  # 返回所有数据
        return data


    def close(self):
        self.db.close()

# if __name__ == '__main__':
    # sql = ReadConfig().get('SQL','mobile_sql')
    # print(sql)
    # mysql_tool = MysqlTool()
    # result = mysql_tool.fetch_one(sql)
    # print(result[0])   # 返回元组，通过下标数字可读性查
    # print(result['MobilePhone'])   #建议返回为字典类型，通过key来取值
    # sql = ReadConfig().get('SQL', 'LeaveAmount')
    # sql = 'SELECT * FROM future.member where MobilePhone='18999999919';'
    # lm = mysql_tool.fetch_one(sql)
    # print(lm)














