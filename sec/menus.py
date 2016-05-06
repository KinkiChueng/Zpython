#!/usr/bin/env python

import sys
from datetime import *
import time
import os
import glob
import MySQLdb,codecs

def getDate():
	useTime = time.strftime('%Y%m%d',time.localtime(time.time() - 24*60*60))
	#return useTime
	return sys.argv[1]

def storage(yesterday,dict):
        try:
                conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
                cur=conn.cursor()
                for menus in dict:
                        cur.execute('insert into TONGJI_MENUS(date,type,uv) values(%s,%s,%s)',(yesterday, menus, len(dict[menus])))
                        print yesterday, menus, len(dict[menus])
                        conn.commit()
                cur.close()
                conn.close()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def compute():
        dict = {}
        route = "/data/logs/loginlog/"+str(yesterday)+".log"
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
	for menus in dict:
		print menus,len(dict[menus]),dict[menus]
        return dict

if __name__ == '__main__':
        yesterday = str(getDate())
        #file = '/data/logs/'+yesterday
        dict = compute()
        storage(yesterday,dict)
