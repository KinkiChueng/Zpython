#!/usr/bin/env python

from datetime import *
import os
import glob
import datetime
import MySQLdb
import sys

def compute(day,result):
        dict={}
	for filename in result:
		route = "/data/logs/"+str(day)+ "/" + filename
		readfile = open(route, "r")
                for line in readfile:
                        for line in readfile:
		#		if "login" in line.split('\t')[1].lower():
	                        if dict.has_key(line.split('\t')[4]):
      	                                #dict[line.split('\t')[4]] += 1
					pass
                       	        else: 
                               	        dict.setdefault(line.split('\t')[4],1)
                                       	#dict[line.split('\t')[4]].add(line.split('\t')[1])
                readfile.close
        return dict

def findfiles(dirname,pattern):
        cwd = os.getcwd()
        if dirname:
                os.chdir(dirname)

        result = []
        for filename in glob.iglob(pattern):
                result.append(filename)
        os.chdir(cwd)
        return result

def getDateDir():
	#yesterday = "2015-12-" + sys.argv[1]
        yesterday = date.today() + datetime.timedelta(-1)
	first = '/data/logs/'+str(yesterday)
        result=findfiles(first,'WRITEaccess_sta.*')
	res1 = compute(yesterday,result)
	#before = "2015-12-" + sys.argv[2]
	before = date.today() + datetime.timedelta(-8)
	sec = '/data/logs/'+str(before)
        result=findfiles(sec,'WRITEaccess_sta.*')
	res2 = compute(before,result)
	storage(yesterday,mix(res1,res2)) 

def mix(res1,res2):
        i = 0.0
        j = 0.0
        key1 = res1.keys()
        key2 = res2.keys()
        key3 = set(key1) & set(key2)
	i = float(len(key1))
	j = float(len(key3))
	return j/i

def storage(yesterday,mix):
        try:
                conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
                cur=conn.cursor()
              #  for hourCut in dict:
                cur.execute('insert into TONGJI_REPEAT(date,res) values(%s,%s)',(yesterday,mix))
                print yesterday
                conn.commit()
                cur.close()
                conn.close()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
	result = getDateDir()
	#dict = compute(result)
	#storage(result)
