#coding=utf-8
import os,MySQLdb,codecs
import time,datetime,urllib,json,glob

dictrefpv={}
dictrefuv={}
dictplatpv={}
dictplatuv={}
dictip={}
dictuv={}
sumpv=0
ref=''
platform=''
dic={}
a=set()
textlist=[]
t = time.time()
day = time.strftime("%Y-%m", time.localtime(t-60*60*24))
base_dir='/data/logs/'
#base_dir='C:/Users/hyl/Desktop/2015-12-03'
list = glob.glob(os.path.join(base_dir,day+'*/WRITE*.*'))
#统计入口来源信息（计算ref对应的uv）
def ref(textlist):
    for line in textlist:
            strlist=line.split('\t') #以\t分割字符串
            ref=strlist[2]
            time=strlist[3]
            uid=strlist[4]
            if ref=='#':
                ref='Direct'
            elif ref.find('syeinfo.tjsydl.com')>=0 or ref.find('sye-info')>=0:
                ref='InterSkip'
            else:
                ref='Navigation'
            if ref in dictrefuv:
                dictrefuv[ref].add(uid)
            else:
                dictrefuv.setdefault(ref,set())
                dictrefuv[ref].add(uid)   
            if ref in dictrefpv:
                sumpv=dictrefpv[ref]
            else:
                sumpv=0
            sumpv=sumpv+1
            dictrefpv[ref]=sumpv
    for ref in dictrefuv:
        #循环插入数据库对应表中
         cur.execute('insert into TONGJI_REF(date,ref,uv,pv) values(%s,%s,%s,%s)',(day,ref,len(dictrefuv[ref]),dictrefpv[ref]))
         #print day,ref,len(dictrefuv[ref]),dictrefpv[ref]
#按平台统计uv（移动和pc）
def platf(textlist):
    for line in textlist:
            strlist=line.split('\t') #以\t分割字符串
            time=strlist[3]
            uid=strlist[4]
            platform=strlist[5]
            if platform in dictplatuv:
                dictplatuv[platform].add(uid)
            else:
                dictplatuv.setdefault(platform,set())
                dictplatuv[platform].add(uid)   
            if platform in dictplatpv:
                sumpv=dictplatpv[platform]
            else:
                sumpv=0
            sumpv=sumpv+1
            dictplatpv[platform]=sumpv
    for platform in dictplatuv:
        #循环插入数据库对应表中
         cur.execute('insert into TONGJI_TERMINAL(date,terminal,uv) values(%s,%s,%s)',(day,platform,len(dictplatuv[platform])))
         #print day,platform,len(dictplatuv[platform]),dictplatpv[platform]
#分地域计算uv      
def iparea(textlist):
    for line in textlist:
        strlist=line.split('\t') #以\t分割字符串
        ip=strlist[0]
        a.add(ip)#把IP放入SET集合中去重，以便减少访问ip接口次数，提高效率
    for ip in a:
        htmlCode = urllib.urlopen('http://ip.taobao.com/service/getIpInfo.php?ip='+ip).read()
        dic=json.loads(htmlCode, "utf-8")
        dictip[ip]=dic['data']['region']#把ip对应的城市写入字典
    for line in textlist:
        strlist=line.split('\t') #以\t分割字符串
        time=strlist[3]
        uid=strlist[4]
        ip=strlist[0]
        if dictip[ip] in dictuv:
            dictuv[dictip[ip]].add(uid)
        else:
            dictuv.setdefault(dictip[ip],set())
            dictuv[dictip[ip]].add(uid)
    for dictip[ip] in dictuv:
        #循环插入数据库对应表中
        cur.execute('insert into TONGJI_AREA(date,area,uv) values(%s,%s,%s)',(day,dictip[ip],len(dictuv[dictip[ip]])))        
       # print day,dictip[ip],len(dictuv[dictip[ip]])    
try:
        conn=MySQLdb.connect(host='101.201.149.190',user='sysinfo',passwd='123456',db='sysdb',port=3306,charset='utf8')
        cur=conn.cursor()
        for i in range(0, len(list)):
            filename=list[i]
            if os.path.exists(filename):
                fileHandler = open(filename, 'a+') #以读写方式处理文件IO
                fileHandler.seek(0)  #从文本内容头开始
                lines = fileHandler.readlines()
            textlist =lines+textlist
        ref(textlist)
        platf(textlist)
        iparea(textlist)
                    #    print ('------------PV-------------')
         #   for ref in dictpv:
         #       print ref,dictpv[ref]
         #       cur.execute('insert into TONGJI_REF(date,ref,pv) values(%s,%s,%s)',(time,ref,dictpv[ref]))
        conn.commit() 
        cur.close()
        conn.close()
except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
