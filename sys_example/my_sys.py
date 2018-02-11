#!/usr/bin/env python
import sys
import time

for i in range(5):
    print('Number is %d' %i),
    sys.stdout.flush()
    time.sleep(1)

