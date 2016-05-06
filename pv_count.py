#!/usr/bin/python
import MySQLdb,codecs
import os,glob,re
file=open('pv_count.txt','w')
for str in range(3,6):
  if str<10:
    sr='0%d'%(str)
  else:
   sr='%d'%(str)
  path='/data/logs/2016-01-'+sr
  os.chdir(path)
  dic={}
  for fname in glob.glob('WRITEaccess_sta.2016*'):
    fs=open(fname,'r')
    for line in fs:
      lines=line.split('\t')
      if lines[3][6:8]==sr:
        keyuid='%s-%s-%s\t%s'%(lines[3][0:4],lines[3][4:6],lines[3][6:8],lines[4])
        if keyuid in dic:
          dic[keyuid].append(1)
        else:
          dic[keyuid]=[]
          dic[keyuid].append(1)
    fs.close()
  list1=[]
  for uid in dic:
     list1.append('%s\t%d'%(uid,len(dic[uid])))
  dic1={}
  for key in list1:
    time=key.split('\t')
    data='%s\t%s'%(time[0],time[2])
    if data in dic1:
        dic1[data].append(1)
    else:
        dic1[data]=[]
        dic1[data].append(1)
  for pv in dic1:
      file.write('%s\t%d\n'%(pv,len(dic1[pv])))
file.close() 
