#!/usr/bin/env python

from datetime import *
import time
import os
import glob
import MySQLdb,codecs
import sys

def getDate():
	mon = int(time.strftime('%Y%m',time.localtime(time.time())))-1
	year = int(time.strftime('%Y',time.localtime(time.time())))-1
	if mon==0:
		mon=str(year)+'12'
	return mon
	#return sys.argv[1]

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

def storage(yesterday,dict):
        try:
                conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
                cur=conn.cursor()
                for menus in dict:
                        cur.execute('insert into TONGJI_MONTH_MENUS(date,type,uv) values(%s,%s,%s)',(yesterday, menus, len(dict[menus])))
                        print mon, menus, len(dict[menus])
                        conn.commit()
                cur.close()
                conn.close()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def compute(result):
        dict = {}
	for filename in result:
        	route = "/data/logs/loginlog/"+filename
		#print route
        	readfile = open(route, "r")
		for line in readfile:
        	        uid = line.split('\t')[1]
        	        menus = line.split('\t')[4]
			if menus == "fanweng":
				menus = "fangwen"
                	if dict.has_key(menus):
                        	dict[menus].add(uid)
                	else:
                        	dict.setdefault(menus,set())
                        	dict[menus].add(uid)
	#for menus in dict:
	#	print menus,len(dict[menus]),dict[menus]
#	print dict 
        return dict

if __name__ == '__main__':
        mon = str(getDate())
        #mon="201512"
	first = '/data/logs/loginlog/'
       # print mon+'*.log'
	result=findfiles(first,mon+'*.log')
	dict=compute(result)
        storage(mon,dict)
	#print mon
