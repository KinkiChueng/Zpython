#!/usr/bin/python
import MySQLdb,codecs,os
path='/data/logs/loginlog'
os.chdir(path)
file=open('denglu4.txt','r')
try:
    conn=MySQLdb.connect(host='localhost',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
    cur=conn.cursor()
    for line in file:
      lines=line.split('\t')
      cur.execute('insert into time_pv values(%s,%s,%s)',(lines[0],lines[1],int(lines[2])))
    conn.commit()
    cur.close()
    conn.close()
    file.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])

