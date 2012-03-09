#!/usr/bin/env bash 

# Run programs n times a piece and capture the UNIX time output
# to a time.cap file.  Each record is comma separated so should
# easily import into a spreadsheet.
# Format of time.cap record: program,real time,user secs,system secs,num time was voluntarily context switched,involuntary context switches

if [ $# -lt 5 ] ; then
	echo "Usage: $0 program_name max_iterations application_dir time_cap_file"
	exit 1
fi
prog=$1
MAXITERATIONS=$2
appdir=$3
timecap=$4
VERSION=$5

SETTINGS="$appdir/settings.py"
pythonbasedir="/usr/local"
py27="python"
pypy="$pythonbasedir/pypy/bin/pypy"
py32="$pythonbasedir/python322/bin/python3"
stackless="$pythonbasedir/stackless272/bin/python"

# run python versions
pyrun()
{
PYTHON=$1
PROG=$2
maxiterations=$3
iteration=1
while [ "$iteration" -le "$maxiterations" ]
do
    echo  "$PYTHON $PROG $iteration of $maxiterations"
	echo -n "$PROG,$PYTHON," >> $timecap
	CMD=" $PYTHON $PROG"
    /usr/bin/time --append --output=$timecap  -f "%e,%U,%S,%w,%c" $CMD
    iteration=$(( $iteration + 1 )) 
    echo ""
done
#exit 0
}

# Run c and go versions
compiledrun()
{
PROG=$1
LANG=$2
SETTINGS=$3
maxiterations=$4
iteration=1

while [ "$iteration" -le "$maxiterations" ]
do
    echo "$PROG $iteration of $maxiterations"
	echo -n "$PROG,$LANG," >> $timecap
	CMD=" $PROG $SETTINGS"
    /usr/bin/time --append --output=$timecap -f "%e,%U,%S,%w,%c"  $CMD
    iteration=$(( $iteration + 1 )) 
    echo ""
done
#exit 0
}

# Start execution
cd $appdir

if [ "$VERSION" -eq 2 ] ;then
    c
	CPROG="c/$prog-c"
	if [ -f "$CPROG" ] ;then
		compiledrun $CPROG "c" $SETTINGS $MAXITERATIONS
	fi

    # go
	GOPROG="go/$prog-go"

	if [ -f "$GOPROG" ] ;then
		compiledrun $GOPROG "go" $SETTINGS $MAXITERATIONS
	fi

    #python 
	pyrun $py27 $prog.py $MAXITERATIONS
	pyrun $pypy $prog.py $MAXITERATIONS
	pyrun $stackless $prog.py $MAXITERATIONS
fi

if [ $VERSION -eq 3 ] ;then
	pyrun $py32 $prog.py $MAXITERATIONS
fi