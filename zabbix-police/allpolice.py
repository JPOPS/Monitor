#!/usr/bin/env python
#coding:utf-8
import MySQLdb
import redis
import sys
from dbread import *
from operation import *
from weixin import *
import datetime,time
sendtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
accesstoken = gettoken()
#发送微信给运维人员
users=['*****']
#在zabbix 可以找到告警收敛的动作ID（actionid）
actionid=*****
#连接redis，并读取所有事件id
r = redis.StrictRedis(host='*****', port=6379)


subjectlist=r.keys()
for i in subjectlist:
    r.delete(i)
#r.flushdb()
#获取原始数据并存入数据库
originallist=[]
for subject in subjectlist:
        a=alerts_eventid(str(actionid),subject)
        originallist.append(a)
problem=mergeproblem(originallist)
normal=mergenormal(originallist)
#发送告警信息
messagelist=compressproblem(problem)
if len(messagelist) != 0:
    for content in  messagelist:
        print sendtime
        for user in users:
            senddata(accesstoken,user,content)
#发送恢复信息    
messagelist=compressnormal(normal)
if len(messagelist) != 0:
    for content in  messagelist:
        print sendtime
        for user in users:
            senddata(accesstoken,user,content)