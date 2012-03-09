#!/usr/bin/env bash 

# Collect system data in
# program,python,real_secs,user_secs,system_secs,voluntarily_context_switches,involuntary_context_switches
if [ $# -lt 2 ] ;then
	echo "Usage: $0  urlextentions iterations"
	exit 1
else
	urlextentions=$1
	iterations=$2
fi

. ./settings.bash

# File for timings.
timecap="$APPDIR/time-cap"
rmfile $timecap

# python3
prog="urlclient_futures_pool.py"
program="$APPDIR/$prog"

array[0]="t"
array[1]="p"
for type in  ${array[*]}
do
	for processes in {1..40} #these must be ints, not vars
	do
		CMD=" $PYTHON3 $program $type $urlextentions $iterations $processes"
		echo  $CMD
		echo -n $CMD >> $timecap
		/usr/bin/time --append --output=$timecap  -f "%e %U %S %w %c" $CMD
		echo ""
	done
	echo -n ""
done

# python2
 array2[0]=urlclient_gevent_pool.py
 for prog in ${array2[*]}
 do
	program="$APPDIR/$prog"
 	for processes in {1..40} #these must be ints, not vars
 	do
 		CMD=" $PYTHON2 $program $urlextentions $iterations $processes"
 		echo $CMD
 		echo -n $CMD >> $timecap
  		/usr/bin/time --append --output=$timecap  -f "%e %U %S %w %c" $CMD
       echo ""
 	done
	echo -n ""
 done

rentimef $timecap
printf "Timing data in %s\n" "$TIMECAPCSV"

