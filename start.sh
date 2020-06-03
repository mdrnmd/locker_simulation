#!/bin/sh
rm ./full_observations
rm ./solution
echo "Simulating"
python3 simulator.py >> full_observations
echo "Bye."
