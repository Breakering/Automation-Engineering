#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/6
"""日报模块"""
import datetime
import gevent
import os
from tkinter import *                   # Tkinter模块，用于UI显示
from tkinter.ttk import *               # Tkinter显示加强模块
from tkinter import messagebox          # 消息弹窗模块
from conf import settings
from core import myselect

# 获取昨天的日期
yesterday = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), "%Y-%m-%d")

# 生成一个简洁查询数据实例
mychaxun = myselect.MySelect()


class DaiLy(object):
    """日报类"""
    obj = None  # 实例在此

    def __init__(self):
        self.daily_root = Tk()
        self.daily_root.title("日报系统 by  %s version:%s" % (settings.AUTHOR, settings.VERSION))
        self.daily_root.iconbitmap(settings.ICO_PATH)  # 设置图标
        self.frame = Frame(self.daily_root)
        self.frame.pack(padx=8, pady=8, ipadx=4)
        Label(self.frame, text="请输入起始日期:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        # 绑定对象到Entry
        self.start = StringVar()
        self.start.set(yesterday)
        Entry(self.frame, textvariable=self.start).grid(row=0, column=1, sticky='ew', padx=5, pady=5, columnspan=2)
        Label(self.frame, text="请输入终止日期:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        # 绑定对象到Entry
        self.end = StringVar()
        self.end.set(yesterday)
        Entry(self.frame, textvariable=self.end).grid(row=1, column=1, sticky='ew', padx=5, pady=5, columnspan=2)

        # 创建按钮
        Button(self.frame, text="导出日报",
               command=lambda: self.__download_daily()).grid(row=2, column=0, padx=5, pady=5)
        Button(self.frame, text="取消", command=lambda: self.daily_root.destroy()).grid(row=2, column=1, padx=5, pady=5)

        # 以下代码居中显示窗口
        self.daily_root.update_idletasks()
        x = (self.daily_root.winfo_screenwidth() - self.daily_root.winfo_reqwidth()) / 4.5
        y = (self.daily_root.winfo_screenheight() - self.daily_root.winfo_reqheight()) / 3
        self.daily_root.geometry("+%d+%d" % (x, y))
        self.daily_root.mainloop()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(DaiLy, cls).__new__(cls, *args, **kwargs)
        return cls._inst

    def __download_daily(self):
        """导出日报功能"""
        start = self.start.get()
        end = self.end.get()
        a = datetime.datetime.timestamp(datetime.datetime.strptime(start, "%Y-%m-%d"))
        b = datetime.datetime.timestamp(datetime.datetime.strptime(end, "%Y-%m-%d"))
        if a > b:
            messagebox.showinfo('友情提示', '起始日期不能大于终止日期')
            return
        day_list = []  # 存放日期的列表
        while True:
            if start == end:  # 如果日期碰到了终止日期就结束
                day_list.append(end)  # 并将最后一个日期放入日期列表
                break
            day_list.append(start)  # 先将起始日期放进去，然后开始加一天循环直到碰到终止日期为止
            start = datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(1)
            start = datetime.datetime.strftime(start, "%Y-%m-%d")
        g_list = [gevent.spawn(self.__excute, i) for i in day_list]  # 批量启动协程
        gevent.joinall(g_list)  # 并发等待所有协程

    def __excute(self, *args):
        """执行导出日报的功能"""
        day = args[0]
        daily_file_name = os.path.join(settings.RIBAO_DIR, day)
        if os.path.exists("%s.txt" % daily_file_name):
            f1 = open("%s.txt" % daily_file_name, "w", encoding="utf-8")
            f1.close()
        f = open("%s.txt" % daily_file_name, "a", encoding="utf-8")
        zhu = mychaxun.select_data("1.报表", "1.日报", "01.注册人数.sql", day, day)
        chong = mychaxun.select_data("1.报表", "1.日报", "02.充值详情.sql", day, day)
        tou = mychaxun.select_data("1.报表", "1.日报", "03.投资内容.sql", day, day)
        lao = mychaxun.select_data("1.报表", "1.日报", "04.老用户转化.sql", day, day)
        xz = mychaxun.select_data("1.报表", "1.日报", "05.新增详情.sql", day, day)
        tx = mychaxun.select_data("1.报表", "1.日报", "06.提现详情.sql", day, day)
        xutou = mychaxun.select_data("1.报表", "1.日报", "07.续投详情.sql", day, day)
        for i in zhu:
            zhu_r = i[0]
        for i in chong:
            chong_r = i[0]
            chong_j = i[1]
        for i in tou:
            tou_r = i[0]
            tou_j = i[1]
            tou_b = i[2]
        for i in lao:
            laoz_r = i[0]
        for i in xz:
            xz_r = i[0]
            xz_j = i[1]
        for i in tx:
            tx_j = i[1]
        for i in xutou:
            xutou_j = i[0]
        f.write('\n注册人数: %s\n' % zhu_r)
        f.write('充值人数: %s\n' % chong_r)
        f.write('投资人数: %s\n' % tou_r)
        f.write('老平台转化投资人数: %s\n' % laoz_r)
        f.write('新增投资人数: %s\n' % xz_r)
        f.write('新增投资金额: %s\n' % xz_j)
        f.write('充值金额: %s\n' % chong_j)
        f.write('投资金额: %s\n' % tou_j)
        f.write('投标笔数: %s\n' % tou_b)
        f.write('提现金额: %s\n' % tx_j)
        f.write('续投金额: %s\n' % xutou_j)
        biaodi = mychaxun.select_data("1.报表", "1.日报", "08.标的详情.sql", day, day)
        f.write('\n标的详情：\n')
        for i in biaodi:
            biaodi_l = i[0]
            biaodi_r = i[1]
            biaodi_j = i[2]
            f.write("%s " % biaodi_l)
            f.write("%s " % biaodi_r)
            f.write("%s\n" % biaodi_j)
        f.write('\n期限详情：\n')
        qixian = mychaxun.select_data("1.报表", "1.日报", "09.期限详情.sql", day, day)
        for i in qixian:
            qixian_l = i[0]
            qixian_r = i[1]
            qixian_j = i[2]
            f.write("%s " % qixian_l)
            f.write("%s " % qixian_r)
            f.write("%s\n" % qixian_j)
        f.write('\n众惠宝短标满标时长: ')

        zh_db_mb = mychaxun.select_data("1.报表", "1.日报", "10.众惠宝短标满标时长.sql", day, day)
        for i in zh_db_mb:
            zh_db_mb_sc = i[1]
            f.write("%s\n" % zh_db_mb_sc)

        f.write('\n众惠宝短标投资详情： ')
        zh_db_tou = mychaxun.select_data("1.报表", "1.日报", "11.众惠宝短标投资详情.sql", day, day)
        for i in zh_db_tou:
            zh_db_tou_r = i[1]
            zh_db_tou_j = i[2]
            f.write("%s " % zh_db_tou_r)
            f.write("%s\n" % zh_db_tou_j)

        f.write('\n各端投资详情：\n')
        gd_tou = mychaxun.select_data("2.常用SQL", "1.各端详情", "1.各端投资.sql", day, day)
        for i in gd_tou:
            gd_l = i[0]
            gd_r = i[1]
            gd_j = i[2]
            f.write("%s " % gd_l)
            f.write("%s " % gd_r)
            f.write("%s\n" % gd_j)

        f.write('\n用户行为：\n')
        tou_sj = mychaxun.select_data("1.报表", "1.日报", "13.各时间段投资人数详情.sql", day, day)
        for i in tou_sj:
            tou_sj_l = i[0]
            tou_sj_r = i[1]
            f.write("%s " % tou_sj_l)
            f.write("%s\n" % tou_sj_r)

        f.write('\n充值金额分布图：\n')
        chong_fen = mychaxun.select_data("1.报表", "1.日报", "14.充值金额分布.sql", day, day)
        for i in chong_fen:
            chong_fen_l = i[0]
            chong_fen_r = i[1]
            f.write("%s " % chong_fen_l)
            f.write("%s\n" % chong_fen_r)

        dan_r = mychaxun.select_data("1.报表", "1.日报", "15.单人最高充值.sql", day, day)
        for i in dan_r:
            f.write('\n单人最高充值: %s\n' % i[1])
        dan_b = mychaxun.select_data("1.报表", "1.日报", "16.单笔最高充值.sql", day, day)
        for i in dan_b:
            f.write('单笔最高充值: %s\n' % i[1])

        f.write('\n各端新增投资详情：\n')
        gd_xztou = mychaxun.select_data("2.常用SQL", "1.各端详情", "2.各端新增投资.sql", day, day)
        for i in gd_xztou:
            gd_xztou_l = i[0]
            gd_xztou_r = i[1]
            gd_xztou_j = i[2]
            f.write("%s " % gd_xztou_l)
            f.write("%s " % gd_xztou_r)
            f.write("%s\n" % gd_xztou_j)

        f.write('\n各端提现详情：\n')
        gd_tx = mychaxun.select_data("2.常用SQL", "1.各端详情", "3.各端提现.sql", day, day)
        for i in gd_tx:
            gd_tx_l = i[0]
            gd_tx_r = i[1]
            gd_tx_j = i[2]
            f.write("%s " % gd_tx_l)
            f.write("%s " % gd_tx_r)
            f.write("%s\n" % gd_tx_j)

        hui = mychaxun.select_data("1.报表", "1.日报", "18.回款详情.sql", day, day)
        for i in hui:
            f.write('\n已还总额: %s\n' % i[1])

        f.write('随存随取赎回金额： \n')
        shu = mychaxun.select_data("1.报表", "1.日报", "19.赎回详情.sql", day, day)
        for i in shu:
            shu_l = i[0]
            shu_j = i[2]
            f.write("%s " % shu_l)
            f.write("%s\n" % shu_j)

        dai = mychaxun.select_data("1.报表", "1.日报", "20.待还详情.sql", day, day)
        for i in dai:
            f.write('待回总额: %s\n' % i[1])
        f.write('\n待收分布图：\n')
        daishou_f = mychaxun.select_data("1.报表", "1.日报", "21.待还分布.sql", day, day)
        for i in daishou_f:
            daishou_f_l = i[0]
            daishou_f_r = i[1]
            f.write("%s " % daishou_f_l)
            f.write("%s\n" % daishou_f_r)

        f.write('\n各端回款并提现详情：\n')
        gd_h_tx = mychaxun.select_data("2.常用SQL", "1.各端详情", "9.各端回款并提现.sql", day, day)
        for i in gd_h_tx:
            gd_h_tx_l = i[0]
            gd_h_tx_r = i[1]
            gd_h_tx_j = i[2]
            f.write("%s " % gd_h_tx_l)
            f.write("%s " % gd_h_tx_r)
            f.write("%s\n" % gd_h_tx_j)

        chong_tou = mychaxun.select_data("1.报表", "1.日报", "22.充值并投资.sql", day, day)
        for i in chong_tou:
            f.write('\n充值并投资金额: %s\n' % i[0])

        f.write('\n期限满标用时：\n')
        qx_mb = mychaxun.select_data("1.报表", "1.日报", "12.期限平均满标用时.sql", day, day)
        for i in qx_mb:
            qx_mb_b = i[0]
            qx_mb_q = i[1]
            qx_mb_j = i[2]
            qx_mb_s = i[3]
            f.write("%s " % qx_mb_b)
            f.write("%s " % qx_mb_q)
            f.write("%s " % qx_mb_j)
            f.write("%s\n" % qx_mb_s)

        sm = mychaxun.select_data("1.报表", "1.日报", "23.实名人数.sql", day, day)
        for i in sm:
            f.write('\n实名人数: %s\n' % i[0])

        zy_yh = mychaxun.select_data("1.报表", "1.日报", "24.众银宝回款详情.sql", day, day)
        for i in zy_yh:
            f.write('众银宝已还金额: %s\n' % i[1])

        tjr = mychaxun.select_data("1.报表", "1.日报", "25.推荐人新增详情.sql", day, day)
        for i in tjr:
            f.write('推荐人新增人数: %s\n' % i[0])
            f.write('推荐人新增金额: %s\n' % i[1])

        un_tjr = mychaxun.select_data("1.报表", "1.日报", "26.非推荐人新增详情.sql", day, day)
        for i in un_tjr:
            f.write('非推荐人新增人数: %s\n' % i[0])

        login = mychaxun.select_data("1.报表", "1.日报", "27.登陆人数.sql", day, day)
        for i in login:
            f.write('登陆人数: %s\n' % i[0])

        zhai = mychaxun.select_data("1.报表", "1.日报", "28.债券转让总额.sql", day, day)
        for i in zhai:
            f.write('债券转让总额: %s\n' % i[0])
        messagebox.showinfo('友情提示', '日报%s导出完毕' % day)



