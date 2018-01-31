#!/usr/bin/env python
import os
import re
import sys
import multiprocessing

def get_log_file(path):
        log_file = []
        for root,dirs,files in os.walk(path):
                for file in files:
                        if '.log' in file:
                            log_file.append(os.path.join(root,file))
        return log_file

def check_iops(log):
        f = open(log,'r')
        comm = f.read()
        logfile = log.split('/')[-1]
        if 'err= 0' in comm:
                print('%s file run fio Passed!' %logfile)
                iops = re.findall('IOPS=(.*), BW', comm)
                #iops = re.findall('IOPS=([0-9]*\.[0-9]*[a-z]), BW', comm)
                latency = [int(float(i)*1000) for i in re.findall(' lat \(msec\):.*avg=([0-9]*\.[0-9]*)', comm)]
                latencyu = [int(float(i)) for i in re.findall(' lat \(usec\):.*avg=([0-9]*\.[0-9]*)', comm)]
                latency.extend(latencyu)
                print('Log file is:%s IOPS is:%s' %(logfile, iops))
                print('Log file is:%s Latencym is:%s' %(logfile, latency))
                #print('Log file is:%s Latencyu is:%s' %(logfile, latencyu))
                #print(re.findall('IOPS=[0-9]*', comm))
        else:
                print('%s file run fio Error!' %log)
                exit(1)
        return (iops, latency)

def total(obj):
        iops, latency = obj.get()
        Iops.append(iops)
        Latency.append(latency)


if __name__ == '__main__':
        if len(sys.argv) != 2:
                print('check_iops.py file path.')
                exit(1)
        path = sys.argv[1]
        log = get_log_file(path)
        sumlat = 0
        summary = []
        Iops = [] 
        Latency = []
        totally_iops = 0
        totally_latency = 0
        pool = multiprocessing.Pool(processes=len(log))
        for i in log:
                summary.append(pool.apply_async(check_iops, (i,)))
                #Iops.append(summary[0])
                #Latency.append(summary[1])
        pool.close()
        pool.join()
        print('Get iops and latency done!')
        #for i in summary:
        #        iops, latency = i.get()
        #        Iops.append(iops)
        #        Latency.append(latency)
        [total(i) for i in summary]
        print('Each Iops is:', Iops)
        print('Each Latency is:', Latency)
        for iops in Iops:
                for i in iops:
                        if 'k' in i:
                            totally_iops = totally_iops + int(float(i.split('k')[0])*1000)
                        else:
                            totally_iops = totally_iops + int(float(i))
        for latency in Latency:
                for l in latency:
                    sumlat = sumlat + 1
                    totally_latency = totally_latency + l
        print('Number of latency is:', sumlat)
        print('Totally Iops is:', totally_iops)
        print('Totally Latency is:', int(totally_latency/sumlat))

