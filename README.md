# python-tool

Demos for using different python libraries.

# Catalogue:

* [argv](#Argv)
* [autossh](#Autossh)


<a id="Argv"></a>
## argv

How to use sys and argparse libraries to parse the parameters from python script.


<a id="Autossh"></a>
## autossh

###ssh_fio.py
Use multiprocess, paramiko, subprocess, ftplib modules to run multi VMs, and log into VMs run fio job at the same time.
Download the result file after fio job end.

~~~{.sh}
./autossh.py vmnumber runtime
~~~

###get_iops_latency.py
Use multiprocess modul to get the Iops and Latency in ".log" files from  path whcih user submit.

~~~{.sh}
./get_iops_latency.py logpath
~~~
