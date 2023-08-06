#!/bin/bash
# Run install_service from commandline to insert PROJ_PATH
PROJ_PATH=/home/pi/projects/FHmonitor
. $PROJ_PATH/venv/bin/activate
python3 $PROJ_PATH/FHmonitor/systemd/FHmonitor_main.py
