#!/usr/bin/python
#coding:utf-8
import datetime,time
#告警合并
def mergeproblem(originallist):
    problemlist=[]
    normalist=[]
    Unknown=[]
    triggerkeylist=[]
    sorts=[]
    alarminfo=[]
    #告警or恢复
    for origina in originallist:

        if origina['triggervalue']=='1' :            
            problemlist.append(origina)
            if origina['triggerkey'] not in triggerkeylist:
                triggerkeylist.append(origina['triggerkey'])
        else :
            Unknown.append(origina)

    for triggerkey in triggerkeylist:
        for problem in problemlist:
            if problem['triggerkey']==triggerkey:
                sorts.append(problem)
        alarminfo.append(sorts)
        sorts=[]
    return alarminfo
#恢复合并
def mergenormal(originallist):
    normallist=[]
    Unknown=[]
    triggerkeylist=[]
    sorts=[]
    alarminfo=[]
    #告警or恢复
    for origina in originallist:

        if origina['triggervalue']=='0' :            
            normallist.append(origina)
            if origina['triggerkey'] not in triggerkeylist:
                triggerkeylist.append(origina['triggerkey'])
        else :
            Unknown.append(origina)

    for triggerkey in triggerkeylist:
        for normal in normallist:
            if normal['triggerkey']==triggerkey:
                sorts.append(normal)
        alarminfo.append(sorts)
        sorts=[]
    return alarminfo

#告警压缩
def compressproblem(alarminfo):
    currenttime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    messagelist=[]
    for info in alarminfo:
        hostlist=''
        hostgroup=''
        infonum=len(info)
        for host in info:
            triggername=host['triggername']
            hostinfo=host['hostname']+':'+host['ipaddress']+'\n'
            if host['hostgroup'] not in hostgroup:
                hostgroup+=host['hostgroup']+'\n'
            hostlist+=hostinfo
        if infonum >= 3 and infonum <= 6:        
            message='告警◕﹏◕\n'+'告警主机:'+str(infonum)+'台\n'+hostlist+'涉及主机组:\n'+hostgroup+'告警项目:\n'+triggername+'\n'+'分析时间:\n'+currenttime
            messagelist.append(message)
        elif infonum > 6:
            message='告警◕﹏◕\n'+'当前存在大量相同告警项,可能发生网络故障!\n详情请查看云警系统！\n'+'告警主机:'+str(infonum)+'台\n'+'告警项目:\n'+triggername+'\n'+'分析时间:\n'+currenttime
            messagelist.append(message)
    return messagelist


#恢复压缩
def compressnormal(alarminfo):
    currenttime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    messagelist=[]
    for info in alarminfo:
        hostlist=''
        hostgroup=''
        infonum=len(info)
        for host in info:
            triggername=host['triggername']
            hostinfo=host['hostname']+':'+host['ipaddress']+'\n'
            if host['hostgroup'] not in hostgroup:
                hostgroup+=host['hostgroup']+'\n'
            hostlist+=hostinfo
        if infonum >= 3 and infonum <= 6:        
            message='恢复◕‿◕\n'+'恢复主机:'+str(infonum)+'台\n'+hostlist+'涉及主机组:\n'+hostgroup+'恢复项目:\n'+triggername+'\n'+'分析时间:\n'+currenttime
            messagelist.append(message)
        elif infonum > 6:
            message='恢复◕‿◕\n'+'大量主机已经恢复!\n详情请查看监控系统！\n'+'恢复主机:'+str(infonum)+'台\n'+'恢复项目:\n'+triggername+'\n'+'分析时间:\n'+currenttime
            messagelist.append(message)
    return messagelist