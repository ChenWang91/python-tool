#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys
import time
from subprocess import Popen, call, check_output, PIPE
import paramiko
import multiprocessing
from ftplib import FTP
import pdb
def run_vm_spdk(n):
        if n < 10:
            p = Popen('/home/wangchen/qemu.vhost/build/x86_64-softmmu/qemu-system-x86_64 \
                    -cpu host -smp 8 -m 2048 -object \
                    memory-backend-file,id=mem,size=2G,mem-path=/dev/hugepages,share=on \
                    -numa node,memdev=mem -drive \
                    file=/var/lib/libvirt/images/snapshot%i.img,if=none,id=disk \
                    -device ide-hd,drive=disk,bootindex=0 -net \
                    user,hostfwd=tcp::1000%i-:22 -net nic -chardev \
                    socket,id=char0,path=/home/wangchen/spdk.vhost/vhost.%i \
                    -device vhost-user-nvme,chardev=char0,num_io_queues=32 --enable-kvm' %(n,n,n), shell=True)
        elif n < 100:
            p = Popen('/home/wangchen/qemu.vhost/build/x86_64-softmmu/qemu-system-x86_64 \
                    -cpu host -smp 8 -m 2048 -object \
                    memory-backend-file,id=mem,size=2G,mem-path=/dev/hugepages,share=on \
                    -numa node,memdev=mem -drive \
                    file=/var/lib/libvirt/images/snapshot%i.img,if=none,id=disk \
                    -device ide-hd,drive=disk,bootindex=0 -net \
                    user,hostfwd=tcp::100%i-:22 -net nic -chardev \
                    socket,id=char0,path=/home/wangchen/spdk.vhost/vhost.%i \
                    -device vhost-user-nvme,chardev=char0,num_io_queues=8 --enable-kvm' %(n,n,n), shell=True)
        else:
            p = Popen('/home/wangchen/qemu.vhost/build/x86_64-softmmu/qemu-system-x86_64 \
                    -cpu host -smp 8 -m 2048 -object \
                    memory-backend-file,id=mem,size=2G,mem-path=/dev/hugepages,share=on \
                    -numa node,memdev=mem -drive \
                    file=/var/lib/libvirt/images/snapshot%i.img,if=none,id=disk \
                    -device ide-hd,drive=disk,bootindex=0 -net \
                    user,hostfwd=tcp::10%i-:22 -net nic -chardev \
                    socket,id=char0,path=/home/wangchen/spdk.vhost/vhost.%i \
                    -device vhost-user-nvme,chardev=char0,num_io_queues=8 --enable-kvm' %(n,n,n), shell=True)


def run_vm_kernel(n):
        if n < 10:
            p = Popen('/home/wangchen/qemu.vhost/build/x86_64-softmmu/qemu-system-x86_64 \
                    -cpu host -smp 8 -m 2048 -object \
                    memory-backend-file,id=mem,size=2G,mem-path=/dev/hugepages,share=on \
                    -numa node,memdev=mem -drive \
                    file=/var/lib/libvirt/images/snapshot%i.img,if=none,id=disk \
                    -device ide-hd,drive=disk,bootindex=0 -net \
                    user,hostfwd=tcp::1000%i-:22 -net nic -drive \
                    format=raw,file=nvme%d.img,if=none,id=nvmedrive \
                    -device nvme,drive=nvmedrive,serial=1234 --enable-kvm' %(n,n,n), shell=True)
        elif n < 100:
            p = Popen('/home/wangchen/qemu.vhost/build/x86_64-softmmu/qemu-system-x86_64 \
                    -cpu host -smp 8 -m 2048 -object \
                    memory-backend-file,id=mem,size=2G,mem-path=/dev/hugepages,share=on \
                    -numa node,memdev=mem -drive \
                    file=/var/lib/libvirt/images/snapshot%i.img,if=none,id=disk \
                    -device ide-hd,drive=disk,bootindex=0 -net \
                    user,hostfwd=tcp::100%i-:22 -net nic -drive \
                    format=raw,file=nvme%d.img,if=none,id=nvmedrive \
                    -device nvme,drive=nvmedrive,serial=1234 --enable-kvm' %(n,n,n), shell=True)

        else:
            p = Popen('/home/wangchen/qemu.vhost/build/x86_64-softmmu/qemu-system-x86_64 \
                    -cpu host -smp 8 -m 2048 -object \
                    memory-backend-file,id=mem,size=2G,mem-path=/dev/hugepages,share=on \
                    -numa node,memdev=mem -drive \
                    file=/var/lib/libvirt/images/snapshot%i.img,if=none,id=disk \
                    -device ide-hd,drive=disk,bootindex=0 -net \
                    user,hostfwd=tcp::10%i-:22 -net nic -drive \
                    format=raw,file=nvme%d.img,if=none,id=nvmedrive \
                    -device nvme,drive=nvmedrive,serial=1234 --enable-kvm' %(n,n,n), shell=True)


def start_vm(num, model):
        hugemem = (num+5) * 2048
        rc = call('HUGEMEM=%d  /home/wangchen/spdk.vhost/scripts/setup.sh' %hugemem, shell=True)
        if rc == 0:
                print('Hugemem set successfully')
        else:
                print('Hugemem set failed')
                exit(1)
        if model == 'spdk':
            [run_vm_spdk(i) for i in range(num)]
        elif model == 'kernel':
            [run_vm_kernel(i) for i in range(num)]


def login_vm(port,password,runtime):
        print('Start time is:', time.time())
        try:
                paramiko.util.log_to_file("filename.log")
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect('localhost', port = int(port), username = 'root', password = password, allow_agent=False, look_for_keys=False, timeout=60)
                sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
                sftp = ssh.open_sftp()
                #paramiko.util.log_to_file("filename.log")
                sftp.put("/root/fio_multi_test.job", "/root/fio_multi_test.job")
                fio_patch = '/root/fio_%s.log' %port
                fio_command = "fio /root/fio_multi_test.job > %s 2>&1" %fio_patch
                command = "sed -i 's/runtime=[0-9]*/runtime=%s/' /root/fio_multi_test.job" %runtime
                stdin, stdout, stderr = ssh.exec_command(command)
                if len(stderr.readlines()) != 0:
                        print('Error message is:' %stderr.readlines())
                        exit(1)
                else:
                        print('Change runtime successfully!')
                print('Fio command is:', fio_command)
                stdin, stdout, stderr = ssh.exec_command(fio_command)

                start_time = time.time()
                flag = True
                while flag:
                        stdin, stdout, stderr = ssh.exec_command("ps aux | grep fio_multi_test.job | grep -v grep | awk '{print$2}'")
                        result = stdout.readlines()
                        print('Fio pid is:', result)
                        end_time = time.time()
                        totall_time = int(end_time) - int(start_time)
                        print('The totall time is:', totall_time)
                        if len(result) == 0 or totall_time > 2400:
                                flag = False
                        time.sleep(1)
                sftp.get(fio_patch, "/home/wangchen/vhostnvme/output/fio_%s.log" %port)
                print('Machine %s is OK!', port[-2:])
                ssh.close()
                sftp.close()
        except pexpect.EOF:
                print('EOF')
                ssh.close()
        except pexpect.TIMEOUT:
                print('TIMEOUT')
                ssh.close()

def kill_vm():
        p = check_output("ps aux|grep snapshot|grep -v grep|awk '{print $2}'", shell=True)
        pid = p.strip().split('\n')
        num = len(pid)
        for i in pid:
            rc = call('kill -9 %s' %i, shell=True)
            if rc == 0:
                print('Kill %s successfully!' %i)
            else:
                print('Kill %s failed!' %i)
        print('The number of VMs is %d, and all the process be killed!' %num)

if __name__ == '__main__':
        if len(sys.argv) != 4:
                print('autossh.py vmnumber runtime model')
                exit(1)
        num = int(sys.argv[1])
        runtime = sys.argv[2]
        model = sys.argv[3]
        if model == 'spdk' or model == 'kernel':
            start_vm(num, model)
        else:
            print("model must be 'spdk' or 'kernel'")
            exit(1)
        if model == 'kernel':
            pid = check_output("ps aux|grep qemu|grep -v grep|awk '{print $2}'", shell=True)
            print('Qemu pid list is:', pid.strip().split('\n'))
            for i in [call('taskset -pc 1 %d' %int(i), shell=True) for i in pid.strip().split('\n')]:
                if i != 0:
                    print('Set cpu core error!')
                    exit(1)
        
        time.sleep(60)
        pool = multiprocessing.Pool(processes=num)
        for i in range(num):
                if i < 10:
                    port = '1000%d' %i
                elif i < 100:
                    port = '100%d' %i
                else:
                    port = '10%d' %i
                pool.apply_async(login_vm, (port, 'intel123', runtime))
        pool.close()
        pool.join()
        print "Sub-process done!"
        kill_vm()
