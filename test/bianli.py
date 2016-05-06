#!/usr/bin/env python

import sys

import os
import glob

def findfiles(dirname,pattern):
    cwd = os.getcwd()
    if dirname:
        os.chdir(dirname)

    result = []
    for filename in glob.iglob(pattern):
        result.append(filename)
    os.chdir(cwd)
    return result

if __name__ == '__main__': print(findfiles('/data/logs/2015-12-06/','WRITEaccess_sta.*'))
