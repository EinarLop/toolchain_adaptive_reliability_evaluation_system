#!/bin/bash
# Disable output (optional, similar to @echo off in batch scripts)
set +x 

# Change directory to 'ctmc'
cd ctmc || exit

# Run the Python script
python3 CTMC.py

# Return to the previous directory
cd ..
