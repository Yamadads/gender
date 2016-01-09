#!/bin/bash
echo "Start!"
for x in $(cat files)
do
    echo $x >> result
    python3 inf117269.py "train/"$x >> result
    echo $x
done
