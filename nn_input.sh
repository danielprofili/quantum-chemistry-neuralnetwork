#!/bin/bash
# nn_input
#
# Generates the neural network input files containing xyz, gzmat, and charge data
# for each perturbation
# 
# 29 May 2018

dest_dir="/nn"
working_dir=$(pwd)
cd subs
for f in *
do
# f is the folder (i.e. the perturbation name TFSI_xxx_xx)
    cd $f 
    #echo $f 
    cat $f.charges >> $working_dir/input
    cd $working_dir
    cat xyz/$f.xyz >> $working_dir/input
    cat gzmat/$f.gzmat >> $working_dir/input
done
