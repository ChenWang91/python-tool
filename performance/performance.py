#!/usr/bin/env python
from subprocess import call
import re
import sys
import os

def main(test_type):
    for i in range(30):
        call("fio --rw={0} --ioengine=libaio --bs=4k --size=50G \
                --numjobs=64 --iodepth=32 --runtime=600s --name=testrw \
                --group_reporting=1 --direct=1 --norandommap=1 \
                --filename=/dev/sdb > {1}/{2}_{3}.log 2>&1".format(test_type, test_type, test_type, i), shell=True)

def get_results():
    read = []
    randread = []
    for i, j, z in os.walk("/home/wangchen/read"):
        for x in z:
            comm = open(os.path.join(i,x),"r").read()
            if "err= 0" not in comm:
                print("fio error")
            else:
                print("read iops is:",re.findall('iops=(.*), runt', comm))

    for i, j, z in os.walk("/home/wangchen/randread"):
        for x in z:
            comm = open(os.path.join(i,x),"r").read()
            if "err= 0" not in comm:
                print("fio error")
            else:
                print("randread iops is:",re.findall('iops=(.*), runt', comm))

if __name__ =="__main__":
    test_type = ["randread", "read"]
    if len(sys.argv) != 2:
        print("Need input function")
        sys.exit()
    if sys.argv[1] == "fio":
        [main(i) for i in test_type]
    elif sys.argv[1] == "results":
        get_results()
    else:
        print("Needs fio or results!")
        sys.exit()


