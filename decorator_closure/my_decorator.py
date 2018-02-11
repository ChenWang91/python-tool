#!/usr/bin/env python
import time
def my_time(func):
    def inner(*args, **kwargs):
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
    time.sleep(5)
    print('This is test1')

@my_time
def test2():
    time.sleep(4)
    print('This is test2')

if __name__ == '__main__':
    print test1()
    print test2()
