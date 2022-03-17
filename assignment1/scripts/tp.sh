#!/bin/bash
ALGO=""
EXAMPLE_FILE=""
OPTIONS=""

while getopts "a:e:pt" FLAG;
do
  case "${FLAG}" in
    a)
      ALGO="${OPTARG}";;
    e) 
      EXAMPLE_FILE="${OPTARG}";;
    p | t) 
      OPTIONS+="${FLAG}";;
    ?)
      echo "ERROR : Wrong option."
      exit 1;;
  esac
done

if [ ! -z "${OPTIONS}" ]; then
  OPTIONS="-${OPTIONS}"
fi

python3 ../sources/skyline.py -a $ALGO -e $EXAMPLE_FILE $OPTIONS
