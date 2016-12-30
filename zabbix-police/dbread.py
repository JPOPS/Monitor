#!/usr/bin/python
#coding:utf-8
#脚本中*****需要修改的地方
import MySQLdb
import datetime,time
import sys
#定义通过actionid和subject获取数据库告警具体信息，并以字典形式返回
def alerts_eventid(actionid,subject):
        try:
                conn=MySQLdb.connect(host='*****',user=*****',passwd='******',db='*****',port=3306)
                #host：zabbix数据库ip
                #user：zabbix数据库用户
                #passwd：zabbix数据库密码
                #db：zabbix数据库名称
                cursor = conn.cursor()
                cursor.execute("SET NAMES utf8");
                sql = "SELECT * FROM alerts where actionid = '%s' and subject = '%s' ;" % (actionid,subject)
                cursor.execute(sql)
                data = cursor.fetchall()
                cursor.close()
                conn.close()
                event=data[0]
                messagelist=[]
                message=event[8]
                messageone=message.split('#')
                for i in messageone:
                        messagelist.append(i.split('|'))
                print messagelist
                messagedict=dict(messagelist)
                return messagedict
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])