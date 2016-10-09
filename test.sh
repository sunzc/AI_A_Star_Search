#!/bin/sh
N=0

until [ $N -ge 20 ];
do
	N=`expr $N + 1`
	echo $N
	RETVAL=124
	until [ $RETVAL -eq 0 ]; do
		python3 ./puzzleGenerator.py 4 output_$N.txt
		timeout 60 ./puzzleSolver.py 2 4 output_$N.txt output_$N.res_h2
		RETVAL=$?
	done
	./puzzleSolver.py 2 4 output_$N.txt output_$N.res_h2
done
