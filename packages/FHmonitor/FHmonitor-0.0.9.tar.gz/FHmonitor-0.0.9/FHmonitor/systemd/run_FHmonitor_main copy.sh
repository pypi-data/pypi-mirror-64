#!/bin/bash
# Run install_service from commandline to insert PROJ_PATH

. $PROJ_PATH/venv/bin/activate
python3 $PROJ_PATH/systemd/FHmonitor_main.py
