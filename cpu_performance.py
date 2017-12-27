#!/usr/bin/env python
# coding=utf-8

'''
Author: dwong
Date: 2017-12-27
Intro:
    1. 通过调用sysbench命令行工具实现CPU性能的测试， 由于测试线程数依赖于系统
    最大线程数依赖, 最好所有平台创建的实例的规格都是一样的。
    然后分别测试1， 2， .. n(CPU个数)线程下的性能。
    2. 记录每次测试结果中Threads fairness下的执行时间。
    3. 每次的测试结果写入到csv文件中。
'''

import time
import subprocess


columns = "Number of Threads;Excution Time"
f = open("cpu_performance-" + time.strftime("%Y%m%d-%H%M%S") + ".csv", "w+")
f.write(columns+"\n")

# 测试线程数列表， 最大值选CPU的核数
num_threads = [1, 2, 4]

for i in num_threads:
    command = "sysbench --test=cpu --cpu-max-prime=20000 --num-threads=" + str(i) + " run"
    output = subprocess.check_output(command, shell=True)
    excu_time = output.split('\n')[-3].split(':')[1].split('/')[0]

    item = "" + str(i) + ";" + str(excu_time)
    print(item)

    f.write(item+"\n")
    f.flush()

f.close()
