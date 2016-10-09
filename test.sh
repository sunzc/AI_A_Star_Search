#!/bin/sh
N=0

until [ $N -ge 20 ];
do
	N=`expr $N + 1`
	echo $N
	RETVAL=124
	until [ $RETVAL -eq 0 ]; do
		python3 ./puzzleGenerator.py 4 20 output_$N.txt
		timeout 30 ./puzzleSolver.py 1 4 output_$N.txt output_$N.res_h2 2
		RETVAL=$?
	done
	./puzzleSolver.py 1 4 output_$N.txt output_$N.res_h1 1
done
