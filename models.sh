#!/bin/bash
_now=$(date +"%m_%d_%Y")
_file="$_now.dat"
python manage.py models panov request > "$_file" 2>&1