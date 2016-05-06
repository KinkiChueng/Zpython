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
		#readfile = open("/data/logs/2015-12-01/WRITEaccess_sta.2015120114", "r")
		for line in readfile:
        		uid = line.split()[4]
        		uri = line.split()[1]
        		if uri in dict:
				dict[uri].append(uid)
			else:
				dict.setdefault(uri, list())
				dict[uri].append(uid)
	return dict
		#for uri in dir:
		#	i = len(dir[uri])
		#	s = set(dir[uri])
		#	print uri, i, len(s)


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
		for uri in dict:
			i = len(dict[uri])
			s = set(dict[uri])
			print uri, i, len(s)
                       	cur.execute('insert into TONGJI_DOC values(%s,%s,%s,%s)',(yesterday, uri, i, len(s)))
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
