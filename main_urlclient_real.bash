#!/usr/bin/env bash 

# Collect only the real time of execution and
# place in record: processes, real1,real2,real3
if [ $# -lt 2 ] ;then
	echo "Usage: $0  urlextentions iterations"
	exit 1
else
	urlextentions=$1
	iterations=$2
fi

. ./settings.bash

 prog="urlclient_futures_pool.py"
 program="$APPDIR/$prog"

# python3
# # python3 threads only, MP pool  hangs
array[0]="t"
for type in  ${array[*]}
do
	for processes in {1..40} #these must be ints, not vars
	do
		CMD="$PYTHON3 $program $type $urlextentions $processes $iterations"
		#echo  $CMD
		$CMD
	done
	echo -n ""
done

# python 2 threads and processes
# under python3 it hangs
array[0]="t"
#array[1]="p"
for type in  ${array[*]}
do
	for processes in {1..40} #these must be ints, not vars
	do
		CMD="$PYTHON2 $program $type $urlextentions $processes $iterations"
#		echo  $CMD
		$CMD
	done
	echo -n ""
done



# gevent
# # python2
 array2[0]=urlclient_gevent_pool.py
 for prog in ${array2[*]}
 do
	program="$APPDIR/$prog"
 	for processes in {1..40} #these must be ints, not vars
 	do
 		CMD=" $PYTHON2 $program $urlextentions $processes $iterations"
 		#echo $CMD
        $CMD
 	done
	echo -n ""
 done


