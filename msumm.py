#!/usr/bin/env python
# coding=utf-8

import sys
from datetime import *
import datetime
import time
import os
import glob
import MySQLdb,codecs

def computeByBrowser(result):
        dict = {}
        for dir in result:
                routetmp = "/data/logs/"+dir
		print routetmp
		result2=findfiles(routetmp,'WRITEaccess_sta.*')
		for filename in result2:
			route = "/data/logs/" + dir + "/" + filename
                	print route
			readfile = open(route, "r")
        	        for line in readfile:
                	        uid = line.split('\t')[4]
                        	browser = line.split('\t')[7].strip()
				dict.setdefault("Others",set())
        	                if browser=="Chrome" or browser=="Firefox" or browser=="Microsoft Internet Explorer_10.0" or browser=="Microsoft Internet Explorer_9.0" or browser=="Microsoft Internet Explorer_8.0" or browser=="Safari":
					if dict.has_key(browser):
                        	        	dict[browser].add(uid)
					else:
						dict.setdefault(browser,set())
						dict[browser].add(uid)
        	                else:
                	                dict["Others"].add(uid)
        return dict
        for browser in dict:
               length = len(dict[browser])
       #       storage(yesterday,browser,length)
               print browser,len(dict[browser]),len(set(dict[browser]))

def transfer():
        trans = {};
        route = "/root/Zpython/menusTranChinese.txt"
        readfile = open(route, "r")
        for line in readfile:
                type = line.split()[1]
		if (type == "首页")==False:
                	uri = line.split()[0]
			trans.setdefault(uri, "")
                	trans[uri]=type
	return trans
	

def computeByPage(trans,result):
        dict = {}
	for dir in result:
	        routetmp = "/data/logs/"+dir
        	result2=findfiles(routetmp,'WRITEaccess_sta.*')
	        for filename in result2:
        	        route = "/data/logs/" + dir + "/" + filename
                	print route
	                readfile = open(route, "r")
        	        for line in readfile:
                	        uid = line.split()[4]
                        	uri = line.split()[1]
				print uri
				if uri == "http://sye-info.com/" or uri == "http://syeinfo.tjsydl.com/index.html" or uri == "http://syeinfo.tjsydl.com/" or uri == "http://www.sye-info.com/" or uri == "http://syeinfo.tjsydl.com/#" or uri == "http://www.sye-info.com/index.html#" or uri == "http://www.sye-info.com/index.html":
					furi = "首页"
				else:
					for tmp in trans:
						if tmp.lower() in uri.lower():
							furi = trans[tmp]
						else:
							pass
                	        if furi in dict:
                        	        dict[furi].append(uid)
                	        else:
					dict.setdefault(furi, list())
                                	dict[furi].append(uid)
	return dict

def computeBySystem(result):
        dict = {}
	for dir in result:
                routetmp = "/data/logs/"+dir
                result2=findfiles(routetmp,'WRITEaccess_sta.*')
                for filename in result2:
                        route = "/data/logs/" + dir + "/" + filename
                        print route
                        readfile = open(route, "r")
                        for line in readfile:
                        	uid = line.split('\t')[4]
                        	system = line.split('\t')[6]
	                        if dict.has_key(system):
        	                        dict[system].add(uid)
                	        else:
                        	        dict.setdefault(system,set())
                                	dict[system].add(uid)
        return dict

def computeByAll(result):
        list=[]
	for dir in result:
                routetmp = "/data/logs/"+dir
                result2=findfiles(routetmp,'WRITEaccess_sta.*')
                for filename in result2:
                        route = "/data/logs/" + dir + "/" + filename
                        readfile = open(route, "r")
                        for line in readfile:
                        	uid = line.split('\t')[4]
	                        list.append(uid)
	print len(list), len(set(list))
        return list

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



def getDate():
        #yesterday = date.today() + datetime.timedelta(-1)
        #return sys.argv[1]
	#return "2015-12-02"
	year = int(time.strftime('%Y',time.localtime(time.time())))
	mon = int(time.strftime('%m',time.localtime(time.time())))-1
        if mon==0:
		year = int(time.strftime('%Y',time.localtime(time.time())))-1
                mon=str(year)+'-12'
	else:
		mon=str(year)+'-'+str(mon)
        return mon
        #return sys.argv[1]

def storage(mon,dict,table):
        try:
                conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
                cur=conn.cursor()
		if table == "TONGJI_DOC":
			for type in dict:
				i = len(dict[type])
	                        s = set(dict[type])
        	                cur.execute('insert into TONGJI_DOC(date,type,pv,uv) values(%s,%s,%s,%s)',(mon, type, i, len(s)))
				print type, i, len(s)
                        	conn.commit()
		elif table == "TONGJI_BROWSER":
			for browser in dict:
                        	cur.execute('insert into TONGJI_BROWSER(date,browser,uv) values(%s,%s,%s)',(mon, browser.strip(), len(dict[browser])))
                        	print mon, browser, len(dict[browser])
                        	conn.commit()
		elif table == "TONGJI_OS":
			for system in dict:
                        	cur.execute('insert into TONGJI_OS(date,os,uv) values(%s,%s,%s)',(mon, system, len(dict[system])))
                        	print mon, system, len(dict[system])
                        	conn.commit()	
		elif table == "TONGJI_OVERALL":
                        cur.execute('insert into TONGJI_OVERALL(date,pv,uv) values(%s,%s,%s)',(mon, len(listA), len(set(listA))))
                        print mon, len(listA), len(set(listA))
                cur.close()
                conn.close()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
        mon = str(getDate())
        first = '/data/logs/'
	#print mon
	result = findfiles(first,mon+'*')
	print result
        #result=findfiles(first,'WRITEaccess_sta.*')

        dictB=computeByBrowser(result)
	storage(mon,dictB,'TONGJI_BROWSER')
	print "aaa"

	trans=transfer()
	dictP=computeByPage(trans,result)
	storage(mon,dictP,'TONGJI_DOC')
	print "bbb"

	dictS=computeBySystem(result)
        storage(mon,dictS,'TONGJI_OS')
	print "CCC"

	listA=computeByAll(result)
        storage(mon,listA,'TONGJI_OVERALL')
	print "ddd"
