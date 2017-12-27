#!/usr/bin/env python
# coding=utf-8

'''
Author: dwong
Date: 2017-12-27
Intro:
    1. 对于磁盘我们除了关注吞吐量和IOPS之外， 也会考虑磁盘的延迟。 这里使用
    工具ioping来进行磁盘延迟进行测量。
    2. 这里我们测试了Cached IO, Direct IO, Async IO三种不同类型的磁盘IO延迟。
    每种测试执行1000次， 分别取最小值， 平均值， 最大值。
    3. 每次的测试结果写入到csv文件中。
'''

import time
import subprocess


columns = "io_type; 最小值(min); 平均值(avg); 最大值(max)"
f = open("io_latency-" + time.strftime("%Y%m%d-%H%M%S") + ".csv", "w+")
f.write(columns+"\n")

for i in ('-C', '-D', '-A'):
    command = "sudo ioping " + str(i) + " -c 1000 ."
    output = subprocess.check_output(command, shell=True)
    response = output.split('\n')[-2]
    result = response.split('=')[1].split('/')
    if i == '-C':
        io_option = "cached"
    elif i == '-D':
        io_option = "direct"
    else:
        io_option = "async"

    item = "" + str(io_option) + ";" + str(result[0]
                                           ) + ";" + str(result[1]) + ";" + str(result[2])
    print(item)

    f.write(item+"\n")
    f.flush()

f.close()
