#!/usr/bin/env python
# coding=utf-8

'''
Author: dwong
Date: 2017-12-27
Intro:
    1. 通过调用sysbench命令行工具实现MEM性能的测试，测试内存块大小为1KB，
    总共100G的数据的读写。
    2. 记录每次测试结果中Threads fairness下的执行时间。
    3. 每次的测试结果写入到csv文件中。
'''

import time
import subprocess


columns = "Type;Excution Time"
f = open("mem_performance-" + time.strftime("%Y%m%d-%H%M%S") + ".csv", "w+")
f.write(columns+"\n")

# 测试线程数列表， 最大值选CPU的核数
mem_opr = ['read', 'write']

for i in mem_opr:
    command = "sysbench --test=memory --memory-block-size=1K --memory-scope=global --memory-total-size=100G --memory-oper=" + str(i) + " run"
    output = subprocess.check_output(command, shell=True)
    excu_time = output.split('\n')[-3].split(':')[1].split('/')[0]

    item = "" + str(i) + ";" + str(excu_time)
    print(item)

    f.write(item+"\n")
    f.flush()

f.close()
