#!/usr/bin/env python
import sys
from subprocess import call, Popen
import os
import re
import xlwt

def run_fio(typ, qd):
    print("Will run {0} test type and {1} queue depth".format(typ, qd))
    if typ != "randrw":
        rc=call("sed -i 's/\(rw=\).*/rw={0}/g' thick_thin_fio_file".format(typ), shell=True)
        rc=call("sed -i 's/\(iodepth=\).*/iodepth={0}/g' thick_thin_fio_file".format(qd), shell=True)
        rc=call("cat thick_thin_fio_file", shell=True)
        rc=call("fio thick_thin_fio_file > results/{0}_{1}.log".format(typ, qd), shell=True)
        
    else:
        rc=call("sed -i 's/\(iodepth=\).*/iodepth={0}/g' thick_thin_fio_file_rw".format(qd), shell=True)
        rc=call("cat thick_thin_fio_file_rw", shell=True)
        rc=call("fio thick_thin_fio_file_rw > results/{0}_{1}.log".format(typ, qd), shell=True)

def get_results():
    total = {}.fromkeys(test_th)
    test = [i + "_" + str(j) for i in test_type for j in test_qd]
    for i in test_th:
        total[i] = {}.fromkeys(test)
    for i in test_th:
        for j in test:
            total[i][j] = {}.fromkeys(test_rs)

    for root, dirs, files in os.walk("./results/"):
        for f in files:
            rw = f.split('.')[0]
            with open(os.path.join(root, f), 'r') as t:
                comm = t.read()
                if "err= 0" in comm:
                    if "randrw" not in rw :
                        #print "file is ", f
                        iops = re.findall('IOPS=(.*), BW', comm)
                        thick_p99 = int(re.findall('99.00th=\[(.*)\], 99.50th', comm)[0])
                        thin_p99 = int(re.findall('99.00th=\[(.*)\], 99.50th', comm)[1])
                        total['thick'][rw]['iops'] = [int(float(i.split('k')[0])*1000) if 'k' in i else int(i) for i in iops][0]
                        total['thick'][rw]['BW'] = re.findall('BW=(.*) \(', comm)[0].split("MiB/s")[0]
                        total['thin'][rw]['iops'] = [int(float(i.split('k')[0])*1000) if 'k' in i else int(i) for i in iops][1]
                        total['thin'][rw]['BW'] = re.findall('BW=(.*) \(', comm)[1].split("MiB/s")[0]
                        if "read" in rw:
                            total['thin'][rw]['p99_read'] = thin_p99
                            total['thick'][rw]['p99_read'] = thick_p99
                        elif "write" in rw:
                            total['thin'][rw]['p99_write'] = thin_p99
                            total['thick'][rw]['p99_write'] = thick_p99
                    else:
                        iops = re.findall('IOPS=(.*), BW', comm)
                        iops = [int(float(i.split('k')[0])*1000) if 'k' in i else int(i) for i in iops]
                        #iops = str(float(sum(iops))/1000) + 'k'
                        bw = re.findall('BW=(.*) \(', comm)
                        bw = [float(i.split("MiB/s")[0]) for i in bw]
                        p99 = [ int(i) for i in re.findall('99.00th=\[(.*)\], 99.50th', comm)]
                        total['thick'][rw]['iops'] = sum(iops[:2]) 
                        total['thick'][rw]['BW'] = sum(bw[:2])
                        total['thin'][rw]['iops'] = sum(iops[2:4])
                        total['thin'][rw]['BW'] = sum(bw[2:4])
                        total['thin'][rw]['p99_read'] = p99[2]
                        total['thick'][rw]['p99_read'] = p99[0]
                        total['thin'][rw]['p99_write'] = p99[3]
                        total['thick'][rw]['p99_write'] = p99[1]
                        #bw = str(sum(bw)) + "MiB/s"
                else:
                    print("Run fio failed with {0}".format(f))
    return total

def base_excel(table):
    [table.write(0, i, title[i]) for i in range(6)]
    [table.write(i, 0, test_type[0]) for i in range(1,7)]
    [table.write(i, 1, test_qd[i-1]) for i in range(1,7)]
    [table.write(i, 0, test_type[1]) for i in range(7,13)]
    [table.write(i, 1, test_qd[i-7]) for i in range(7,13)]
    [table.write(i, 0, test_type[2]) for i in range(13,19)]
    [table.write(i, 1, test_qd[i-13]) for i in range(13,19)]

def cotent_excel(data, table, number, rw):
    #th = str(table).split('_')[0]
    for k in loc:
        if loc[k] == table:
            th = k.split('_')[0]
    table.write(number, 2, data[th][rw]['iops'])
    table.write(number, 3, data[th][rw]['p99_read'])
    table.write(number, 4, data[th][rw]['p99_write'])
    table.write(number, 5, data[th][rw]['BW'])

def generate_excel(data):
    f = xlwt.Workbook()
    thick_table = f.add_sheet("thick",cell_overwrite_ok=True)
    thin_table = f.add_sheet("thin",cell_overwrite_ok=True)
    for i in range(6):
        thick_table.col(i).width = (30*200)
        thin_table.col(i).width = (30*200)
    base_excel(thick_table)
    base_excel(thin_table)

    global loc
    loc = locals() 

    test = [i + "_" + str(j) for i in test_type for j in test_qd]
    [cotent_excel(data, thick_table, i, test[i-1]) for i in range(1,19)]
    [cotent_excel(data, thin_table, i, test[i-1]) for i in range(1,19)]

    f.save("result.xls")

def main(function):
    if function == "fio":
        [run_fio(i, j) for i in test_type for j in test_qd]
    elif function == "results":
        total = get_results()
        print total
        generate_excel(total)
    else:
        print("function should be 'fio' or 'results'!")
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error! usage should be performance.py fio/results")
        sys.exit()
    else:
        test_qd = [1, 32, 64, 128, 256, 512]
        test_type = ["randread", "randwrite", "randrw"]
        test_th = ["thick", "thin"]
        test_rs = ["iops", "p99_read", "p99_write", "BW"]
        title = ["Access Pattern", "Queue Depth", "IOPS", "P99(us)read", "P99(us)write", "BW(MiB/s)"]
        main(sys.argv[1])
