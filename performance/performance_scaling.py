#!/usr/bin/env python
from subprocess import check_output, call, Popen, PIPE
import sys
import time
import pdb

def get_pcie_address(types):
    p = Popen("lspci -nnn|grep Non|awk '{print $1}'", stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    p.wait()
    pcie = p.stdout.readlines()
    address = []
    flag = 0
    for i in pcie:
        if types == "fioplugin":
            #address.append(" --name=job{0} '--filename=trtype=PCIe traddr=0000.".format(flag) + i.strip('\n').replace(':', '.') + ' ns=1\'')
            address.append(" '--filename=trtype=PCIe traddr=0000." + i.strip('\n').replace(':', '.') + ' ns=1\'')
        elif types == "perf":
            address.append(" -r 'trtype:PCIe traddr:0000:" + i.strip('\n') + "'")
        flag = flag + 1
    return address

def run_command(types, num, version):
    fio_command = "/usr/src/fio/fio --ioengine=libaio --group_reporting=1 \
--direct=1 --thread=1 --verify=0 --time_based=1 \
--ramp_time=0 --runtime=1800 --iodepth=256 \
--rw=randread --bs=4096 --name=job0"
    fioplugin_command = "/usr/src/fio/fio --ioengine=/home/wangchen/spdk-{0}/examples/nvme/fio_plugin/fio_plugin --group_reporting=1 \
--direct=1 --thread=1 --verify=0 --time_based=1 \
--ramp_time=0 --runtime=1800 --iodepth=256 \
--rw=randread --bs=4096 --name=job0".format(version)
    #perf_command = "/home/wangchen/spdk-{0}/examples/nvme/perf/perf -c 0xFF -q 256 -s 4096 -w randread -t 1800".format(version)
    perf_command = "/home/wangchen/spdk-{0}/examples/nvme/perf/perf -q 256 -s 4096 -w randread -t 1800".format(version)
    if types == "fio":
        for i in range(num):
            #fio_command = fio_command + " --name=job{0} --filename=/dev/nvme{1}n1".format(i, i)
            fio_command = fio_command + " --filename=/dev/nvme{0}n1".format(i)
        command = fio_command
    elif types == "fioplugin":
        for i in get_pcie_address(types)[:num]:
            fioplugin_command = fioplugin_command + i
        command = fioplugin_command
    elif types == "perf":
        for i in get_pcie_address(types)[:num]:
            perf_command = perf_command + i
        command = perf_command
    return command

def run_test(types, num, version):
    command = run_command(types, num, version) + " > {0}_{1}_{2}.log 2>&1".format(version, types, num)
    print command
    if types == "fio":
        call("/home/wangchen/spdk-18.01/scripts/setup.sh reset", shell=True)
    else:
        call("/home/wangchen/spdk-18.01/scripts/setup.sh", shell=True)

    p = call(command, shell=True)

if __name__ == '__main__':
    test_types = ["fioplugin", "perf", "fio"]
    #test_types = ["fio"]
    num = int(check_output("lspci -nnn|grep Non|wc -l", shell=True).split()[0])
    total_num = [int(i) for i in sys.argv[1].split(',')]
    test_cases = {}
    if max(total_num) > num:
        print ("The number of SSD is {0}. So the number which used to test must less than or equal to it!".format(num))
        sys.exit()
    else:
        test_cases = {i:total_num for i in test_types}
        print ("Will run testcases {0}".format(test_cases))
    for t in ["18.01", "17.10", "17.07"]:
    #for t in ["17.07"]:
        [run_test(k,j,t) for k,v in test_cases.items() for j in v]
    #get_pcie_address()
