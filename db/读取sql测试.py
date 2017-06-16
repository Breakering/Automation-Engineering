#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/25

import os
import sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

sql_file_path = os.path.join(path, "sql_file")

print(sql_file_path)
print(os.listdir(sql_file_path))
chose_sql_file_path = os.path.join(sql_file_path, os.listdir(sql_file_path)[0])
print(os.listdir(chose_sql_file_path))
chose_sql_path = os.path.join(chose_sql_file_path, os.listdir(chose_sql_file_path)[0])
print(os.listdir(chose_sql_path))
