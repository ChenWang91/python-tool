#!/usr/bin/env python
import sys

class parse(object):
	def __init__(self):
		pass
	def par(self):
		num = len(sys.argv)
		for i in range(num):
			print('The %d parameter is %s.' %(i,sys.argv[i])) 
		flag = 0
		for parameter in sys.argv[1:]:
			flag+=1
			if parameter == '-h' or parameter == '--help':
				print('*********************')
			elif parameter == '-v' or parameter == '--version':
				print('Version is:', sys.argv[flag+1])
			else:
				print('More')
if __name__ == '__main__':
	parse().par()
