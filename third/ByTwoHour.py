#!/usr/bin/env python

import datetime
import time
import os
import glob
import MySQLdb,codecs

def getDate():
        mon = int(time.strftime('%Y%m',time.localtime(time.time())))-1
        year = int(time.strftime('%Y',time.localtime(time.time())))-1
        if mon==0:
                mon=str(year)+'12'
        return mon

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

def transtime(timestamp):
	return int(str(time.strftime('%Y%m%d-%H',time.localtime(timestamp))).split("-")[1])

def compute(result):
        dict = {}
        for filename in result:
                route = "/data/logs/loginlog/" + filename
                readfile = open(route, "r")
		for i in range(0,24,2):
			dict.setdefault(str(i)+"-"+str(i+2), list())
                for line in readfile:
			uname = line.split('\t')[1]
			try:
				tmp = transtime(int(line.split('\t')[0]))
			except Exception:
				print line.split('\t')[0]
				#print transtime(int(line.split('\t')[0].strip('\r').strip('\n')))
			for key in dict:
			#print key
				if (tmp >= int(key.split("-")[0]) and tmp < int(key.split("-")[1])):
					#print "aaaa"
					dict[key].append(uname)
	return dict



def storage(dict):
        try:
                conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
                cur=conn.cursor()
                for hourCut in dict:
                        cur.execute('insert into MONTH_PV_UV(hour,pv,uv) values(%s,%s,%s)',(hourCut,len(dict[hourCut]),len(set(dict[hourCut]))))
                       # print yesterday, system, len(dict[system])
                        conn.commit()
                cur.close()
                conn.close()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__': 
	mon = str(getDate())
	#mon = "201512"
	first = '/data/logs/loginlog/'
	result=findfiles(first,mon+'*.log')
	#print result
	dict = compute(result)
	storage(dict)
