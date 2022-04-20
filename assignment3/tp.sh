#!/bin/bash
EXAMPLE_FILE=""
PRINT_SOL=0

while getopts "e:p" FLAG; 
do
  case "${FLAG}" in
    e) 
      EXAMPLE_FILE="${OPTARG}";;
    p)
      PRINT_SOL=1;;
  esac
done

bin/tp3 $EXAMPLE_FILE $PRINT_SOL
