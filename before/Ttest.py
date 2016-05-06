#!/usr/bin/env python

import sys

dir = {}
readfile = open("/data/logs/2015-12-01/WRITEaccess_sta.2015120114", "r")
for line in readfile:
        uid = line.split()[4]
        uri = line.split()[1]
        if uri in dir:
		dir[uri].append(uid)
	else:
		dir.setdefault(uri, list())
		dir[uri].append(uid)
for uri in dir:
	i = len(dir[uri])
	s = set(dir[uri])
	print uri, i, len(s)
