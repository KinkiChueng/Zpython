#!/usr/bin/env python

import sys
from datetime import *
import time
import datetime

day = datetime.datetime.now() - datetime.timedelta(days=1)
now = date.today() + datetime.timedelta(-1)
otherStyle = time.strftime('%Y%m%d', now)
#print day.isoformat()
print otherStyle 
