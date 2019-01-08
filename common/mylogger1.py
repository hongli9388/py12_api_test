# -*- coding: utf-8 -*-
# @time     : 2019/1/2 0002 下午 19:47
# @Author   : yuxuan
# #file     : mylogger1.py


import logging
from common.read_config import ReadConfig
from common import contants
import os
import time

# 定义一个日志收集器
logger = logging.getLogger(ReadConfig().get('LOGS','logger_name'))
#设置收集级别
logger.setLevel('DEBUG')

# 设置handler
def set_handler(levels):
    if levels == 'error':  # 如果是error就添加到error的handler
        logger.addHandler(MyLog.error_handler)
    else:   # 其他添加到info的handler
        logger.addHandler(MyLog.info_handler)
    logger.addHandler(MyLog.ch)   # 全部输出添加到console

# 去重handler
def remove_handler(levels):
    if levels == 'error':
        logger.removeHandler(MyLog.error_handler)
    else:
        logger.removeHandler(MyLog.info_handler)
    logger.removeHandler(MyLog.ch)


# 获取当天日志存放目录
def get_log_dir():
    log_dir = os.path.join(contants.log_dir,get_current_date())
    if not os.path.isdir(log_dir):    # 判断目录是否存在
        os.mkdir(log_dir)   # 不存在就创建
    return log_dir   # 存在就返回log_dir


# 获取当天时间
def get_current_date():
    return time.strftime('%Y%m%d', time.localtime(time.time()))


class MyLog:
    log_dir = get_log_dir()
    # 输出文件
    info_file = os.path.join(log_dir,'info.log')
    error_file = os.path.join(log_dir,'error.log')
    #输出格式
    formatter = logging.Formatter(ReadConfig().get('LOGS', 'export_formatter'))
    #输出渠道
    # 控制台
    ch = logging.StreamHandler()
    ch.setLevel('DEBUG')
    ch.setFormatter(formatter)

    # info文件输出
    info_handler = logging.FileHandler(filename=info_file,encoding='utf-8')
    info_handler.setLevel('INFO')
    info_handler.setFormatter(formatter)
    # ERROR文件
    error_handler = logging.FileHandler(filename=error_file,encoding='utf-8')
    error_handler.setLevel('ERROR')
    error_handler.setFormatter(formatter)

    #报表日志输出

    @staticmethod
    def debug(msg):
        set_handler('debug')
        logger.debug(msg)
        remove_handler('debug')

    @staticmethod
    def info(msg):
        set_handler('info')
        logger.info(msg)
        remove_handler('info')

    @staticmethod
    def error(msg):
        set_handler('error')
        logger.error(msg, exc_info=True)   # 同时输出异常信息
        remove_handler('error')















