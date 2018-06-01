#!/bin/bash
# nn_input
#
# Generates the neural network input files containing xyz, gzmat, and charge data
# for each perturbation
# 
# 29 May 2018

dest_dir="/nn"
working_dir=$(pwd)
# initialize the input file
echo "BEGIN INPUT FILE" > $working_dir/input
cd subs
for f in *
do
# f is the folder (i.e. the perturbation name TFSI_xxx_xx)
    #echo $f 
    # Print the name at the top of the block
    cd $working_dir
    echo -e "\n$f\n" >> $working_dir/input
    cat xyz/$f.xyz >> $working_dir/input
    echo -e "\n===================\n" >> $working_dir/input
    cat gzmat/$f.gzmat >> $working_dir/input
    echo -e "\n===================\n" >> $working_dir/input
    cat $working_dir/subs/$f/$f.charges >> $working_dir/input
    echo -e "\n===================\n" >> $working_dir/input
    #echo DEBUG
    #sleep 5
done
