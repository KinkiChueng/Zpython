#!/bin/sh
log_home=/data/logs
timeDate=`date +%Y-%m-%d -d  '-1 hours'`
timeHour=`date +%Y%m%d%H -d  '-1 hours'`
echo $timeHour
timeHour=`date +%Y%m%d%H`
cd $log_home
file="/data/logs/$timeDate"
if [ -d "$file" ];then
echo "OK"
else
mkdir /data/logs/$timeDate
fi
timeHour2=`date +%Y%m%d%H -d  '-1 hours'`
mv /data/logs/access.log $file/access_sta.$timeHour2
echo $timeHour2
/usr/local/nginx/sbin/nginx -s reload
