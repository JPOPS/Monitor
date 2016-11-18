#!/usr/bin/python
#磁盘只读检测脚本正常0，异常1
#jipeng 2016/3/26
import time
try:
    fileDisk = open ( '/usr/local/zabbix/scripts/disk_health_check.log', 'w' )
    old = str(time.time())
    fileDisk.write(old)
    fileDisk = open ( '/usr/local/zabbix/scripts/disk_health_check.log' )
    new=fileDisk.read()
    if (old==new):
        print '0'
    else:
        print '1'
    fileDisk.close()
except:
    print '1'