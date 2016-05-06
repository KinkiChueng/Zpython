#!/usr/bin/env python
 
import sys
import time
import MySQLdb,codecs

t = time.time()

timeArray = time.localtime(t)
Style = time.strftime('%Y-%m-%d', timeArray)
print Style
otherStyle = time.strftime('%Y%m%d%H', timeArray)
useTime = int(otherStyle) - 1
#readfile = open("/data/logs/"+Style+"/WRITEaccess_sta."+str(useTime), "rw")
for i in range(12,24):
	list=[]
	if i < 10:
		readfile = open("/data/logs/2015-12-"+sys.argv[1]+"/WRITEaccess_sta.201512"+sys.argv[1]+"0"+str(i), "rw")
	else:
		readfile = open("/data/logs/2015-12-"+sys.argv[1]+"/WRITEaccess_sta.201512"+sys.argv[1]+str(i), "rw")
	for line in readfile:
		uid = line.split('\t')[4]
		list.append(uid)
	print len(list), len(set(list))

	try:
		conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
		cur=conn.cursor()
		if i < 10:	
			cur.execute('insert into TONGJI_RT_OVERALL values(%s,%s,%s)',("2015-12-" + sys.argv[1] +" 0"+str(i)+":00:00", len(list), len(set(list))))
	 	else:
			cur.execute('insert into TONGJI_RT_OVERALL values(%s,%s,%s)',("2015-12-" + sys.argv[1] +" "+str(i)+":00:00", len(list), len(set(list))))
		conn.commit()
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
