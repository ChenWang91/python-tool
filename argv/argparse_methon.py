#!/usr/bin/env python
import argparse

class parse(object):
	def __init__(self):
		pass
	def par(self):
		pars = argparse.ArgumentParser()
		pars.add_argument('-o', help='output the command')
		par = pars.parse_args()
		print(par.o)
if __name__ == '__main__':
	parse().par()
