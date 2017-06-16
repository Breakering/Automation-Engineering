#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/6
"""各端模块"""
import threading
from tkinter import *                   # Tkinter模块，用于UI显示
from tkinter.ttk import *               # Tkinter显示加强模块
from tkinter import messagebox          # 消息弹窗模块
from conf import settings
import datetime
from core import myselect               # 简洁查询数据模块

# 获取昨天的日期
date1 = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), "%Y-%m-%d 00:00:00")
date2 = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), "%Y-%m-%d 23:59:59")

# 生成一个简洁查询数据实例
mychaxun = myselect.MySelect()

# 生成一个锁
geduan_lock = threading.Lock()


class GeDuan(object):
    """各端类"""

    def __init__(self):
        self.geduan_root = Tk()
        self.geduan_root.title("各端详情 by  %s version:%s" % (settings.AUTHOR, settings.VERSION))
        self.geduan_root.iconbitmap(settings.ICO_PATH)  # 设置图标
        self.frame = Frame(self.geduan_root)
        self.frame.pack(padx=8, pady=8, ipadx=4)
        Label(self.frame, text="请输入起始日期:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.start_date = StringVar()
        self.start_date.set(date1)
        Entry(self.frame, textvariable=self.start_date).grid(row=0, column=1, sticky='ew', padx=5, pady=5, columnspan=2)
        Label(self.frame, text="请输入终止日期:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.end_date = StringVar()
        self.end_date.set(date2)
        Entry(self.frame, textvariable=self.end_date).grid(row=1, column=1, sticky='ew', padx=5, pady=5, columnspan=2)
        self.biaoqian1 = StringVar()
        self.biaoqian1.set("各端投资")
        Label(self.frame, textvariable=self.biaoqian1).grid(row=3, column=0, padx=5, pady=5, sticky='ew')
        self.biaoqian2 = StringVar()
        self.biaoqian2.set("投资人数")
        Label(self.frame, textvariable=self.biaoqian2).grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.biaoqian3 = StringVar()
        self.biaoqian3.set("投资金额")
        Label(self.frame, textvariable=self.biaoqian3).grid(row=3, column=3, padx=5, pady=5, sticky='ew')
        self.D_1 = StringVar()
        self.D_1.set('APP')
        Label(self.frame, textvariable=self.D_1).grid(row=4, column=0, padx=5, pady=5, sticky='ew')
        self.D_2 = StringVar()
        self.D_2.set('PC')
        Label(self.frame, textvariable=self.D_2).grid(row=5, column=0, padx=5, pady=5, sticky='ew')
        self.D_3 = StringVar()
        self.D_3.set('WAP')
        Label(self.frame, textvariable=self.D_3).grid(row=6, column=0, padx=5, pady=5, sticky='ew')
        self.D_4 = StringVar()
        self.D_4.set('上海')
        Label(self.frame, textvariable=self.D_4).grid(row=7, column=0, padx=5, pady=5, sticky='ew')
        self.D_5 = StringVar()
        self.D_5.set('杭州部')
        Label(self.frame, textvariable=self.D_5).grid(row=8, column=0, padx=5, pady=5, sticky='ew')
        # self.D_6 = StringVar()
        # self.D_6.set('feed')
        # Label(self.frame, textvariable=self.D_6).grid(row=9, column=0, padx=5, pady=5, sticky='ew')
        self.D_7 = StringVar()
        self.D_7.set('总计')
        Label(self.frame, textvariable=self.D_7).grid(row=10, column=0, padx=5, pady=5, sticky='ew')

        # 以下输入框为输出结果用
        self.APP_r = StringVar()
        Entry(self.frame, textvariable=self.APP_r).grid(row=4, column=1, sticky='ew', padx=5, pady=5, columnspan=2)
        self.APP_j = StringVar()
        Entry(self.frame, textvariable=self.APP_j).grid(row=4, column=3, sticky='ew', padx=5, pady=5, columnspan=2)
        self.PC_r = StringVar()
        Entry(self.frame, textvariable=self.PC_r).grid(row=5, column=1, sticky='ew', padx=5, pady=5, columnspan=2)
        self.PC_j = StringVar()
        Entry(self.frame, textvariable=self.PC_j).grid(row=5, column=3, sticky='ew', padx=5, pady=5, columnspan=2)
        self.WAP_r = StringVar()
        Entry(self.frame, textvariable=self.WAP_r).grid(row=6, column=1, sticky='ew', padx=5, pady=5, columnspan=2)
        self.WAP_j = StringVar()
        Entry(self.frame, textvariable=self.WAP_j).grid(row=6, column=3, sticky='ew', padx=5, pady=5, columnspan=2)
        self.SH_r = StringVar()
        Entry(self.frame, textvariable=self.SH_r).grid(row=7, column=1, sticky='ew', padx=5, pady=5, columnspan=2)
        self.SH_j = StringVar()
        Entry(self.frame, textvariable=self.SH_j).grid(row=7, column=3, sticky='ew', padx=5, pady=5, columnspan=2)
        self.HZ_r = StringVar()
        Entry(self.frame, textvariable=self.HZ_r).grid(row=8, column=1, sticky='ew', padx=5, pady=5, columnspan=2)
        self.HZ_j = StringVar()
        Entry(self.frame, textvariable=self.HZ_j).grid(row=8, column=3, sticky='ew', padx=5, pady=5, columnspan=2)
        # self.fd_r = StringVar()
        # Entry(self.frame, textvariable=self.fd_r).grid(row=9, column=1, sticky='ew', padx=5, pady=5, columnspan=2)
        # self.fd_j = StringVar()
        # Entry(self.frame, textvariable=self.fd_j).grid(row=9, column=3, sticky='ew', padx=5, pady=5, columnspan=2)
        self.zong_r = StringVar()
        Entry(self.frame, textvariable=self.zong_r).grid(row=10, column=1, sticky='ew', padx=5, pady=5, columnspan=2)
        self.zong_j = StringVar()
        Entry(self.frame, textvariable=self.zong_j).grid(row=10, column=3, sticky='ew', padx=5, pady=5, columnspan=2)

        # 以下按钮提供查询功能
        Button(self.frame, text="各端投资",
               command=lambda: threading.Thread(target=self.__touzi, args=(self.start_date.get(),
                                                self.__change_time(self.end_date.get()))).start(),
               default='active').grid(row=0, column=3)
        Button(self.frame, text="各端新增投资",
               command=lambda: threading.Thread(target=self.__xz_touzi, args=(self.start_date.get(),
                                                self.__change_time(self.end_date.get()))).start()).grid(row=0, column=4)
        Button(self.frame, text="各端提现",
               command=lambda: threading.Thread(target=self.__tixian, args=(self.start_date.get(),
                                                self.__change_time(self.end_date.get()))).start()).grid(row=1, column=3)
        Button(self.frame, text="各端充值",
               command=lambda: threading.Thread(target=self.__chongzhi, args=(self.start_date.get(),
                                                self.__change_time(self.end_date.get()))).start()).grid(row=1, column=4)
        Button(self.frame, text="各端待还",
               command=lambda: threading.Thread(target=self.__daihui, args=(self.start_date.get(),
                                                self.__change_time(self.end_date.get()))).start()).grid(row=2, column=3)
        Button(self.frame, text="待定",
               command=lambda: threading.Thread(target=self.__test, args=(self.start_date.get(),
                                                self.__change_time(self.end_date.get()))).start()).grid(row=2, column=4)

        # 格式化各端对应标签和输入框，方便调用
        self.corresponding = {
            "APP": [self.D_1, self.APP_r, self.APP_j],
            "PC": [self.D_2, self.PC_r, self.PC_j],
            "WAP": [self.D_3, self.WAP_r, self.WAP_j],
            "上海": [self.D_4, self.SH_r, self.SH_j],
            "杭州部": [self.D_5, self.HZ_r, self.HZ_j],
            # "feed": [self.D_6, self.fd_r, self.fd_j],
            "总计": [self.D_7, self.zong_r, self.zong_j]
        }

        # 以下代码居中显示窗口
        self.geduan_root.update_idletasks()
        x = (self.geduan_root.winfo_screenwidth() - self.geduan_root.winfo_reqwidth()) / 1.15
        y = (self.geduan_root.winfo_screenheight() - self.geduan_root.winfo_reqheight()) / 2
        self.geduan_root.geometry("+%d+%d" % (x, y))
        self.geduan_root.mainloop()

    def __deafult(self):
        """重置数据"""
        for key in self.corresponding:
            self.corresponding[key][0].set(key)
            self.corresponding[key][1].set("")
            self.corresponding[key][2].set("")

    def __put_to_window(self, *args):
        """打印到前端"""
        data = args[0]
        total = args[1]
        fields = args[2]
        geduan_lock.acquire()
        for row in data:
            if row[0] in self.corresponding:
                self.corresponding[row[0]][0].set(row[0])
                self.corresponding[row[0]][1].set(row[1])
                self.corresponding[row[0]][2].set(row[2])
        for row1 in total:
            self.corresponding["总计"][0].set("总计")
            self.corresponding["总计"][1].set(row1[0])
            self.corresponding["总计"][2].set(row1[1])
        self.biaoqian1.set(fields[0][0])  # 设置字段
        self.biaoqian2.set(fields[1][0])
        self.biaoqian3.set(fields[2][0])
        geduan_lock.release()

    def __touzi(self, *args):
        """各端投资查询功能"""
        start = args[0]
        end = args[1]
        self.__deafult()
        data, fields = mychaxun.select_data_fields("2.常用SQL", "1.各端详情", "1.各端投资.sql", start, end)
        if data == "查询失败" or data == "sql语句不存在":
            messagebox.showerror('友情提示', data)
            return
        total = mychaxun.select_data("1.报表", "1.日报", "03.投资内容.sql", start, end)
        self.__put_to_window(data, total, fields)
        messagebox.showinfo('友情提示', "查询完毕")

    def __xz_touzi(self, *args):
        """各端新增投资查询功能"""
        start = args[0]
        end = args[1]
        self.__deafult()
        data, fields = mychaxun.select_data_fields("2.常用SQL", "1.各端详情", "2.各端新增投资.sql", start, end)
        if data == "查询失败" or data == "sql语句不存在":
            messagebox.showerror('友情提示', data)
            return
        total = mychaxun.select_data("1.报表", "1.日报", "05.新增详情.sql", start, end)
        self.__put_to_window(data, total, fields)
        messagebox.showinfo('友情提示', "查询完毕")

    def __tixian(self, *args):
        """各端提现查询功能"""
        start = args[0]
        end = args[1]
        self.__deafult()
        data, fields = mychaxun.select_data_fields("2.常用SQL", "1.各端详情", "3.各端提现.sql", start, end)
        if data == "查询失败" or data == "sql语句不存在":
            messagebox.showerror('友情提示', data)
            return
        total = mychaxun.select_data("1.报表", "1.日报", "06.提现详情.sql", start, end)
        self.__put_to_window(data, total, fields)
        messagebox.showinfo('友情提示', "查询完毕")

    def __chongzhi(self, *args):
        """各端充值查询功能"""
        start = args[0]
        end = args[1]
        self.__deafult()
        data, fields = mychaxun.select_data_fields("2.常用SQL", "1.各端详情", "4.各端充值.sql", start, end)
        if data == "查询失败" or data == "sql语句不存在":
            messagebox.showerror('友情提示', data)
            return
        total = mychaxun.select_data("1.报表", "1.日报", "02.充值详情.sql", start, end)
        self.__put_to_window(data, total, fields)
        messagebox.showinfo('友情提示', "查询完毕")

    def __daihui(self, *args):
        """各端待还查询功能"""
        start = args[0]
        end = args[1]
        self.__deafult()
        data, fields = mychaxun.select_data_fields("2.常用SQL", "1.各端详情", "5.各端待还.sql", start, end)
        if data == "查询失败" or data == "sql语句不存在":
            messagebox.showerror('友情提示', data)
            return
        total = mychaxun.select_data("1.报表", "1.日报", "18.回款详情.sql", start, end)
        self.__put_to_window(data, total, fields)
        messagebox.showinfo('友情提示', "查询完毕")

    @staticmethod
    def __test(*args):
        """
        测试日期格式
        :param args:
        :return: 无返回值
        """
        x = args[0]
        y = args[1]
        messagebox.showinfo("友情提示", "起始时间点：%s\n终止时间点：%s" % (x, y))

    @staticmethod
    def __change_time(*args):
        """
        改变终止日期，使其符合规范
        :param date: 终止日期
        :return: 返回修改后的终止日期
        """
        date = args[0]
        tmp_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") - datetime.timedelta(1)  # 减一天
        after_date = datetime.datetime.strftime(tmp_date, "%Y-%m-%d %H:%M:%S")
        return after_date

if __name__ == '__main__':
    g = GeDuan()
