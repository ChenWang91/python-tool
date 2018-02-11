#!/usr/bin/env python
def my_closer(b):
    a = 2
    def test():
        #nonlocal a
        print('b is', b)
        print('a is', a)
        #a = 5
    return test
if __name__ == '__main__':
    t = my_closer(5)
    t()
