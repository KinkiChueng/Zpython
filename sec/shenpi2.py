#!/usr/bin/env python
#coding=utf-8 

import time
import sys
import glob
import csv
import MySQLdb,codecs

def getDate():
        useTime = time.strftime('%Y%m%d',time.localtime(time.time() - 24*60*60))
        return useTime
	#return sys.argv[1]

def compute(day):
	dictB={}
	routebefore = "/root/Zpython/sec/a"
	readbefore = open(routebefore, "r")
	for line in readbefore:
		dictB[line.split('#')[0]]=line.strip('\r').strip('\n')
	#if day < 10:
	routelog = "/data/logs/loginlog/%s.log" % (day)
	#else:
	#	routelog = "/data/logs/loginlog/201512%s.log" % (day)
	dict={}
	readfile = open(routelog, "r")
	for line in readfile:
		if line.split('\t')[4] == "shenpi":
			format = '%Y-%m-%d'
			value = time.localtime(float(line.split('\t')[0]))
			lasttime = time.strftime(format,value)
			number = line.split('\t')[5].strip('\n').strip('\r')
                	if dict.has_key(number):
				timestamp=lasttime+"#"+str(int(dict[number].split('#')[1])+1)
				dict[number]=timestamp
                   	else:
                        	dict.setdefault(number,"")
				if dictB.has_key(number):
					timestamp=lasttime+"#"+str(int(dictB[number].split('#')[3])+1)
					#print timestamp
				else:
					timestamp=lasttime+"#1"
					#print 'aaa'
                              	dict[number]=timestamp

	for num in dictB:
		#print dict.has_key(num)
		if dict.has_key(num) == False:
			print dictB[num]

	route = "/data/logs/loginlog/stub.csv"
	route2 = "/data/logs/loginlog/type.csv"
	reader = csv.reader(file(route,'rb'))
	reader2 = csv.reader(file(route2,'rb'))   	
	type = {}
	for line2 in reader2:
		if type.has_key(line2[0])==False:
			type[line2[0]]=line2[1]
	route = "/data/logs/loginlog/stub.csv"
	reader = csv.reader(file(route,'rb'))
	for line in reader:
		if dict.has_key(line[0].strip()):	
			if line[4].strip() == "审核完毕（已通过）":
				if type.has_key(line[2]):
					#print line[0].strip() + "#" + line[1] + "#" + dict[line[0].strip()] + "#" + line[2] + "#finish#" + type[line[2]]
					
					storage(line[0].strip(),line[1],dict[line[0].strip()].split('#')[0],dict[line[0].strip()].split('#')[1],"finish",type[line[2]])
			elif line[4].strip() == "审核中":
				if type.has_key(line[2]):
                                	print line[0].strip() + "#" + line[1] + "#" + dict[line[0].strip()] + "#" + line[2] + "#continue#" + type[line[2]]
			else:
				if type.has_key(line[2]):
					#print line[0].strip() + "#" + line[1] + "#" + dict[line[0].strip()] + "#" + line[2] + "#failed#" + type[line[2]]
					storage(line[0].strip(),line[1],dict[line[0].strip()].split('#')[0],dict[line[0].strip()].split('#')[1],"failed",type[line[2]])

def storage(id,starttime,endtime,num,status,type):
        try:
                conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
                cur=conn.cursor()
                cur.execute('insert into TONGJI_FLOW(id,starttime,endtime,num,status,type) values(%s,%s,%s,%s,%s,%s)',(id,starttime,endtime,num,status,type))
                        
                conn.commit()
                cur.close()
                conn.close()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
	day=getDate()
	dict=compute(day)
	#storage(dict)
