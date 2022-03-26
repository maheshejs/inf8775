#!/bin/bash
ALGO=""
EXAMPLE_FILE=""
OPTIONS=""

while getopts "a:e:ptx" FLAG; # x is optional to compute maximum height
do
  case "${FLAG}" in
    a)
      ALGO="${OPTARG}";;
    e) 
      EXAMPLE_FILE="${OPTARG}";;
    p | t | x)
      OPTIONS+="${FLAG}";;
    ?)
      echo "ERROR : Wrong option."
      exit 1;;
  esac
done

if [ ! -z "${OPTIONS}" ]; then
  OPTIONS="-${OPTIONS}"
fi

python3 ../sources/box_stacking.py -a $ALGO -e $EXAMPLE_FILE $OPTIONS
