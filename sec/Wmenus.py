#!/usr/bin/env python

import sys
from datetime import *
import datetime
import time
import os
import glob
import MySQLdb,codecs

def getDate():
	days = []
	days.append(datetime.datetime.fromtimestamp(time.time()-7*24*3600).strftime("%Y%m%d"))
	days.append(datetime.datetime.fromtimestamp(time.time()-6*24*3600).strftime("%Y%m%d"))
	days.append(datetime.datetime.fromtimestamp(time.time()-5*24*3600).strftime("%Y%m%d"))
	days.append(datetime.datetime.fromtimestamp(time.time()-4*24*3600).strftime("%Y%m%d"))
	days.append(datetime.datetime.fromtimestamp(time.time()-3*24*3600).strftime("%Y%m%d"))
	days.append(datetime.datetime.fromtimestamp(time.time()-2*24*3600).strftime("%Y%m%d"))
	days.append(datetime.datetime.fromtimestamp(time.time()-1*24*3600).strftime("%Y%m%d"))
	return days

def storage(days,dict):
        try:
                conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
                cur=conn.cursor()
                for menus in dict:
                        #cur.execute('insert into TONGJI_OS values(%s,%s,%s)',(yesterday, system, len(dict[system])))
                        print days[0], menus, len(dict[menus])
                        conn.commit()
                cur.close()
                conn.close()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def compute(week):
        dict = {}
        for today in week:
                route = "/data/logs/loginlog/"+ today +".log"
		print route
                readfile = open(route, "r")
                for line in readfile:
                        uid = line.split('\t')[1]
                        menus = line.split('\t')[4]
                        if dict.has_key(menus):
                                dict[menus].add(uid)
                        else:
                                dict.setdefault(menus,set())
                                dict[menus].add(uid)
        return dict

if __name__ == '__main__':
        week = getDate()
        #mon="201512"
        first = '/data/logs/loginlog/'
    #    print mon+'*.log'
   #     result=findfiles(first,mon+'*.log')
        dict=compute(week)
        storage(week,dict)
        print week
