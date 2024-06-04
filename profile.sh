#!/bin/bash

export DISPLAY=:0

vncviewer 192.168.0.143:5900 &

sleep 5

python3 -m cProfile -o main.pstats main.py
unset GTK_PATH
gprof2dot -f pstats main.pstats | dot -Tpng -o output.png && eog output.png