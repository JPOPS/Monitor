#!/bin/bash
#iptables 监控脚本
#2017-03-30
function tcp {
sudo iptstate --single | grep tcp | wc -l
}
function tcp-syn {
sudo iptstate --single | grep SYN | wc -l
}
function tcp-timewait {
sudo iptstate --single | grep TIME_WAIT | wc -l
}
function tcp-established {
sudo iptstate --single | grep ESTABLISHED | wc -l 
}
function tcp-close {
sudo iptstate --single | grep CLOSE | wc -l
}
function udp {
sudo iptstate --single | grep udp | wc -l
}
function icmp {
sudo iptstate --single | grep icmp | wc -l
}
function all {
sudo iptstate --single | wc -l
}
$1
