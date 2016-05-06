#coding=utf-8
import time,os,datetime,MySQLdb

dictuv={}
dictperpv={}
dictprouv={}
dictdepuv={}
sumpv=0
sumuv=0
a=set()
t = time.time()
day = time.strftime("%Y%m%d", time.localtime(t-60*60*24))
dayt = time.strftime("%Y-%m-%d", time.localtime(t-60*60*24))
filename='/data/logs/loginlog/%s'%day+'.log'
#filename='C:/Users/hyl/Desktop/20151207.log'
print filename
#每条公告栏访问的uv
def gonggao(lines):

    for line in lines:
        strlist=line.split('\t') #以\t分割字符串
        uid=strlist[1]
        operation=strlist[4]
        title=strlist[5].strip()
        #print uid,operation,title
        if operation=='gonggao':
            if title in dictuv:
                dictuv[title].add(uid)
            else:
                dictuv.setdefault(title,set())
                dictuv[title].add(uid)                 
    for title in dictuv:           
        #print day,title,len(dictuv[title])
        cur.execute('insert into TONGJI_Inner_NOTICE(date,title,uv) values(%s,%s,%s)',(dayt,title,len(dictuv[title])))
#内网总访问的pv、uv
def allvisit(lines):
    global sumpv
    for line in lines:
        strlist=line.split('\t') #以\t分割字符串
        uid=strlist[1]
        #print uid,operation,title
        a.add(uid)
        sumpv=sumpv+1 
    cur.execute('insert into TONGJI_Inner_VISIT(date,uv,pv) values(%s,%s,%s)',(dayt,len(a),sumpv))
#每个人访问的次数uv
def pervisit(lines):
    for line in lines:
        strlist=line.split('\t') #以\t分割字符串
        uid=strlist[1]
        if uid in dictperpv:
            dictperpv[uid].append(uid)
        else:
            dictperpv.setdefault(uid,[])
            dictperpv[uid].append(uid)
    for uid in dictperpv:  
        cur.execute('insert into TONGJI_Inner_PERVISIT_COUNT(date,uid,pv) values(%s,%s,%s)',(dayt,uid,len(dictperpv[uid])))
#)各项目、各部门的uv占比
def project(lines):
    for line in lines:
        strlist=line.split('\t') #以\t分割字符串
        uid=strlist[1]
        department=strlist[2]
        project=strlist[3]
        if project.find('#')>=1:
            slist=project.split('#')
            for i in range(0, len(slist)):
                project=slist[i]
                if project in dictprouv:
                    dictprouv[project].add(uid)
                else:
                    dictprouv.setdefault(project,set())
                    dictprouv[project].add(uid)
        if department in dictdepuv:
            dictdepuv[department].add(uid)
        else:
            dictdepuv.setdefault(department,set())
            dictdepuv[department].add(uid)
        if project in dictprouv:
            dictprouv[project].add(uid)
        else:
            dictprouv.setdefault(project,set())
            dictprouv[project].add(uid)    
    for department in dictdepuv:
        cur.execute('insert into TONGJI_Inner_PROJECT(date,name,uv,flag) values(%s,%s,%s,%s)',(dayt,department,len(dictdepuv[department]),'BM'))
    for project in dictprouv:
       #print dayt,project,len(dictprouv[project]),'XM'
        cur.execute('insert into TONGJI_Inner_PROJECT(date,name,uv,flag) values(%s,%s,%s,%s)',(dayt,project,len(dictprouv[project]),'XM'))
      
try:
        conn=MySQLdb.connect(host='101.201.149.190',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
        cur=conn.cursor()
        if os.path.exists(filename):
            fileHandler = open(filename, 'a+') #以读写方式处理文件IO
            fileHandler.seek(0)  #从文本内容头开始
            lines = fileHandler.readlines()
            print('读取日志内容结束--------End')
            print('逻辑处理开始--------Start')
            gonggao(lines)
            allvisit(lines)
            pervisit(lines)
            project(lines)
        conn.commit() 
        cur.close()
        conn.close()
        print('逻辑结束--------End')
        print('写入已处理日志内容开始--------Start')
except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
