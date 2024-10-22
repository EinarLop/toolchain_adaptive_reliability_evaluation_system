#!/bin/bash
# Disable output (optional, similar to @echo off in batch scripts)
set +x

# Change directory to 'prism'
cd prism || exit

# Run the command (assuming 'prism.bat' has a corresponding Linux executable, e.g., 'prism')
./bin/prism -importtrans ctmc/ctmc.tra -ctmc ctmc/ctmc.csl

# Return to the previous directory
cd ../..
