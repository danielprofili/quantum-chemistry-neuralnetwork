#!/bin/bash
# nn_input
#
# Generates the neural network input files containing xyz, gzmat, and charge data
# for each perturbation
# 
# 29 May 2018
for f in subs/*
do
# f is the folder
    cd $f 
    
    cat $f.charges >> ../input_file
    cd ..
done
