#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/19
"""
配置信息模块
"""
import os
import logging
# 主路径
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置文件路径
CONF_DIR = os.path.join(BASEDIR, "conf")

# 数据库配置信息文件路径
DATABASE_INFO_PATH = os.path.join(CONF_DIR, "database_info.json")

# 马甲信息文件路径
MAJIA_PATH = os.path.join(CONF_DIR, "majia.json")

# sql文件路径
SQL_FILE_DIR = os.path.join(BASEDIR, "db", "sql_file")

# 日志路径
ACTION_LOG_PATH = os.path.join(BASEDIR, "log", "action.log")

# 设置日志输出级别
LOG_LEVEL = {
            "global_level": logging.INFO,
            "ch_level": logging.WARNING,
            "fh_level": logging.INFO
            }

# 图标路径
ICO_PATH = os.path.join(BASEDIR, "db", "ico", "kool.ico")

# 作者
AUTHOR = "Breakering"

# 版本
VERSION = "0.2.0"

# 日报输出路径
RIBAO_DIR = os.path.join(BASEDIR, "output", "日报输出")

# 周报输出路径
ZHOUBAO_DIR = os.path.join(BASEDIR, "output", "周报输出")

# 主要文件匹配路径
MAIN_FILE_PATH = os.path.join(BASEDIR, "conf", "main_file")
if __name__ == '__main__':
    print(BASEDIR)
