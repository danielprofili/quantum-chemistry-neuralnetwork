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
        # put the check for success here
        # f is the folder (i.e. the perturbation name TFSI_xxx_xx)
        #echo $f 
        # Print the name at the top of the block
        cd $working_dir
        flag=`grep "Psi4 exiting" ${working_dir}/subs/${f}/${f}.out | wc | cut -c -10` 
        if [ $flag -eq 1 ] 
        then 
                echo -e "\n$f\n" >> $working_dir/input
                cat xyz/$f.xyz >> $working_dir/input
                echo -e "\n===================\n" >> $working_dir/input
                cat gzmat/$f.gzmat >> $working_dir/input
                echo -e "\n===================\n" >> $working_dir/input
                echo -e "Begin charges\n" >> $working_dir/input
                cat $working_dir/subs/$f/$f.charges >> $working_dir/input
                echo -e "\n===================\n" >> $working_dir/input
        fi
        #echo DEBUG
        #sleep 5
done
