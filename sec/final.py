#!/usr/bin/env python
#coding=utf-8 

import sys
import time
import glob
import csv
import MySQLdb,codecs

def getDate():
        useTime = time.strftime('%Y%m%d',time.localtime(time.time() - 24*60*60))
        return useTime
	#return sys.argv[1]

def compute(day):
	dict={}
	routebefore = "/root/Zpython/sec/a"
	readbefore = open(routebefore, "r")
	for line in readbefore:
		dict[line.split('#')[0]]=line.strip('\r').strip('\n')
	readbefore.close()

	routelog = "/data/logs/loginlog/%s.log" % (day)
	#dict={}
	readfile = open(routelog, "r")
	for line in readfile:
		if line.split('\t')[4] == "shenpi":
			format = '%Y-%m-%d'
			tmptime = time.localtime(float(line.split('\t')[0]))	##time
			lasttime = time.strftime(format,tmptime)
			message = line.split('\t')[5].strip('\n').strip('\r')	##value  项目立项申请表#2bb6a4551a8244b38546fbc1886487c0#continue
                	number = message.split('#')[1]
			if dict.has_key(number):
				timestamp=number+"#"+dict[number].split('#')[1]+"#"+lasttime+"#"+message.split('#')[2]+"#"+str(int(dict[number].split('#')[4])+1)+"#"+message.split('#')[0]
				dict[number]=timestamp
                   	else:
                        	dict.setdefault(number,"")
				timestamp=number+"#"+lasttime+"#"+lasttime+"#"+message.split('#')[2]+"#1#"+message.split('#')[0]
				dict[number]=timestamp
	readfile.close()
	traverse(dict)

def transtime(start,end):
	timeArray = time.strptime(start, "%Y-%m-%d")
	startStamp = int(time.mktime(timeArray))
	timeArray = time.strptime(end, "%Y-%m-%d")
	endStamp = int(time.mktime(timeArray))
	#print strptime(endStamp-startStamp,"d")
	if endStamp-startStamp == 0:
                return 1
        else:
                return (endStamp-startStamp)/60/60/24 + 1

def traverse(dict):
	beforewrite = open("/root/Zpython/sec/a",'w')
	for value in dict:
		if dict[value].split('#')[3] == "start" or dict[value].split('#')[3] == "continue":
			try:
				beforewrite.writelines(dict[value]+"\r\n")
			except Exception:
				print dict[value]
		elif dict[value].split('#')[3] == "failed" or dict[value].split('#')[3] == "end":	
			try:
				#print dict[value].split('#')[1],dict[value].split('#')[2]
				con=transtime(dict[value].split('#')[1],dict[value].split('#')[2])
				storage(value,dict[value].split('#')[1],dict[value].split('#')[2],con,dict[value].split('#')[4],dict[value].split('#')[3],dict[value].split('#')[5])
			except Exception:
				print value,dict[value].split('#')[1],dict[value].split('#')[2],dict[value].split('#')[4],dict[value].split('#')[3],dict[value].split('#')[5]
	beforewrite.close()		

def storage(id,starttime,endtime,con,num,status,type):
        try:
                conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
                cur=conn.cursor()
                cur.execute('insert into TONGJI_FLOW(id,starttime,endtime,con,num,status,type) values(%s,%s,%s,%s,%s,%s,%s)',(id,starttime,endtime,con,num,status,type))
                print id,starttime,endtime,con,num,status,type       
                conn.commit()
                cur.close()
                conn.close()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
	day=getDate()
	print day
	dict=compute(day)
	#storage(dict)
