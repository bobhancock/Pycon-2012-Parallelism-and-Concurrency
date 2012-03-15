#!/usr/bin/env bash 

x=$(netstat -antp|grep 2020| wc -l) >/dev/null 2>&1
echo $x
while true
do
	sleep 10
	x=$(netstat -antp|grep 2020| wc -l) >/dev/null 2>&1
	echo $x
done