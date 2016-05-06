#!/usr/bin/env python

import sys
from datetime import *
import datetime
import os
import glob
import MySQLdb,codecs

def compute(result):
        dict = {}
	for filename in result:
        	route = "/data/logs/"+str(yesterday)+ "/" + filename
        	readfile = open(route, "r")
        	for line in readfile:
                	uid = line.split('\t')[4]
			system = line.split('\t')[6]
                	if dict.has_key(system):
                        	dict[system].add(uid)
                	else:
                        	dict.setdefault(system,set())
	                       	dict[system].add(uid)
        return dict

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

def getDate():
	yesterday = date.today() + datetime.timedelta(-1)
	return yesterday

def storage(yesterday,dict):
	try:
		conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
		cur=conn.cursor()
		for system in dict:
        		cur.execute('insert into TONGJI_OS values(%s,%s,%s)',(yesterday, system, len(dict[system])))
			print yesterday, system, len(dict[system])
			conn.commit()
        	cur.close()
        	conn.close()
	except MySQLdb.Error,e:
        	print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
	yesterday = str(getDate())
	first = '/data/logs/'+yesterday
	result=findfiles(first,'WRITEaccess_sta.*')
	dict=compute(result)
	storage(yesterday,dict)
