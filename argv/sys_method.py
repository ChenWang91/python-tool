#!/usr/bin/env python
import sys
import argparse

class parse(object):
	def __init__(self,num):
		self.num = num
	def par(self):
		if self.num == 1:
			print '1'
		else:
			print '2'

if __name__ == '__main__':
	num = int(sys.argv[-1])
	print '#########%d' %num
	parse(num).par()
