#!/usr/bin/env python

import sys
import time

ISOTIMEFORMAT='%Y-%m-%d %X'
t = time.time()
timeArray = time.localtime(1449550768)
otherStyle = time.strftime(ISOTIMEFORMAT, timeArray)
print otherStyle

ISOTIMEFORMAT='%H'
t = time.time()
timeArray = time.localtime(t)
otherStyle = time.strftime(ISOTIMEFORMAT, timeArray)
print otherStyle
