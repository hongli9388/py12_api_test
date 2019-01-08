# -*- coding: utf-8 -*-
# @time     : 2018/12/16 0016 下午 13:02
# @Author   : yuxuan
# #file     : mylogger.py

# 封装logger   removeHandler
import logging
from common.read_config import ReadConfig
from common import contants
class MyLog:

    def my_log(self,level,msg):
        # 创建收集器
        my_logger = logging.getLogger(ReadConfig().get('LOGS', 'logger_name'))
        my_logger.setLevel(ReadConfig().get('LOGS', 'collect_level'))
        #输出格式
        formatter = logging.Formatter(ReadConfig().get('LOGS', 'export_formatter'))

        #控制台输出设置
        ch=logging.StreamHandler()
        ch.setLevel(ReadConfig().get('LOGS', 'console_handler_level'))
        ch.setFormatter(formatter)

        fh=logging.FileHandler(contants.log_path, encoding='utf-8')
        fh.setLevel(ReadConfig().get('LOGS', 'file_handler_level'))
        fh.setFormatter(formatter)

        my_logger.addHandler(ch)
        my_logger.addHandler(fh)

        if level == 'DEBUG':
            my_logger.debug(msg)
        elif level == 'INFO':
            my_logger.info(msg)
        elif level == 'ERROR':
            my_logger.error(msg)
        elif level == 'WARNING':
            my_logger.warning(msg)
        elif level == 'CRITICAL':
            my_logger.critical(msg)

        my_logger.removeHandler(ch)
        my_logger.removeHandler(fh)

    def debug(self,msg):
        self.my_log('DEBUG',msg)

    def info(self,msg):
        self.my_log('INFO',msg)

    def error(self,msg):
        self.my_log('ERROR',msg)

    def warning(self,msg):
        self.my_log('WARNING',msg)

    def critical(self,msg):
        self.my_log('CRITICAL',msg)











