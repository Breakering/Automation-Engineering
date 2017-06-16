#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/2
import json
import os
from core.database_handle import MyHandle
from conf import settings


class MySelect(object):
    """封装查询类"""

    def __init__(self):
        self.database_info = None
        self.majia_info = None
        self.myhandle = None

    def get_info(self):
        self.database_info = json.load(open(settings.DATABASE_INFO_PATH, "r", encoding="utf-8"))
        self.majia_info = json.load(open(settings.MAJIA_PATH, "r", encoding="utf-8"))
        self.myhandle = MyHandle(self.database_info["host"], self.database_info["user"], self.database_info["passwd"],
                                 self.database_info["db"], self.database_info["port"], self.database_info["charset"])

    def select_data(self, customer, type_user, sqlname, start, end):
        """查询单次并返回所有结果信息"""
        self.get_info()
        sql_path = os.path.join(settings.SQL_FILE_DIR, customer, type_user, sqlname)
        if os.path.isfile(sql_path):
            sql = open(sql_path, "r", encoding="utf-8").read()
            sql = sql.format(start, end, self.majia_info["majia_kefu"], self.majia_info["majia_yonghu"])
            data = self.myhandle.chaxun(sql)
            return data
        else:
            return "sql语句不存在"

    def select_data_fields(self, customer, type_user, sqlname, start, end):
        """查询单次并返回所有结果信息"""
        self.get_info()
        sql_path = os.path.join(settings.SQL_FILE_DIR, customer, type_user, sqlname)
        if os.path.isfile(sql_path):
            sql = open(sql_path, "r", encoding="utf-8").read()
            sql = sql.format(start, end, self.majia_info["majia_kefu"], self.majia_info["majia_yonghu"])
            data, fields = self.myhandle.chaxun_all(sql)
            return data, fields
        else:
            data = "sql语句不存在"
            fields = None
            return data, fields
