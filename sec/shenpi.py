#!/usr/bin/env python
#coding=utf-8 

import time
import sys
import glob
import csv
import MySQLdb,codecs

start = ""
end = ""
def compute():
	dict={}
	for num in range(1,12):
		if num < 10:
			route = "/data/logs/loginlog/2015120%d.log" % (num)
		else:
			route = "/data/logs/loginlog/201512%d.log" % (num)
		
		readfile = open(route, "r")
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
					timestamp=lasttime+"#1"
                               		dict[number]=timestamp
	#print dict
	readfile.close()
	route = "/data/logs/loginlog/stub.csv"
	route2 = "/data/logs/loginlog/type.csv"
	reader = csv.reader(file(route,'rb'))
	reader2 = csv.reader(file(route2,'rb'))   	
	type = {}
	for line2 in reader2:
		if type.has_key(line2[0])==False:
			type[line2[0]]=line2[1]
	for line in reader:
		#try:
		#	pass
			#print dict[line[0].strip('\n').strip('\r')]	
		#except Exception:
		#	print line[0].strip()
		if dict.has_key(line[0].strip()):
			#print dict[line[0].strip()]	
			if line[4].strip() == "审核完毕（已通过）":
				if type.has_key(line[2]):
					#pass
					#print line[0].strip() + "#" + line[1] + "#" + dict[line[0].strip()] + "#" + line[2] + "#finish#" + type[line[2]]
					#transtime(dict[value].split('#')[1],dict[value].split('#')[2])
					storage(line[0],line[1],dict[line[0]].split('#')[0],dict[line[0].strip()].split('#')[1],"end",type[line[2]])
			elif line[4].strip() == "审核中":
				if type.has_key(line[2]):
					#pass
                                	print line[0] + "#" + line[1] + "#" + dict[line[0]].split('#')[0] + "#continue#" + dict[line[0]].split('#')[1] + "#" + type[line[2]]
			else:
				if type.has_key(line[2]):
					#print line[0].strip() + "#" + line[1] + "#" + dict[line[0].strip()] + "#" + line[2] + "#failed#" + type[line[2]]
					#continue = transtime(line[1],dict[line[0]].split('#')[0])
					storage(line[0],line[1],dict[line[0]].split('#')[0],dict[line[0].strip()].split('#')[1],"failed",type[line[2]])


def transtime(start,end):
        timeArray = time.strptime(start, "%Y-%m-%d")
        startStamp = int(time.mktime(timeArray))
        timeArray = time.strptime(end, "%Y-%m-%d")
        endStamp = int(time.mktime(timeArray))
	#print endStamp-startStamp
	if endStamp-startStamp == 0:
		return 1
	else:
		return (endStamp-startStamp)/60/60/24 + 1

def storage(id,starttime,endtime,num,status,type):
	con=transtime(starttime,endtime)
	
        try:
                conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
                cur=conn.cursor()
		#continue = transtime(starttime,endtime)
                cur.execute('insert into TONGJI_FLOW(id,starttime,endtime,con,num,status,type) values(%s,%s,%s,%s,%s,%s,%s)',(id,starttime,endtime,con,num,status,type))
                        
                conn.commit()
                cur.close()
                conn.close()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
	dict=compute()
	#storage(dict)
