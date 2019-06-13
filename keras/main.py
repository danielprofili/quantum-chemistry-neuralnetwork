#!/usr/bin/python
import sys
import NN_qc_fit_main as methods

"""
This script acts as a wrapper for user interaction with the neural network. 

Usage: python main.py [inputfile]
    If no input file is specified, the script will use "input_all.qc".
"""

if len(sys.argv) > 1:
    inputfile = sys.argv[1]
else:
    inputfile='input_all.qc'
    print("No input file specified. Using default (input_all.qc)")

model, symmetry_funs = methods.build_model(inputfile)
methods.fit_model(model)
predictions = methods.model_predict(model, symmetry_funs)
