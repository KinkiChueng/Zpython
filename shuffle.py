#coding=utf-8
import urllib
import time,datetime,os

uri=''
referrer=''
strStart=''
uid=''
alllist=''
time_format=''
terminal=''
system=''
version=''
actualname=''
List=[]
systemdict = {'windows nt 5.1':'Windows_XP','windows nt 6.0':'Windows_VISTA','windows nt 6.1':'Windows_7','windows nt 6.2':'Windows_8','windows nt 6.3':'Windows_8','windows nt 10.0':'Windows_10'}
t = time.time()
day = time.strftime("%Y-%m-%d", time.localtime(t-60*60))
hm=time.strftime("%Y%m%d%H", time.localtime(t-60*60))
print('读取日志内容开始--------Start')
filename='/data/logs/%s'%day+'/access_sta.%s'%hm
print(filename)
if os.path.exists(filename): 
    fileHandler = open(filename, 'a+') #以读写方式处理文件IO
    fileHandler.seek(0)  #从文本内容头开始
    lines = fileHandler.readlines()
    print('读取日志内容结束--------End')
    print('逻辑处理开始--------Start')
    for line in lines:
        if "zd.html?actualname" in line:
            strlist=line.split(' - -') #以 - -分割字符串
            ip=strlist[0]  #IP地址
            #substr=urllib.unquote(strlist[1]).decode('utf-8', 'replace').encode('gbk', 'replace') #将文本转换编码格式，将中文显示正常
            substr=strlist[1]
            str1list=substr.split('&') #以&分割字符串
            #判断是PC端登录还是移动端-----Start
            if str1list[7].lower().find('mobile') >= 0:
                terminal='Mobile'
            else:
                terminal='PC'
            #判断是PC端登录还是移动端-----End
                
            #判断登录系统-----Start    
            if str1list[7].lower().find('windows') >= 0:
                system=str1list[7].lower()[str1list[7].lower().find('windows'):str1list[7].lower().find('windows')+15].replace(';','').replace(')','')
                if system in systemdict:
                   system=systemdict[system]
                else:
                   system='Windows_10'
            elif str1list[7].lower().find('android') >= 0:
                system='Android'
            elif str1list[7].lower().find('iphone') >= 0:
                system='iPhone'
 	    elif str1list[7].lower().find('mac') >= 0:
                system='Mac'
            else:
                system='#'
            #判断登录系统-----End
            #取出埋点函数中传的参数-----Start   
            for st in str1list:
                if st.find('version=') >= 0:
                    version=st[st.find('version=')+8:]
                if st.find('actualname=') >= 0:
                    actualname=st[st.find('actualname=')+11:]
                    actualname=urllib.unquote(actualname).decode('utf-8', 'replace').encode('gbk', 'replace')
                    if actualname=='undefined':actualname='other'                        
                if st.find('uri=') >= 0:
                    uri=st[st.find('uri=')+4:]
                if st.find('referrer=') >= 0:
                    referrer=st[9:]
                if st.find('strStart=') >= 0:
                    strStart=urllib.unquote(st[9:]).decode('utf-8', 'replace').encode('gbk', 'replace')#将文本转换编码格式，将中文显示正常
                    time_format = datetime.datetime.strptime(strStart, '%Y-%m-%d %H:%M:%S')#这里可以 print time_format 或者 直接 time_format 一下看看输出结果，默认存储为datetime格式
                    time_format = time_format.strftime('%Y%m%d%H%M%S')
                if st.find('uid=') >= 0:
                    uid=st[4:]
                    uid=urllib.unquote(uid).decode('utf-8', 'replace').encode('gbk', 'replace')
                    if uid.find('key=')>=0:uid=uid[4:]
            	    if uid.find('; JSESSIONID=')>=0:uid=uid[:uid.find('; JSESSIONID=')]
                #值为空的话赋值为'#'
                if uri=='':uri='#'
                if referrer=='':referrer='#'
                if time_format=='':time_format='#'
                if uid=='':uid='#'
                   
            #判断浏览器为IE的加上浏览器版本号   
            if actualname=='Microsoft Internet Explorer':
                actualname=actualname+'_'+version    
            alllist=ip+'\t'+uri+'\t'+referrer+'\t'+time_format+'\t'+uid+'\t'+terminal+'\t'+system+'\t'+actualname     #最终显示的每行样式数据
            List.append(urllib.unquote(alllist).decode('utf-8', 'replace').encode('gbk', 'replace'))# 循环完成的数据添加到数组  #将文本转换编码格式，将中文显示正常
            #取出埋点函数中传的参数-----End
    fileHandler.close()
    print('逻辑结束--------End')
    print('写入已处理日志内容开始--------Start')
    filewtname='/data/logs/%s'%day+'/WRITEaccess_sta.%s'%hm
    filewrite=file(filewtname,"w+")#将拼接好的字符串写入到指定文件中
    for i in List:#循环输入每行数据
        filewrite.write(i)
        filewrite.write("\n")
    filewrite.close()
    print('写入已处理内容结束--------End')
else: print('文件不存在')
