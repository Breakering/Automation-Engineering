#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/6
"""主界面"""
import time
import xlwt
import datetime
import os
import threading
import multiprocessing
import json
from tkinter import *                   # Tkinter模块，用于UI显示
from tkinter.ttk import *               # Tkinter显示加强模块
from tkinter import messagebox          # 消息弹窗模块
from tkinter.filedialog import asksaveasfile
from conf import settings               # 配置模块
from core import mylogger
from core import myselect               # 简洁查询数据模块
from front.geduan import GeDuan         # 导入各端模块
from front.daily import DaiLy           # 导入日报模块

# 获取今天的日期
today = time.strftime("%Y-%m-%d", time.localtime())

# 生成日志对象
action_logger = mylogger.Mylogger(settings.ACTION_LOG_PATH, "action", settings.LOG_LEVEL).get_logger()

# 获取一把锁
lock = threading.Lock()

# 生成一个简洁查询数据实例
mychaxun = myselect.MySelect()

# 生成星期
week_list = ("星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日")       # 星期对照表
week = week_list[int(datetime.datetime.now().weekday())]    # 获取星期


class MainUi(object):
    """主窗口类"""
    def __init__(self):
        # UI显示
        self.root = Tk()
        self.root.wm_title('简易小工具 by %s version:%s' % (settings.AUTHOR, settings.VERSION))  # 标题
        self.root.iconbitmap(settings.ICO_PATH)  # 设置图标
        self.frame1 = Frame(self.root)
        self.frame1.pack(padx=8, pady=8, ipadx=4)

        # 菜单栏
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="新建", command=self.developing)
        filemenu.add_command(label="打开", command=self.developing)
        filemenu.add_command(label="保存", command=self.developing)
        filemenu.add_command(label="另存为", command=self.developing)
        filemenu.add_command(label="关闭", command=self.developing)
        filemenu.add_separator()  # 添加分割线
        filemenu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=filemenu)

        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="配置数据库信息", command=self.database_info_change)
        editmenu.add_command(label="配置马甲信息", command=self.maja_change)
        editmenu.add_separator()  # 添加分割线
        editmenu.add_command(label="测试重要文件", command=self.__test_main_file)
        menubar.add_cascade(label="编辑", menu=editmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="说明文档", command=self.developing)
        helpmenu.add_command(label="关于", command=self.about)
        menubar.add_cascade(label="帮助", menu=helpmenu)
        self.root.config(menu=menubar)

        # 空白标签
        Label(self.frame1, text=''.center(10, " ")).grid(row=0, column=5, sticky=E)
        Label(self.frame1, text=' ').grid(row=5, column=0, sticky=W)

        # 左侧标签
        Label(self.frame1, text='用户目录:  ').grid(row=0, column=0, sticky=W)
        Label(self.frame1, text='分类管理:  ').grid(row=1, column=0, sticky=W)
        Label(self.frame1, text='语句名称:  ').grid(row=2, column=0, sticky=W)
        Label(self.frame1, text='起始日期:  ').grid(row=3, column=0, sticky=W)
        Label(self.frame1, text='终止日期:  ').grid(row=4, column=0, sticky=W)
        Label(self.frame1, text='当前日期：').grid(row=6, column=0, sticky=W)
        Label(self.frame1, text='查询结果：').grid(row=7, column=0, sticky=W)

        # 右侧标签
        Label(self.frame1, text='    常用功能').grid(row=0, column=6, sticky=NSEW)

        # 输入框
        self.First = StringVar()  # 必须获取一个StringVar对象才可以存放输入框中的信息
        self.First.set(today)
        # 起始日期输入框
        Entry(self.frame1, textvariable=self.First, width=22).grid(row=3, column=1, sticky=W)
        self.Finally = StringVar()
        self.Finally.set(today)
        # 终止日期输入框
        Entry(self.frame1, textvariable=self.Finally, width=22).grid(row=4, column=1, sticky=W)
        date_week = StringVar()
        date_week.set("%s %s" % (today, week))
        # 当前日期
        Label(self.frame1, textvariable=date_week).grid(row=6, column=1, sticky=W)

        # 下拉列表
        number1 = StringVar()  # 用户目录下拉列表
        self.MyChosen1 = Combobox(self.frame1, width=28, textvariable=number1)  # state='readonly'设置只读
        self.MyChosen1.bind('<Button-1>', self.__customer_select)
        # MyChosen1['values'] = ""                                       # 设置下拉列表的值
        self.MyChosen1.grid(row=0, column=1, sticky=W)  # 设置其在界面中出现的位置  column代表列   row 代表行
        # MyChosen1.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

        number2 = StringVar()  # 分类管理下拉列表
        self.MyChosen2 = Combobox(self.frame1, width=28, textvariable=number2)
        self.MyChosen2.bind('<Button-1>', self.__type_select)
        # MyChosen2['values'] = ""
        self.MyChosen2.grid(row=1, column=1, sticky=W)
        # MyChosen2.current(0)

        number3 = StringVar()  # 语句名称下拉列表
        self.MyChosen3 = Combobox(self.frame1, width=28, textvariable=number3)
        self.MyChosen3.bind('<Button-1>', self.__sql_name_select)
        # MyChosen3['values'] = ""
        self.MyChosen3.grid(row=2, column=1, sticky=W)
        # MyChosen3.current(0)

        # text文本框
        lfc_field_1_t_sv = Scrollbar(self.frame1, orient=VERTICAL)  # 文本框-竖向滚动条
        lfc_field_1_t_sh = Scrollbar(self.frame1, orient=HORIZONTAL)  # 文本框-横向滚动条
        self.t1 = Text(self.frame1, height=15, width=30, yscrollcommand=lfc_field_1_t_sv.set,
                       xscrollcommand=lfc_field_1_t_sh.set, wrap='none')  # 查询结果输出文本框

        self.t1.grid(row=7, column=1, sticky=W)
        lfc_field_1_t_sv.grid(row=7, column=2, sticky=NS)
        lfc_field_1_t_sh.grid(row=8, column=1, sticky=EW)

        # 滚动事件
        lfc_field_1_t_sv.config(command=self.t1.yview)
        lfc_field_1_t_sh.config(command=self.t1.xview)

        # 左侧按钮
        # 用户目录添加按钮
        Button(self.frame1, text='添加', width=5, command=self.__customer_add).grid(row=0, column=3, sticky=NSEW)
        # 分类管理添加按钮
        Button(self.frame1, text='添加', width=5, command=self.__type_add).grid(row=1, column=3, sticky=NSEW)
        # 语句名称添加按钮
        Button(self.frame1, text='添加', width=5, command=self.__sql_name_add).grid(row=2, column=3, sticky=NSEW)
        # 查询按钮
        Button(self.frame1, text='查询', width=4,
               command=lambda: threading.Thread(target=self.__sql_select).start()).grid(row=6, column=2, sticky=NSEW)
        Button(self.frame1, text='导出', width=4,
               command=lambda: threading.Thread(target=self.__download).start()).grid(row=8, column=3, sticky=NSEW)
        # 用户目录修改按钮
        Button(self.frame1, text='修改', width=4, command=self.developing).grid(row=0, column=4, sticky=NSEW)
        # 分类管理修改按钮
        Button(self.frame1, text='修改', width=4, command=self.developing).grid(row=1, column=4, sticky=NSEW)
        # 语句名称修改按钮
        Button(self.frame1, text='修改', width=4, command=self.__sql_name_change).grid(row=2, column=4, sticky=NSEW)

        # 最右侧按钮
        Button(self.frame1, text='日报系统',
               command=lambda: multiprocessing.Process(target=DaiLy).start()).grid(row=1, column=6, sticky=NSEW)
        Button(self.frame1, text='各端系统',
               command=lambda: multiprocessing.Process(target=GeDuan).start()).grid(row=2, column=6, sticky=NSEW)
        b62 = Button(self.frame1, text='新增渠道检测', command=self.developing)
        # b62.grid(row=3, column=6, sticky = NSEW)

        # 以下代码居中显示窗口
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry("+%d+%d" % (x, y))
        self.root.mainloop()

    def __customer_select(self, event):
        """
        用户目录设置函数
        :param event: 鼠标单击执行
        :return: 没有返回值
        """
        customer_list = os.listdir(settings.SQL_FILE_DIR)
        self.MyChosen1['values'] = customer_list
        self.MyChosen2['values'] = ("", "")
        self.MyChosen2.current(0)
        self.MyChosen3['values'] = ("", "")
        self.MyChosen3.current(0)

    def __type_select(self, event):
        """
        分类管理设置函数
        :param event:鼠标单击执行
        :return:没有返回值
        """
        customer_get = self.MyChosen1.get().strip()
        if len(customer_get) == 0:
            messagebox.showinfo('友情提示', '请设置前置分类')
            return
        type_path = os.path.join(settings.SQL_FILE_DIR, customer_get)
        type_list = os.listdir(type_path)
        self.MyChosen2['values'] = type_list
        self.MyChosen3['values'] = ("", "")
        self.MyChosen3.current(0)

    def __sql_name_select(self, event):
        """
        语句名称设置函数
        :param event:鼠标单击执行
        :return:没有返回值
        """
        customer_get = self.MyChosen1.get().strip()
        type_get = self.MyChosen2.get().strip()
        if len(customer_get) == 0 or len(type_get) == 0:
            messagebox.showinfo('友情提示', '请设置前置分类')
            return
        sql_name_path = os.path.join(settings.SQL_FILE_DIR, customer_get, type_get)
        sql_name_list = os.listdir(sql_name_path)
        self.MyChosen3['values'] = sql_name_list

    def __sql_select(self):
        """
        查询函数，用来查询相应sql语句对应的结果
        :return: 没有返回值
        """
        customer_get = self.MyChosen1.get().strip()  # 用户目录获取
        type_get = self.MyChosen2.get().strip()  # 分类管理获取
        sql_name_get = self.MyChosen3.get().strip()  # 语句名称获取
        if len(customer_get) == 0 or len(type_get) == 0 or len(sql_name_get) == 0:
            messagebox.showinfo('友情提示', '请设置sql语句')
            return
        riqi1 = self.First.get().strip()  # 起始日期获取
        riqi2 = self.Finally.get().strip()  # 终止日期获取
        data, fields = mychaxun.select_data_fields(customer_get, type_get, sql_name_get, riqi1, riqi2)
        if fields is None:  # 代表查询失败
            messagebox.showinfo('友情提示', data)
            return
        lock.acquire()  # 加锁,目的防止同一时间有多个线程输出内容到文本框中
        self.t1.delete(0.0, END)  # 将文本框清空
        for field in range(0, len(fields)):  # 写上字段信息
            self.t1.insert(END, fields[field][0] + "\t")
        self.t1.insert(END, "\n")
        count = 1  # 控制换行
        for row in data:
            for col in range(0, len(row)):
                if count % int(len(row)) == 0:  # 计数项能被列数整除，说明是一行的最后一个数据，此时应在此换行
                    self.t1.insert(END, "%s\n" % row[col])
                    count += 1
                else:
                    self.t1.insert(END, "%s\t" % row[col])
                    count += 1
        lock.release()  # 释放锁
        messagebox.showinfo('友情提示', '查询完毕')

    def __download(self):
        """
        导出到EXCEL功能
        :return:
        """
        customer_get = self.MyChosen1.get().strip()  # 用户目录获取
        type_get = self.MyChosen2.get().strip()  # 分类管理获取
        sql_name_get = self.MyChosen3.get().strip()  # 语句名称获取
        riqi1 = self.First.get().strip()  # 起始日期获取
        riqi2 = self.Finally.get().strip()  # 终止日期获取
        if len(customer_get) == 0 or len(type_get) == 0 or len(sql_name_get) == 0:
            messagebox.showinfo('友情提示', '请设置sql语句')
            return
        title = '保存文件'
        ftypes = [('Excel文件', '.xls'), ('所有文件', '*')]
        path = asksaveasfile(filetypes=ftypes, title=title, defaultextension='.xls')
        if path is not None:
            data, fields = mychaxun.select_data_fields(customer_get, type_get, sql_name_get, riqi1, riqi2)
            if fields is None:
                messagebox.showinfo('友情提示', data)
                return
            workbook = xlwt.Workbook(encoding='utf-8')
            sheet = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
            style = xlwt.XFStyle()  # 创建格式style
            font = xlwt.Font()  # 创建font，设置字体
            font.name = 'Arial Unicode MS'  # 字体格式
            style.font = font  # 将字体font，应用到格式style
            alignment = xlwt.Alignment()  # 创建alignment，居中
            alignment.horz = xlwt.Alignment.HORZ_CENTER  # 居中
            style.alignment = alignment  # 应用到格式style
            style1 = xlwt.XFStyle()
            font1 = xlwt.Font()
            font1.name = 'Arial Unicode MS'
            # font1.colour_index = 3                  #字体颜色（绿色）
            font1.bold = True  # 字体加粗
            style1.font = font1
            style1.alignment = alignment
            for field in range(0, len(fields)):  # 写上字段信息
                sheet.write(0, field, fields[field][0], style1)
            row = 1
            col = 0
            for row in range(1, len(data) + 1):
                for col in range(0, len(fields)):
                    sheet.write(row, col, u'%s' % data[row - 1][col], style)  # 获取并写入数据段信息
            workbook.save(path.name)
            messagebox.showinfo('友情提示', '导出完成')

    def __customer_add(self):
        """用户目录添加功能"""
        customer = self.MyChosen1.get()
        file_path = os.path.join(settings.SQL_FILE_DIR, customer)
        if len(customer) == 0:
            messagebox.showinfo('友情提示', '不能为空')
            return
        if os.path.exists(file_path):
            messagebox.showinfo('友情提示', '已经存在')
            return
        os.mkdir(file_path)
        messagebox.showinfo('友情提示', '创建成功！')

    def __type_add(self):
        """类型添加功能"""
        customer = self.MyChosen1.get()
        type_own = self.MyChosen2.get()
        file_path = os.path.join(settings.SQL_FILE_DIR, customer, type_own)
        if len(customer) == 0 or len(type_own) == 0:
            messagebox.showinfo('友情提示', '不能为空')
            return
        if os.path.exists(file_path):
            messagebox.showinfo('友情提示', '已经存在')
            return
        os.mkdir(file_path)
        messagebox.showinfo('友情提示', '创建成功！')

    def __sql_name_add(self):
        """sql文件添加功能"""
        customer = self.MyChosen1.get()
        type_own = self.MyChosen2.get()
        sql_name = self.MyChosen3.get()
        file_path = os.path.join(settings.SQL_FILE_DIR, customer, type_own, sql_name)
        if len(customer) == 0 or len(type_own) == 0 or len(sql_name) == 0:
            messagebox.showinfo('友情提示', '不能为空')
            return
        if os.path.exists(file_path):
            messagebox.showinfo('友情提示', '已经存在')
            return
        self.__sql_file_show(file_path)

    def __customer_change(self):
        pass  # todo(Breakering)  此功能以后再弄

    def __type_change(self):
        pass  # todo(Breakering)  此功能以后再弄

    def __sql_name_change(self):
        """修改SQL文件"""
        customer = self.MyChosen1.get()
        type_own = self.MyChosen2.get()
        sql_name = self.MyChosen3.get()
        file_path = os.path.join(settings.SQL_FILE_DIR, customer, type_own, sql_name)
        if len(customer) == 0 or len(type_own) == 0 or len(sql_name) == 0:
            messagebox.showinfo('友情提示', '不能为空')
            return
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                sqlyuju = f.read()
            self.__sql_file_show(file_path, sqlyuju)

    def __sql_file_show(self, file_path, sqlyuju=None):
        """SQL文件添加修改窗口"""
        sfs_root = Toplevel()
        sfs_root.wm_title("SQL语句输入窗口")
        sfs_root.iconbitmap(os.path.join(settings.ICO_PATH))  # 设置图标
        # 标签
        Label(sfs_root, text='请在下方输入SQL语句：').grid(row=0, column=0, sticky=W)
        Label(sfs_root, text='\t').grid(row=0, column=4, sticky=W)
        # text文本框
        s_scrollbar = Scrollbar(sfs_root, orient=VERTICAL)  # 文本框-竖向滚动条
        h_scrollbar = Scrollbar(sfs_root, orient=HORIZONTAL)  # 文本框-横向滚动条
        text1 = Text(sfs_root, height=50, width=200, yscrollcommand=s_scrollbar.set,
                     xscrollcommand=h_scrollbar.set, wrap='none')  # 文本框
        text1.grid(row=2, column=0, sticky=W)
        if sqlyuju is not None:  # 传入SQL语句表明是修改功能
            text1.insert(END, sqlyuju)
        s_scrollbar.grid(row=2, column=1, sticky=NS)
        h_scrollbar.grid(row=3, column=0, sticky=EW)
        # 滚动事件
        s_scrollbar.config(command=text1.yview)
        h_scrollbar.config(command=text1.xview)
        # 按钮
        b1 = Button(sfs_root, text='确定',
                    command=lambda: self.__sql_file_change(file_path, text1.get("0.0", "end"), sfs_root))
        b1.grid(row=0, column=2, sticky=W)
        Button(sfs_root, text='取消', command=lambda: sfs_root.destroy()).grid(row=1, column=2, sticky=W)
        # 以下代码居中显示窗口
        sfs_root.update_idletasks()
        x1 = (sfs_root.winfo_screenwidth() - sfs_root.winfo_reqwidth()) / 2
        y1 = (sfs_root.winfo_screenheight() - sfs_root.winfo_reqheight()) / 2
        sfs_root.geometry("+%d+%d" % (x1, y1))
        sfs_root.mainloop()

    @staticmethod
    def __sql_file_change(*args):
        """对SQL文件进行修改"""
        file_path = args[0]
        text = args[1]
        sfs_root = args[2]
        sfs_root.destroy()  # 关闭窗口
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        messagebox.showinfo('友情提示', '修改或创建成功！')

    @staticmethod
    def database_info_change():
        """配置数据库信息"""
        def change_info():
            """数据库信息确认"""
            database_info["host"] = host.get()
            database_info["user"] = user.get()
            database_info["passwd"] = passwd.get()
            database_info["db"] = db.get()
            database_info["port"] = int(port.get())
            database_info["charset"] = charset.get()
            json.dump(database_info, open(database_info_path, "w", encoding="utf-8"))
            database_root.destroy()
            messagebox.showinfo('友情提示', '数据库信息修改成功!')
        database_info_path = os.path.join(settings.CONF_DIR, "database_info.json")
        database_info = json.load(open(database_info_path, "r", encoding="utf-8"))
        database_root = Toplevel()
        database_root.wm_title("修改数据库信息")
        database_root.iconbitmap(settings.ICO_PATH)
        Label(database_root, text="数据库信息如下:").grid(row=0, column=0, sticky=EW)
        Label(database_root, text="host:").grid(row=1, column=0, sticky=EW)
        Label(database_root, text="user:").grid(row=2, column=0, sticky=EW)
        Label(database_root, text="passwd:").grid(row=3, column=0, sticky=EW)
        Label(database_root, text="db:").grid(row=4, column=0, sticky=EW)
        Label(database_root, text="port:").grid(row=5, column=0, sticky=EW)
        Label(database_root, text="charset:").grid(row=6, column=0, sticky=EW)
        Label(database_root, text="  ").grid(row=0, column=2, sticky=EW)
        host = StringVar()
        host.set(database_info["host"])
        user = StringVar()
        user.set(database_info["user"])
        passwd = StringVar()
        passwd.set(database_info["passwd"])
        db = StringVar()
        db.set(database_info["db"])
        port = StringVar()
        port.set(database_info["port"])
        charset = StringVar()
        charset.set(database_info["charset"])
        Entry(database_root, textvariable=host, width=22).grid(row=1, column=1, sticky=EW)
        Entry(database_root, textvariable=user, width=22).grid(row=2, column=1, sticky=EW)
        Entry(database_root, textvariable=passwd, width=22).grid(row=3, column=1, sticky=EW)
        Entry(database_root, textvariable=db, width=22).grid(row=4, column=1, sticky=EW)
        Entry(database_root, textvariable=port, width=22).grid(row=5, column=1, sticky=EW)
        Entry(database_root, textvariable=charset, width=22).grid(row=6, column=1, sticky=EW)
        Button(database_root, text='修改', width=5, command=change_info).grid(row=7, column=1, sticky=E)  # 修改数据库信息按钮
        # 以下代码居中显示窗口
        database_root.update_idletasks()
        x = (database_root.winfo_screenwidth() - database_root.winfo_reqwidth()) / 2
        y = (database_root.winfo_screenheight() - database_root.winfo_reqheight()) / 2
        database_root.geometry("+%d+%d" % (x, y))
        database_root.mainloop()

    @staticmethod
    def maja_change():
        """配置马甲信息"""

        def change_majia():
            """马甲信息确认"""
            majia_info["majia_kefu"] = majia_kefu.get()
            majia_info["majia_yonghu"] = majia_yonghu.get()
            json.dump(majia_info, open(majia_info_path, "w", encoding="utf-8"))
            majia_root.destroy()
            messagebox.showinfo('友情提示', '马甲信息修改成功!')
        majia_info_path = os.path.join(settings.CONF_DIR, "majia.json")
        majia_info = json.load(open(majia_info_path, "r", encoding="utf-8"))
        majia_root = Toplevel()
        majia_root.wm_title("修改马甲信息")
        majia_root.iconbitmap(settings.ICO_PATH)
        Label(majia_root, text="马甲信息如下:").grid(row=0, column=0, sticky=EW)
        Label(majia_root, text="马甲客服:").grid(row=1, column=0, sticky=EW)
        Label(majia_root, text="马甲用户:").grid(row=2, column=0, sticky=EW)
        majia_kefu = StringVar()
        majia_kefu.set(majia_info["majia_kefu"])
        majia_yonghu = StringVar()
        majia_yonghu.set(majia_info["majia_yonghu"])
        Entry(majia_root, textvariable=majia_kefu, width=80).grid(row=1, column=1, sticky=EW)
        Entry(majia_root, textvariable=majia_yonghu, width=80).grid(row=2, column=1, sticky=EW)
        Button(majia_root, text='修改', width=5, command=change_majia).grid(row=3, column=1, sticky=E)  # 修改数据库信息按钮
        # 以下代码居中显示窗口
        majia_root.update_idletasks()
        x = (majia_root.winfo_screenwidth() - majia_root.winfo_reqwidth()) / 2
        y = (majia_root.winfo_screenheight() - majia_root.winfo_reqheight()) / 2
        majia_root.geometry("+%d+%d" % (x, y))
        majia_root.mainloop()

    @staticmethod
    def developing():
        """
        施工函数，表示该功能还没开发完成
        :return: 没有返回值
        """
        messagebox.showinfo('友情提示', '该功能正在开发中，敬请期待！')

    @staticmethod
    def about():
        """关于函数"""
        messagebox.showinfo('关于', '作者：%s\n版本：%s' % (settings.AUTHOR, settings.VERSION))

    @staticmethod
    def __test_main_file():
        """SQL文件添加修改窗口"""
        def test_file(text1, info):
            """
            测试重要文件功能
            :param text1: 文本框对象
            :param info: 底部标签对象
            :return: 没有返回值
            """
            total = 0  # 计数总计重要文件个数
            normal = 0  # 计数通过验证的文件个数
            error = 0  # 计数异常文件个数
            text1.delete(0.0, END)
            text1.insert(END, "%-10s%-10s%-30s%s\n" % ("用户目录", "分类管理", "语句名称", "状态"))
            text1.insert(END, "\n".rjust(70, "="))
            with open(settings.MAIN_FILE_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    if len(line.strip()) == 0:  # 空行则跳过
                        continue
                    line_split = [i.replace('"', "").strip() for i in line.split(",") if i]  # 将三级目录规范输出为列表格式
                    if len(line_split) != 3:  # 必须保证是三级目录的格式
                        messagebox.showerror('友情提示', 'main_file文件有异常,请检查,剩余文件继续测试!')
                        continue
                    file_path = os.path.join(settings.SQL_FILE_DIR, line_split[0], line_split[1], line_split[2])
                    total += 1
                    if os.path.isfile(file_path):
                        text1.insert(END, "%-10s%-10s%-30s%-5s\n" % (line_split[0], line_split[1], line_split[2], "通过"))
                        normal += 1
                    else:
                        text1.insert(END, "%-10s%-10s%-30s%-5s\n" % (line_split[0], line_split[1], line_split[2], "异常"))
                        error += 1
                if error == 0:  # 全部通过验证
                    messagebox.showinfo('友情提示', '全部通过！')
                else:  # 代表有异常文件
                    messagebox.showerror('友情提示', '有%s个异常!' % error)
            info.set("%-40s%-40s%-40s" % ("总计:%s" % total, "通过:%s" % normal, "异常:%s" % error))

        tmf_root = Toplevel()
        tmf_root.wm_title("测试重要文件窗口")
        tmf_root.iconbitmap(os.path.join(settings.ICO_PATH))  # 设置图标
        # 标签
        Label(tmf_root, text='测试重要文件：').grid(row=0, column=0, sticky=W)
        Label(tmf_root, text='\t').grid(row=0, column=4, sticky=W)
        Label(tmf_root, text='(目的：防止重要文件被修改)').grid(row=1, column=0, sticky=W)

        info = StringVar()
        info.set("%-40s%-40s%-40s" % ("总计:", "通过:", "异常:"))
        # 当前日期
        Label(tmf_root, textvariable=info).grid(row=4, column=0, sticky=W)

        # text文本框
        s_scrollbar = Scrollbar(tmf_root, orient=VERTICAL)  # 文本框-竖向滚动条
        h_scrollbar = Scrollbar(tmf_root, orient=HORIZONTAL)  # 文本框-横向滚动条
        text1 = Text(tmf_root, height=25, width=80, yscrollcommand=s_scrollbar.set,
                     xscrollcommand=h_scrollbar.set, wrap='none')  # 文本框
        text1.grid(row=2, column=0, sticky=W)
        s_scrollbar.grid(row=2, column=1, sticky=NS)
        h_scrollbar.grid(row=3, column=0, sticky=EW)
        # 滚动事件
        s_scrollbar.config(command=text1.yview)
        h_scrollbar.config(command=text1.xview)
        # 按钮
        b1 = Button(tmf_root, text='测试',
                    command=lambda: test_file(text1, info))
        b1.grid(row=0, column=2, sticky=W)
        Button(tmf_root, text='取消', command=lambda: tmf_root.destroy()).grid(row=1, column=2, sticky=W)
        # 以下代码居中显示窗口
        tmf_root.update_idletasks()
        x1 = (tmf_root.winfo_screenwidth() - tmf_root.winfo_reqwidth()) / 2
        y1 = (tmf_root.winfo_screenheight() - tmf_root.winfo_reqheight()) / 2
        tmf_root.geometry("+%d+%d" % (x1, y1))
        tmf_root.mainloop()
