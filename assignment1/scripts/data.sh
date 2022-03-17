#!/bin/bash
for n in {"1000","5000","10000","50000","100000","500000"}; do
    python3 ../sources/inst_gen.py -s $n -n 5
done
