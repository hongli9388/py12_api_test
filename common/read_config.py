# -*- coding: utf-8 -*-
# @time     : 2018/12/14 0014 下午 22:45
# @Author   : yuxuan
# #file     : read_config.py

# 读取配置文件
import configparser
import os
from common import contants
class ReadConfig:

    def __init__(self):
        self.cf = configparser.ConfigParser()
        file_name = os.path.join(contants.conf_dir,'global.conf')
        self.cf.read(filenames=file_name, encoding='utf-8')
        if self.get_bool('switch','on'):   # 如果为True，获取第一套环境信息,否则读取第二套环境信息
            test_env_1_name = os.path.join(contants.conf_dir, 'test_env_1.conf')
            self.cf.read(filenames=test_env_1_name)
        else:
            test_env_2_name = os.path.join(contants.conf_dir, 'test_env_2.conf')
            self.cf.read(filenames=test_env_2_name)


    def get(self, section, option):    # 返回str类型的值
        return self.cf.get(section,option)

    def get_bool(self,section,option):    # 返回bool类型的值
        return self.cf.getboolean(section,option)

    def get_int(self,section,option):    # 返回int类型的值
        return self.cf.getint(section,option)

    def get_float(self,section,option):    # 返回float类型的值
        return self.cf.getfloat(section,option)

    #将数据写入配置文件中
    def write_value(self, section, option, value):
        file_name = os.path.join(contants.conf_dir, 'global.conf')
        self.cf.read(filenames=file_name, encoding='utf-8')
        if self.get_bool('switch', 'on'):
            # self.cf.add_section(section)
            self.cf.set(section, option, value)
            test_env_1_name = os.path.join(contants.conf_dir, 'test_env_1.conf')
            self.cf.write(open(test_env_1_name, 'w'))
        else:
            # self.cf.add_section(section)
            self.cf.set(section, option, value)
            test_env_2_name = os.path.join(contants.conf_dir, 'test_env_2.conf')
            self.cf.write(open(test_env_2_name, 'w'))







if __name__ == '__main__':

    config = ReadConfig()
    url_pre = config.get('test_api', 'url_pre')
    print(type(url_pre),url_pre)
    # config.write_value('MobilePhone', 'max_phone', '18999999599')
    # s = ReadConfig().get('basic', 'normal_phone')
    # print(s)
























