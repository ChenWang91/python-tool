#!/usr/bin/env python

from collections import namedtuple

class tup(object):
    __name = "test"
    
    def __init__(self, name):
        self.__name = name

    def test(self):
        Point = namedtuple('Point', ["x", "y"])
        p = Point(1,2)
        print("x is {0}, and y is {1}".format(p.x, p.y))

if __name__ == "__main__":
    t = tup("Mytest")
    print("protect name is {0}".format(t._tup__name))
    t.test()
