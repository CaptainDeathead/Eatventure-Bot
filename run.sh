#!/bin/bash

export DISPLAY=:0

vncviewer 192.168.0.143:5900 &

sleep 5

python3 main.py
