#!/usr/bin/env python
from collections import Counter

def normal(s):
    c = Counter(s)
    print"The number of 't' is:", c["t"]

def update(s):
    c = Counter(s)
    print"The old number of 't' is:", c["t"]
    c.update(s) #c.update(Counter(s))
    print"The add new number of 't' is:", c["t"]
    c.subtract(s) #c.subtract(Counter(s))
    print"The subtract new number of 't' is:", c["t"]

def delete(s):
    c = Counter(s)
    print"The old counter is", c
    del c["t"]
    print"The new counter is", c
    
def iter(s):
    c = Counter(s)
    print"The iter is", list(c.elements())

def most(s):
    c = Counter(s)
    print"The most is", c.most_common()


if __name__ == '__main__':
    normal("MyTest")
    update("MyTest")
    delete("MyTest")
    iter("MyTest")
    most("MyTest")

