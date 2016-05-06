#!/usr/bin/env python
# coding=utf-8

from datetime import *
import sys
import datetime
import os
import glob
import MySQLdb,codecs

def computeByBrowser(result):
        dict = {}
        for filename in result:
                route = "/data/logs/"+str(yesterday)+ "/" + filename
                readfile = open(route, "r")
                for line in readfile:
                        uid = line.split('\t')[4]
                        browser = line.split('\t')[7].strip()
			dict.setdefault("others",set())
                        if browser=="Chrome" or browser=="Firefox" or browser=="Microsoft Internet Explorer_10.0" or browser=="Microsoft Internet Explorer_9.0" or browser=="Microsoft Internet Explorer_8.0" or browser=="Safari":
				if dict.has_key(browser):
                                	dict[browser].add(uid)
				else:
					dict.setdefault(browser,set())
                                        dict[browser].add(uid)
                        else:	
				dict["others"].add(uid)
		readfile.close()
        return dict
        #for browser in dict:
        #       storage(yesterday,browser,length)
        #       print browser,length

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
        for filename in result:
                route = "/data/logs/"+str(yesterday)+ "/" + filename
                readfile = open(route, "r")
                for line in readfile:
                        uid = line.split()[4]
                        uri = line.split()[1]
                        if uri == "http://sye-info.com/" or uri == "http://syeinfo.tjsydl.com/index.html" or uri == "http://syeinfo.tjsydl.com/" or uri == "http://www.sye-info.com/" or uri == "http://syeinfo.tjsydl.com/#" or uri == "http://www.sye-info.com/index.html#" or uri == "http://www.sye-info.com/index.html":
                                furi = "首页"
                        else:
                                for tmp in trans:
					if tmp.lower() in uri.lower():
                                                furi = trans[tmp]
                                        else:
                                                pass
                        if furi in dict:
                                print furi
                                dict[furi].append(uid)
                        else:
                                dict.setdefault(furi, list())
                                dict[furi].append(uid)
        return dict

def computeBySystem(result):
        dict = {}
        for filename in result:
                route = "/data/logs/"+str(yesterday)+ "/" + filename
                readfile = open(route, "r")
                for line in readfile:
                        uid = line.split('\t')[4]
                        system = line.split('\t')[6]
                        if dict.has_key(system):
                                dict[system].add(uid)
                        else:
                                dict.setdefault(system,set())
                                dict[system].add(uid)
		readfile.close()
        return dict

def computeByAll(result):
	list=[]
	for filename in result:
		route = "/data/logs/"+str(yesterday)+ "/" + filename
                readfile = open(route, "r")
		for line in readfile:
			uid = line.split('\t')[4]
        		list.append(uid)
		readfile.close()
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
        yesterday = date.today() + datetime.timedelta(-1)
        return yesterday
	#return sys.argv[1]

def storage(yesterday,dict,table):
        try:
                conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
                cur=conn.cursor()
		if table == "TONGJI_DOC":
                        for type in dict:
                                i = len(dict[type])
                                s = set(dict[type])
                                cur.execute('insert into TONGJI_DOC(date,type,pv,uv) values(%s,%s,%s,%s)',(yesterday, type, i, len(s)))
                                print type, i, len(s)
                                conn.commit()                       	
		elif table == "TONGJI_BROWSER":
			for browser in dict:
                        	cur.execute('insert into TONGJI_BROWSER(date,browser,uv) values(%s,%s,%s)',(yesterday, browser, len(dict[browser])))
                        	print yesterday, browser, len(dict[browser])
                        	conn.commit()
		elif table == "TONGJI_OS":
			for system in dict:
                        	cur.execute('insert into TONGJI_OS(date,os,uv) values(%s,%s,%s)',(yesterday, system, len(dict[system])))
                        	print yesterday, system, len(dict[system])
                        	conn.commit()
		elif table == "TONGJI_OVERALL":
			cur.execute('insert into TONGJI_OVERALL(date,pv,uv) values(%s,%s,%s)',(yesterday, len(listA), len(set(listA))))
                        print yesterday, len(listA), len(set(listA))
	
                cur.close()
                conn.close()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
        yesterday = str(getDate())
        first = '/data/logs/'+yesterday
        result=findfiles(first,'WRITEaccess_sta.*')

        dictB=computeByBrowser(result)
	storage(yesterday,dictB,'TONGJI_BROWSER')

	trans=transfer()
	dictP=computeByPage(trans,result)
	storage(yesterday,dictP,'TONGJI_DOC')

	dictS=computeBySystem(result)
        storage(yesterday,dictS,'TONGJI_OS')
	
	listA=computeByAll(result)
	storage(yesterday,listA,'TONGJI_OVERALL')
