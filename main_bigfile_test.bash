#!/usr/bin/env bash 

if [ $# -ne 2 ] ;then
	echo "Usage: main_bigfile_test.bash  max_iterations version"
	exit 1
fi

MAXITERATIONS="$1"
VERSION="$2"
APPDIR="/local/src/Pycon2012ParallelConcurrent"
TESTSUITE="./bigfile_test.bash"
STOPSCALING="./stop_scaling_frequency.bash"

if [ ! -f $TESTSUITE ] ;then
	echo "$TESTSUITE does not exist."
	exit 1
fi

# The array contains the base names of the programs
# to test.  test_suite is called for each in the
# order of the array.
if [ "$VERSION" -eq 2 ] ;then 
	array=( bigfile_brute bigfile_brute_regex bigfile_pipeline \
		bigfile_pipeline_2 bigfile_coroutines bigfile_chunks_threads \
		bigfile_chunks_mp bigfile_chunks_futures_threadpool bigfile_chunks_gevent )

fi

if [ "$VERSION" -eq 3 ] ;then
    # These are the tests that specific to version 3
    # We need python 3 specific versions of these since
    # generators do not have a next attibute in release 3.
    # bigfile_pipeline_2 bigfile_pipeline_coroutines
    array=( bigfile_brute bigfile_brute_regex bigfile_pipeline \
		bigfile_pipeline_2 bigfile_coroutines bigfile_chunks_threads \
		bigfile_chunks_mp bigfile_chunks_futures_threadpool bigfile_chunks_gevent )
fi

# File for timings.
# program,python,real_secs,user_secs,system_secs,voluntarily_context_switches,involuntary_context_switches
TIMECAP="$APPDIR/time-cap"
if [ -f $TIMECAP ]
then
	rm $TIMECAP
else
	touch $TIMECAP
fi

# Execute
for item in ${array[*]}
do
	
	$TESTSUITE $item $MAXITERATIONS $APPDIR $TIMECAP $VERSION
done

# Rename timings file
ext=$(date +%Y-%m-%d-%H-%M-%S)
TIMECAPCSV="$TIMECAP-$ext.csv" 
mv $TIMECAP $TIMECAPCSV 
printf "Timing data in %s\n" "$TIMECAPCSV"
