#!/bin/bash
EXAMPLE_FILE=""
OPTIONS=""

while getopts "e:p" FLAG; 
do
  case "${FLAG}" in
    e) 
      EXAMPLE_FILE="${OPTARG}";;
    p)
      OPTIONS+="${FLAG}";;
  esac
done

if [ ! -z "${OPTIONS}" ]; then
  OPTIONS="-${OPTIONS}"
fi

../sources/tp3 -e $EXAMPLE_FILE $OPTIONS
