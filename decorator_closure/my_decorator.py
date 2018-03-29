#!/usr/bin/env python
import time
from functools import wraps
def my_time(func):
    @wraps(func)
    def inner(*args, **kwargs):
        '''inner doc'''
        st = time.time()
        func(*args, **kwargs)
        et = time.time()
        total = et - st
        print('function name is', func.__name__)
        print('Total time is', total)
        return total
    return inner
@my_time
def test1():
    '''test1 doc'''
    time.sleep(5)
    print('This is test1')

@my_time
def test2():
    time.sleep(4)
    print('This is test2')

if __name__ == '__main__':
    a=test1()
    b=test2()
    print('Name is:',test1.__name__)
    print('Doc is:',test1.__doc__)

