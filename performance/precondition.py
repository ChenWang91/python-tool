#!/usr/bin/env python
from subprocess import check_output,call,Popen,PIPE
import sys

def get_pcie_address():
    p = Popen("lspci -nnn|grep Non|awk '{print $1}'", stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    p.wait()
    pcie = p.stdout.readlines()
    address = []
    for i in pcie:
        address.append("'trtype:PCIe traddr:0000:" + i.strip('\n') + '\'')
    return address

def run_perf(path, address):
    write_command = path + ' -q 32 -s 131072 -w write -t 7200 -c 0xFE000000'
    rand_write_command = path + ' -q 32 -s 4096 -w randwrite -t 7400 -c 0xFE000000'
    for i in address:
        write_command = write_command + " -r " + "%s" %i
        rand_write_command = rand_write_command + " -r " + "%s" %i
    print write_command
    print rand_write_command
    print("Run perf with following command:", write_command)
    rc = call(write_command, shell=True)
    if rc != 0:
        print("Run perf failed!")
        sys.exit()
    print("Run perf with following command:", rand_write_command)
    rc = call(rand_write_command, shell=True)
    if rc != 0:
        print("Run perf failed!")
        sys.exit()
    print("Precondition Done!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Nedd add perf path! Such like:")
        print("./precondition.py /home/spdk/perf/perf")
        sys.exit()
    else:    
        pcie_address = get_pcie_address()
        run_perf(sys.argv[1], pcie_address)
