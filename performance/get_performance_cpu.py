#!/usr/bin/env python
import re
from subprocess import Popen, call, check_output
import sys
import os
import xlwt

def get_log_name(path, name):
    log_name = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if name in file:
                log_name.append(os.path.join(root,file))
    return log_name

def get_iops_lantency(path, rw, queue_depth):
    total = {}
    if rw != "randrw":
        name = rw + '_' + str(queue_depth) + '.log'
        file_name = [i for i in path if name in i][0]
        path = [i.replace(".log",".cpu")for i in path]
        cpu_name = rw + '_' + str(queue_depth) + '.cpu'
        cpu_file_name = [i for i in path if cpu_name in i][0]
    else:
        name = "70%_read_30%_write_" + str(queue_depth) + ".log"
        file_name = [i for i in path if name in i][0]
        path = [i.replace(".log",".cpu")for i in path]
        cpu_name = "70%_read_30%_write_" + str(queue_depth) + ".cpu"
        cpu_file_name = [i for i in path if cpu_name in i][0]

    f = open(file_name, 'r')
    comm = f.read()
    if "err= 0" in comm:
        if rw != "randrw":
            iops = re.findall('IOPS=(.*), BW', comm)[0]
            bw = re.findall('BW=(.*) \(', comm)[0]
            latency = [float(i)*1000 for i in re.findall(' lat \(msec\):.*avg=(.[0-9]*\.[0-9]*)', comm)]
            latencyu = [float(i) for i in re.findall(' lat \(usec\):.*avg=(.[0-9]*\.[0-9]*)', comm)]
            latency.extend(latencyu)
            latency = str(latency[0]) + "(usec)"
        else:
            iops = re.findall('IOPS=(.*), BW', comm)
            iops = [int(float(i.split('k')[0])*1000) if 'k' in i else int(i) for i in iops]
            iops = str(float(sum(iops))/1000) + 'k'
            bw = re.findall('BW=(.*) \(', comm)
            bw = [float(i.split("MiB/s")[0]) for i in bw]
            bw = str(sum(bw)) + "MiB/s"
            latency = [float(i)*1000 for i in re.findall(' lat \(msec\):.*avg=(.[0-9]*\.[0-9]*)', comm)]
            latencyu = [float(i) for i in re.findall(' lat \(usec\):.*avg=(.[0-9]*\.[0-9]*)', comm)]
            latency.extend(latencyu)
            latency = str(sum(latency)/len(latency)) + "(usec)"

        key = rw + '_' + str(queue_depth)
        
    else:
        print "Run fio failed with log:", file_name

    cpu = check_output("cat %s" %cpu_file_name, shell=True)
    cpu = str(max(cpu.split('\n'))) + "%"
    total[key] = {
            "iops":iops,
            "bw":bw,
            "latency":latency,
            "cpu usage":cpu
            }

    print total
    return total

def write_basic(table, title, num):
    queue_depth = [1,8,32,128,256]
    table.write(num,0,title)
    table.write(num,1,queue_depth[num%5-1])

def main(path, savefile):
    test_cases = {
            "randread":[1,8,32,128,256],
            "randwrite":[1,8,32,128,256],
            "randrw":[1,8,32,128,256]
            }
    log_path = get_log_name(path, ".log")

    result = [get_iops_lantency(log_path, k, i) for k, v in test_cases.items() for i in v]
    f = xlwt.Workbook()
    table = f.add_sheet("Result")
    for i in range(6):
        table.col(i).width = (30*200)
    title = ["Access Pattern", "Queue Depth", "Throughput(IOPS)", "BW(MiB/s)", "Avg. Latency(usec)", "CPU %"]
    [table.write(0,i,title[i]) for i in range(6)]
    comms = ["4K 100% Random Read","4K 100% Random Write","4K 70% Read 30% Write"]
    for com in comms:
        [write_basic(table, com, i) for i in range(comms.index(com)*5+1,comms.index(com)*5+6)]
    for i in result[0:5]:
        table.write(1+result.index(i),2,i.values()[0]["iops"])
        table.write(1+result.index(i),3,i.values()[0]["bw"])
        table.write(1+result.index(i),4,i.values()[0]["latency"])
        table.write(1+result.index(i),5,i.values()[0]["cpu usage"])
    for i in result[5:10]:
        table.write(result.index(i)+6,2,i.values()[0]["iops"])
        table.write(result.index(i)+6,3,i.values()[0]["bw"])
        table.write(result.index(i)+6,4,i.values()[0]["latency"])
        table.write(result.index(i)+6,5,i.values()[0]["cpu usage"])
    for i in result[10:15]:
        table.write(result.index(i)-4,2,i.values()[0]["iops"])
        table.write(result.index(i)-4,3,i.values()[0]["bw"])
        table.write(result.index(i)-4,4,i.values()[0]["latency"])
        table.write(result.index(i)-4,5,i.values()[0]["cpu usage"])

    f.save(savefile)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Need add log path and save file"
        sys.exit()
    else:
        main(sys.argv[1], sys.argv[2])
