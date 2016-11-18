#!/usr/bin/env python
import urllib2
import sys
import json
import argparse

#定义通过HTTP方式访问API地址的函数，后面每次请求API的各个方法都会调用这个函数
def requestJson(url,values):        
    data = json.dumps(values)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json-rpc'})
    response = urllib2.urlopen(req, data)
    output = json.loads(response.read())
#    print output
    try:
        message = output['result']
    except:
        message = output['error']['data']
        print message
        quit()

    return output['result']

#API接口认证的函数，登录成功会返回一个Token
def authenticate(url, username, password):
    values = {'jsonrpc': '2.0',
              'method': 'user.login',
              'params': {
                  'user': username,
                  'password': password
              },
              'id': '0'
              }
    idvalue = requestJson(url,values)
    return idvalue

#定义更加主机分组名称获取各个hostid的函数
def getHosts(groupname,url,auth):
    host_list = []
    values = {'jsonrpc': '2.0',
              'method': 'hostgroup.get',
              'params': {
                  'output': 'extend',
                  'filter': {
                      'name': groupname
                  },

                  'selectHosts' : ['hostid','host'],
              },
              'auth': auth,
              'id': '2'
              }
    output = requestJson(url,values)
    for host in output[0]['hosts']:
        host_list.append(host['hostid'])
    return host_list

#定义获取graphid的函数
def getGraphs(host_list,name_list, url, auth, columns, graphtype=0 ,dynamic=0):
    if (graphtype == 0):
       selecttype = ['graphid']
       select = 'selectGraphs'
    if (graphtype == 1):
       selecttype = ['itemid', 'value_type']
       select = 'selectItems'
    values=({'jsonrpc' : '2.0',
             'method' : 'graph.get',
             'params' : {
                  'output' : ['graphid','name'],
                  select : [selecttype,'name'],
                  'hostids' : host_list,
                  'sortfield' : 'name',
                  'filter' : {
                         'name' : name_list,

                             },
                        },
             'auth' : auth,
             'id' : 3
              })
    output = requestJson(url,values)
    bb = sorted(output,key = lambda x:x['graphid'])
    graphs = []
    if (graphtype == 0):
        for i in bb:
            print i
            graphs.append(i['graphid'])
    if (graphtype == 1):
        for i in bb:
            if int(i['value_type']) in (0, 3):
               graphs.append(i['itemid'])

    graph_list = []
    x = 0
    y = 0
    for graph in graphs:
        print "x is " + str(x)
        print "y is " + str(y)
        graph_list.append({
            "resourcetype": graphtype,
            "resourceid": graph,
            "width": "500",
            "height": "100",
            "x": str(x),
            "y": str(y),
            "colspan": "1",
            "rowspan": "1",
            "elements": "0",
            "valign": "0",
            "halign": "0",
            "style": "0",
            "url": "",
            "dynamic": str(dynamic)
        })
        x += 1
#        print type(x)
#        print type(columns)
        if x == int(columns):
            x = 0
            y += 1
#    print graph_list
    return graph_list

#定义创建screen的函数
def screenCreate(url, auth, screen_name, graphids, columns):
    columns = int(columns)
    if len(graphids) % columns == 0:
        vsize = len(graphids) / columns
    else:
        vsize = (len(graphids) / columns) + 1

#先使用screen.get判断给定的screen name是否存在
    values0 = {
               "jsonrpc" : "2.0",
               "method"  : "screen.get",
               "params"  : {
                   "output" : "extend",
                   "filter" : {
                       "name" : screen_name,
                              }
                           },
               "auth" : auth,
               "id" : 2
               }
    values = {
              "jsonrpc": "2.0",
              "method": "screen.create",
              "params": {
                  "name": screen_name,
                  "hsize": columns,
                  "vsize": vsize,
                  "screenitems": []
              },
              "auth": auth,
              "id": 2
              }
    output0 = requestJson(url,values0)
    print output0

#如果给定的screen name不存在则直接创建screen 
    if output0 == []:
       print "The Given Screen Name Not Exists"
       print "Creating Screen %s" %screen_name
       for i in graphids:
          values['params']['screenitems'].append(i)
       output = requestJson(url,values)
    else:


#如果给定的screen name已经存在，直接创建screen是不行的，
#要么先使用screen.delete把原来的screen删除掉，然后再创建，
#要么直接使用screen.update更新原来那个screen，
#使用screen.delete会产生新的screenid,
#使用screen.update比较合理一点。
       print "The Given Screen Name Already Exists"
       update_screenid=output0[0]["screenid"]
       print update_screenid
       print "Updating Screen Name %s  Screen ID %s" %(screen_name,update_screenid)
       values1 = {
               "jsonrpc" : "2.0",
               "method"  : "screen.update",
               "params"  : {
                       "screenid" : update_screenid,
                       "screenitems": []
                           },
               "auth"    : auth,
               "id"      : 2
                 }
       output1 = requestJson(url,values1)
       print output1
       print "Updating  Screen Name %s" %screen_name
       for i in graphids:
          values1['params']['screenitems'].append(i)
       output = requestJson(url,values1)

def main():
    url = 'http://zabbixip/zabbix/api_jsonrpc.php'
    username = '****'
    password = '****'
    auth = authenticate(url, username, password)
    host_list = getHosts(groupname,url,auth)
    print host_list
    graph_ids = getGraphs(host_list,graphname, url, auth, columns)
    screenCreate(url, auth, screenname, graph_ids, columns)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Zabbix screen from all of a host Items or Graphs.')
    parser.add_argument('-G', dest='graphname', nargs='+',metavar=('grah name'),
                        help='Zabbix Host Graph to create screen from')
    parser.add_argument('-H', dest='hostname', nargs='+',metavar=('10.19.111.145'),
                        help='Zabbix Host to create screen from')
    parser.add_argument('-g', dest='groupname', nargs='+',metavar=('linux server'),
                        help='Zabbix Group to create screen from')
    parser.add_argument('-n', dest='screenname', type=str,
                        help='Screen name in Zabbix.  Put quotes around it if you want spaces in the name.')
    parser.add_argument('-c', dest='columns', type=int,
                        help='number of columns in the screen')
    args = parser.parse_args()
    print args
    hostname = args.hostname
    groupname = args.groupname
    screenname = args.screenname
    columns = args.columns
    graphname = args.graphname
    if columns is None:
        columns = len(graphname)
#    print columns
    main()