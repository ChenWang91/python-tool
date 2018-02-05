#!/usr/bin/env python
import time

def target():
    m = ''
    while True:
        n = yield m
        if not n:
            print 'NO'
            m = 'ERROR'
        else:
            print('[target] is %d' %n)
            time.sleep(1)
            m = '200 OK'

def initiator(obj):
    obj.next()
    n = 0
    while n < 5:
        print('[initiator] is %d' %n)
        m = obj.send(n)
        print('[target return %s]' %m)
        n = n + 1
    obj.close()

if __name__ == '__main__':
    obj = target()
    initiator(obj)
