#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/26
"""数据库处理模块"""
import pymysql


class MyHandle(object):

    def __init__(self, host, user, passwd, db, port, charset):
        self.host = host  # 主机地址
        self.user = user  # 用户名
        self.passwd = passwd  # 密码
        self.db = db  # 库名
        self.port = port  # 端口
        self.charset = charset  # 编码格式
        self.conn = None  # 一个链接
        self.cur = None  # 一个游标

    def __conn(self):
        """连接数据库"""
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db,
                                    port=self.port, charset=self.charset)  # 数据库连接信息
        self.cur = self.conn.cursor()  # 获取一个游标

    def __disconn(self):
        """断开连接"""
        self.cur.close()  # 关闭游标
        self.conn.close()  # 释放数据库资源
        self.conn = None  # 重置连接
        self.cur = None  # 重置游标

    def chaxun(self, sql):
        """查询单次并返回所有结果信息"""
        self.__conn()
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
        except Exception as e:
            data = "查询失败"
        finally:
            self.__disconn()
        return data

    def chaxun_all(self, sql):
        """查询单次并返回所有结果和字段信息"""
        self.__conn()  # 连接数据库
        try:
            self.cur.execute(sql)
            fields = self.cur.description  # 获取MYSQL里面的数据字段名称
            data = self.cur.fetchall()
        except Exception as e:
            fields = None
            data = "查询失败"
        finally:
            self.__disconn()
        return data, fields


