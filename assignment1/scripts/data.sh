#!/bin/bash
for n in {"1000","5000","10000","50000","100000","500000"}; do
    py ../sources/inst_gen.py -s $n -n 5
done