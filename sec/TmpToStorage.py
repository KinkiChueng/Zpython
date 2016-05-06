#!/usr/bin/env python

import os
import MySQLdb,codecs

def reader():
	route = "/root/Zpython/sec/a"
	readfile = open(route, "r")
	for line in readfile:
		storage(line)

def storage(line):
	try:
                conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
                cur=conn.cursor()
                cur.execute('insert into TONGJI_STILL_FLOW(id,starttime,type) values(%s,%s,%s)',(line.split("#")[0],line.split("#")[1],line.split("#")[5]))
                        
                conn.commit()
                cur.close()
                conn.close()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
	reader()
