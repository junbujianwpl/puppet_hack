import os
import sys

import logbook
from logbook import Logger, StreamHandler, FileHandler

import time

logbook.set_datetime_format('local')

default_log_path = "d:/yjb_log/"


class DefaultLogHandler(object):
    """默认的 Log 类"""

    def __init__(self, name='default', log_type='stdout', file_path=default_log_path, loglevel='DEBUG'):
        """Log对象
        :param name: log 名字
        :param :logtype: 'stdout' 输出到屏幕, 'file' 输出到指定文件
        :param :filename: log 文件名
        :param :loglevel: 设定log等级 ['CRITICAL', 'ERROR', 'WARNING', 'NOTICE', 'INFO', 'DEBUG', 'TRACE', 'NOTSET']
        :param :dir_path: 文件夹路径
        :return log handler object
        """
        self.log = Logger(name)
        if log_type == 'stdout':
            StreamHandler(sys.stdout, level=loglevel).push_application()
        if log_type == 'file':
            date = time.strftime("%Y%m%d", time.localtime())
            # 一天对应一个文件夹
            file_path = "%s%s/" % (file_path, date)
            file_path_final = "%s%s-%s.log" % (file_path, date, name)
            print(file_path)
            if file_path[-1] == '/' and not os.path.exists(file_path):
                os.makedirs(os.path.dirname(file_path))
            file_handler = FileHandler(file_path_final, level=loglevel)
            self.log.handlers.append(file_handler)

    def __getattr__(self, item, *args, **kwargs):
        return self.log.__getattribute__(item, *args, **kwargs)


my_logger = DefaultLogHandler("yjb_log", "file").log
