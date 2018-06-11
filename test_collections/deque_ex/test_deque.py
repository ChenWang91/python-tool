#!/usr/bin/env python
from collections import deque

def test():
    d = deque(["1","2","3"])
    d.append("4")
    d.appendleft("0")
    print d[0]

if __name__ == "__main__":
    test()
