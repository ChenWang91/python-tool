# python-tool

Demos for using different python libraries.

# Catalogue:

* [argv](#Argv)
* [autossh](#Autossh)
* [generate](#Generate)
* [higherdef](#Higherdef)


<a id="Argv"></a>
## argv

How to use sys and argparse libraries to parse the parameters from python script.


<a id="Autossh"></a>
## autossh

autossh.py

Use multiprocess, paramiko, subprocess, ftplib modules to run multi VMs, and log into VMs run fio job at the same time.
Download the result file after fio job end.

~~~{.sh}
./autossh.py vmnumber runtime model
~~~

get_iops_latency.py

Use multiprocess module to get the Iops and Latency in ".log" files from  path whcih user submit.

~~~{.sh}
./get_iops_latency.py logpath
~~~

<a id="Generate"></a>
## generate

list_generate.py

change "[]" to "()" in list comprehension and become python generate

generate.py

example about python generator(yield, next(), send()).

coroutine.py

example about python coroutine with generator

<a id="Higherdef"></a>
## higherdef

selfhigher.py

example about python higher-order functions:
map(), reduce(), filter(), sum(), any(), all()
