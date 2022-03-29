#!/bin/bash
ALGO=""
while getopts "a:" FLAG;
do
  case "${FLAG}" in
    a)
      ALGO="${OPTARG}";;
    ?)
      echo "ERROR : Wrong option."
      exit 1;;
  esac
done

for i in 1 5
do
  for j in {2..5}
  do
    RUNNING_TIME=0
    RUNNING_HEIGHT=0
    NUMBER=$((i*10**j))
    if [ $i -eq 5 -a $j -eq 5 ]; then
      break
    fi
    for k in {1..10}
    do
      BOXFILE="../data/b${NUMBER}_${k}.txt"
      { read HEIGHT; read TIME;} <<< "$(./tp.sh -a ${ALGO} -e ${BOXFILE} -xt)"
      RUNNING_HEIGHT=`echo "${RUNNING_HEIGHT}+${HEIGHT}" | bc -l`  
      RUNNING_TIME=`echo "${RUNNING_TIME}+${TIME}" | bc -l`  
    done
    MEAN_TIME=`echo "scale=6;${RUNNING_TIME}/10" | bc -l` 
    MEAN_HEIGHT=`echo "scale=6;${RUNNING_HEIGHT}/10" | bc -l` 
    echo -e "No. blocks : ${NUMBER}, Mean time (ms) : ${MEAN_TIME}, Mean max height : ${MEAN_HEIGHT}"
  done  
done
