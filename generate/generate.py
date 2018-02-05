#!/usr/bin/env python

def test_generate(num):
    while num < 5:
        i = yield num
        print i
        num = num + 1
if __name__ == '__main__':
    nu = 3
    ge = test_generate(0)
    print('Return first number is:', ge.next())
    print('Return second number is:', ge.next())
    for i in ge:
        print('The %d num in generate is %d' %(nu,i))
        nu = nu + 1
    ge2 = test_generate(0)
    print ge2.next()
    print ge2.send(4)
    print ge2.next()
