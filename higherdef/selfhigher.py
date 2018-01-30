#!/usr/bin/env python

def test_map(li):
	return li + 1

def test_reduce(li, li1):
	return li + li1

def test_filter(li):
	if li % 2 == 0:
		return li

if __name__ == '__main__':
	testlist = [1,2,3,4,5]
	print('Original list is', testlist)
	print('Map function result is:', map(test_map, testlist))
	print('Reduce function result is:', reduce(test_reduce, testlist))
	print('Filter function result is:', filter(test_filter, testlist))
