#!/usr/bin/python
# Helper for the input file generator that determines which file to put the
# data file contents in. This file is dependent on an array of thresholds
# in the form [t0, t1, t2, ..., tn]. n+1 files will be written, where each file
# file_i (where i is one of t0, ..., tn) contains all data files with energy within
# minimum_energy + i (in millihartrees). 

from __future__ import division
import sys
min_energy = sys.argv[1]
energy = sys.argv[2]
thresholds = [20/1000, 50/1000, 100/1000, 500/1000, 1]

for rn in thresholds:
        if abs(float(energy) - float(min_energy)) <= rn:
                filename = "input_" + str(int(rn * 1000)) + ".qc"

                print(filename)
                break
