#!/bin/bash
echo "10152 65535" > /proc/sys/net/ipv4/ip_local_port_range
sysctl -w fs.file-max=128000
sysctl -w net.ipv4.tcp_keepalive_time=300
sysctl -w net.core.somaxconn=250000
sysctl -w net.ipv4.tcp_max_syn_backlog=2500
sysctl -w net.core.netdev_max_backlog=2500
ulimit -n 10240