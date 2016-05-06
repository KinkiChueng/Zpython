#!/usr/bin/env python
 
import sys
import time
import MySQLdb,codecs

list = []
t = time.time()

timeArray = time.localtime(t)
Style = time.strftime('%Y-%m-%d', timeArray)
print Style
otherStyle = time.strftime('%Y%m%d%H', timeArray)
useTime = int(otherStyle) - 1
getHour = time.strftime('%H', timeArray)
hour = int(getHour) - 1
readfile = open("/data/logs/"+Style+"/WRITEaccess_sta."+str(useTime), "rw")
#readfile = open("/data/logs/2015-12-03/WRITEaccess_sta.2015120323", "rw")
for line in readfile:
	uid = line.split('\t')[4]
	list.append(uid)
print len(list), len(set(list))

try:
	conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
	cur=conn.cursor()
	cur.execute('insert into TONGJI_RT_OVERALL values(%s,%s,%s)',(Style+' '+str(hour)+':00:00', len(list), len(set(list))))
	conn.commit()
	cur.close()
	conn.close()
except MySQLdb.Error,e:
	print "Mysql Error %d: %s" % (e.args[0], e.args[1])
