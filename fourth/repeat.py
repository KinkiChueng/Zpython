#!/usr/bin/env python

import os
import glob

def compute(i):
	dict={}
	for num in range(i,i+5):
		#route = "/data/logs/2015-12-0"+str(num)+"WRITEaccess_sta.2015121100"
		first = '/data/logs/2015-12-0'+str(num)
		if num >= 10:
			first = '/data/logs/2015-12-'+str(num)
		result=findfiles(first,'WRITEaccess_sta.*')
		for filename in result:
			readfile = open(first+"/"+filename, "r")
			for line in readfile:
				if dict.has_key(line.split('\t')[4]):
					dict[line.split('\t')[4]].add(line.split('\t')[1])
				else: 
					dict.setdefault(line.split('\t')[4],set())
					dict[line.split('\t')[4]].add(line.split('\t')[1])
		readfile.close	
	return dict
			
def mix():
	i = 0.0
	j = 0.0
	res1 = compute(1)
	res2 = compute(6)
	key1 = res1.keys()
	key2 = res2.keys()
	key3 = set(key1) & set(key2)
	for key in key2:
		i += len(res2[key])
	for key in key3:
		j += len(res2[key])
	print j/i,i,j
	
def findfiles(dirname,pattern):
        cwd = os.getcwd()
        if dirname:
                os.chdir(dirname)

        result = []
        for filename in glob.iglob(pattern):
                result.append(filename)
        #compute(result,yesterday)
        #result.append(filename)
        os.chdir(cwd)
        return result

if __name__ == '__main__':
	mix()
