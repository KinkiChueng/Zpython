#!/usr/bin/env python

def transfer():
        trans = {};
        route = "/root/Zpython/menusTranChinese.txt"
        readfile = open(route, "r")
        for line in readfile:
                type = line.split()[1]
                uri = line.split()[0]
                if type in trans:
                        trans[type].add(uri)
                else:
                        trans.setdefault(type, set())
                        trans[type].add(uri)
	print trans.keys()

if __name__ == '__main__':
	transfer()
