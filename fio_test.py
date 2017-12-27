#!/usr/bin/env python
# coding=utf-8

'''
Author: dwong
Date: 2017-12-27
Intro:
  1. 该脚本会测试顺序读写、随机读写； 单次IO块文件大小: 4K, 16K, 64K, 1M;
单次测试的线程数： 1, 8, 32; 单次测试IO单元数量: 1, 8, 32, 64, 128;
每次测试都会执行三次取平均值。
  2. 整个fio测试结果数据比较庞大， 我们只取两项： 吞吐量和IOPS
 　　　- throughput 磁盘的吞吐量， 有助于了解磁盘的顺序读写性能
       - IOPS 磁盘每秒读写次数， 有助于了解磁盘的随机读写性能
  3. 每次的测试结果都会写入到csv文件中。
'''

import os
import time
import subprocess

device = 'fio_testfile'

fio_size = "1G"  # size in fio
fio_runtime = "5"  # runtime in fio for time_based tests

# fio --minimal hardcoded positions
fio_iops_pos = 7

kernel_version = os.uname()[2]
columns = "iotype;bs;njobs;iodepth;throughput;iops"

# Eliminate noise by running each test n times and calculating average.
n_iterations = 3

f = open("fio_test-" + time.strftime("%Y%m%d-%H%M%S") + ".csv", "w+")
f.write(columns+"\n")

for run in ('write', 'randwrite', 'read', 'randread'):
    for blocksize in ('4k', '16k', '64k', '1M'):
        for numjobs in (1, 8, 32):
            for iodepth in (1, 8, 32, 64, 128):

                fio_type_offset = 0
                throughput = 0.0
                iops = 0.0

                result = "" + str(run) + ";" + str(blocksize) + ";" + str(
                    numjobs) + ";" + str(iodepth) + ";"
                command = "sudo fio --minimal -name=temp-fio --bs="+str(blocksize)+" --ioengine=libaio --iodepth="+str(iodepth)+" --size="+fio_size+" --direct=1 --rw="+str(
                    run)+" --filename=/home/"+str(device)+" --numjobs="+str(numjobs)+" --time_based --runtime="+fio_runtime+" --group_reporting"
                print(command)

                for i in range(0, n_iterations):
                    os.system("sleep 2")  # Give time to finish inflight IOs
                    output = subprocess.check_output(command, shell=True)
                    if "write" in run:
                        fio_type_offset = 41

                    # fio is called with --group_reporting. This means that all
                    # statistics are group for different jobs.

                    # throughput
                    throughput = throughput + float(
                        output.split(";")
                        [fio_type_offset + fio_iops_pos - 1])

                    # iops
                    iops = iops + float(output.split(";")
                                        [fio_type_offset + fio_iops_pos])

                # throughput
                result = result+str(throughput / n_iterations)

                # iops
                result = result+";"+str(iops / n_iterations)

                print(result)
                f.write(result+"\n")
                f.flush()

f.closed
