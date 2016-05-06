#!/usr/bin/env python

import sys

dir = {}
readfile = open("/data/logs/2015-12-01/WRITEaccess_sta.2015120114", "r")
for line in readfile:
	uid = line.split()[4]
	OS = line.split()[6]
	if OS in dir:
		dir[OS].add(uid)
	else:
		dir.setdefault(OS, set())
		dir[OS].add(uid)
for uri in dir:
        print uri, len(dir[uri])
