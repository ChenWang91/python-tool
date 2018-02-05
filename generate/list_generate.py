#!/usr/bin/env python
l = (x*x for x in range(5))
print('The first number is', l.next())
print('The second number is', l.next())

num = 3
for i in l:
    print('The %d number is %d' %(num,i))
    num = num + 1
