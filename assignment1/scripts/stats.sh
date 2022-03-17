#!/bin/bash
for i in 1 5
do
	for j in {3..5}
	do
		TIME=0
		NUMBER=$((i*10**j))
		for k in {0..4}
		do
			SKYFILE="../data/N${NUMBER}_${k}"
			TIME=`echo "${TIME}+$(./tp.sh -a seuil -e ${SKYFILE} -t)" | bc -l`  
		done
		TIME=`echo "scale=6;${TIME}/5" | bc -l` 
		echo -e "Number of buildings : ${NUMBER}, \tAverage time (ms) :  ${TIME}"
	done	
done
