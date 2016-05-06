#coding=utf-8
import urllib2,MySQLdb,time
timenow = time.localtime()
datenow = time.strftime('%Y-%m-%d %H:%M', timenow)
def portTest():
        try:
                response = urllib2.urlopen('http://syeinfo.tjsydl.com/Login.jsp', timeout=10)
                cur.execute('insert into TONGJI_Inner_HEALTH(date,flag) values(%s,%s)',(datenow,'连接成功'))
                cur.execute('select success from  TONGJI_Inner_HEALTHCOUNT where keyid=1')
                scount = cur.fetchone()
                cur.execute('update TONGJI_Inner_HEALTHCOUNT set success=%s where keyid=1',(scount[0]+1))
		
        except:
                cur.execute('insert into TONGJI_Inner_HEALTH(date,flag) values(%s,%s)',(datenow,'连接失败'))
                cur.execute('select fail from  TONGJI_Inner_HEALTHCOUNT where keyid=1')
                fcount=cur.fetchone()
                cur.execute('update TONGJI_Inner_HEALTHCOUNT set fail=%s where keyid=1',(fcount[0]+1))
if __name__ == "__main__":
        try:
            conn=MySQLdb.connect(host='101.201.149.190',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
            cur=conn.cursor()
            portTest()
            conn.commit() 
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
             print "Mysql Error %d: %s" % (e.args[0], e.args[1])
