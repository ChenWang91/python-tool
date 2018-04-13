#!/usr/bin/env python
from subprocess import check_output, call, Popen, PIPE
import sys
import time
import pdb

def get_pcie_address():
    p = Popen("lspci -nnn|grep Non|awk '{print $1}'", stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    p.wait()
    pcie = p.stdout.readlines()
    address = []
    for i in pcie:
        address.append("'--filename=trtype=PCIe traddr=0000." + i.strip('\n').replace(':', '.') + ' ns=1\'')
    return address[4]

def change_config(kind, address, rw_type, queue_depth):
    if kind == "spdk":
        job = "fioplugin.job"
        rwjob = "rwfioplugin.job"
    else:
        job = "fio.job"
        rwjob = "rwfio.job"
    if rw_type != "randrw":
        #old_res = check_output("cat fioplugin.job", shell=True)
        rc=call("sed -i 's/\(rw=\).*/rw=%s/g' %s" %(rw_type, job), shell=True)
        rc=call("sed -i 's/\(iodepth=\).*/iodepth=%d/g' %s" %(queue_depth, job), shell=True)
        print "Changed file is %s" %job
        #new_res = check_output("cat fioplugin.job", shell=True)
        name = kind + "_" + "4K_%s_%d" %(rw_type, queue_depth) + ".log"
    else:
        #old_res = check_output("cat rwfioplugin.job", shell=True)
        rc=call("sed -i 's/\(iodepth=\).*/iodepth=%d/g' %s" %(queue_depth, rwjob), shell=True)
        print "Changed file is %s" %rwjob
        #new_res = check_output("cat rwfioplugin.job", shell=True)
        name = kind + "_" + "4K_70%%_read_30%%_write_%d" %queue_depth + ".log"
    performance(kind, address, name)

def get_cpu_usage(p, cpu_file):
    while True:
        if Popen.poll(p) is not None:
            print "Fio is Over!"
            break
        else:
            print "Fio is still Running"
            cpu = check_output("./cpu/ptumon -t 1|grep CPU1|awk '{print $11}'", shell=True).split('\n')[0]
            print "Cpu usage is: %s%%" %cpu
            call("echo '%s' >> %s" %(cpu, cpu_file), shell=True)
            time.sleep(120)


def performance(kind, address, name):
    if kind == "spdk":
        if "70%" in name:
            command = "/usr/src/fio/fio rwfioplugin.job "
        else:
            command = "/usr/src/fio/fio fioplugin.job "
        #total_command = command + reduce(lambda x,y:x+" "+y, address) + " > %s 2>&1" %name
        total_command = command + address + " > %s 2>&1" %name
        print "Start run test case with command:", total_command
        p = Popen(total_command, shell=True)
    else:
        if "70%" in name:
            command = "/usr/src/fio/fio rwfio.job > %s 2>&1" %name
        else:
            command = "/usr/src/fio/fio fio.job > %s 2>&1" %name
        print "Start run test case with command:", command
        p = Popen(command, shell=True)

    cpu_file = name.replace('.log', '.cpu')
    get_cpu_usage(p, cpu_file)

if __name__ == '__main__':
    test_cases = {
            "randread":[1,8,32,128,256],
            "randwrite":[1,8,32,128,256],
            "randwrite":[1,8,32,128,256],
            "randrw":[1,8,32,128,256]
            }
    if len(sys.argv) != 2 or sys.argv[1] not in ["spdk", "kernel"]:
        print("Need add type of test, such like spdk or kernel")
        sys.exit()
    elif sys.argv[1] == "spdk":
        address = get_pcie_address()
        print address
        [change_config("spdk", address, k, i) for k, v in test_cases.items() for i in v]
    else:
        [change_config("kernel", [], k, i) for k, v in test_cases.items() for i in v]

