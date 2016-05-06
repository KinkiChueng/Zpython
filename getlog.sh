#!/bin/sh
log_home=/data/logs/loginlog
timeDate=`date +%Y%m%d -d  '-1 hours'`
wget -O /data/logs/loginlog/$timeDate.log http://61.136.58.235:6000/$timeDate.log

