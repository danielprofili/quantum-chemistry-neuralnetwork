#!/bin/bash
# nn_input
#
# Generates the neural network input files containing xyz, gzmat, and charge data
# for each perturbation
# 
# 29 May 2018

dest_dir="nn"
working_dir=$(pwd)

# first determine minimum energy
min=$(./min_energy.sh)

# initialize the input file
#echo "BEGIN INPUT FILE" > $working_dir/input
echo "BEGIN INPUT FILE" > $working_dir/$dest_dir/input_all.qc
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
                cd subs
                # Filter based on energy
                energy=$(grep "Total Energy" ${f}/${f}.out | grep -E -o "\-[0-9]+\.[0-9]+")
                empty_flag=$(echo $energy | wc -w)
                if [ $flag -ge 1 ]; then
                        cd $working_dir
                        filename=$(python ${working_dir}/filter_by_energy.py ${min} ${energy})
                        filename_empty_flag=$(echo $filename | wc -w)
                        #echo $filename
                        #echo $filename_empty_flag

                        # only write if the filter script actually sorted into a file
                        # (if the energy is too high, the filter script won't return
                        # a value - this is so there aren't arbitrary large numbers
                        # in the thresholds)
                        if [ $filename_empty_flag -ge 1 ]; then
                                source $working_dir/write_input.sh $f $working_dir/$dest_dir/$filename
                        fi
                        source $working_dir/write_input.sh $f $working_dir/$dest_dir/input_all.qc
                        #echo -e "\n$f\n" >> $working_dir/input
                        #cat xyz/$f.xyz >> $working_dir/input
                        #echo -e "\n===================\n" >> $working_dir/input
                        #cat gzmat/$f.gzmat >> $working_dir/input
                        #echo -e "\n===================\n" >> $working_dir/input
                        #echo -e "Begin charges\n" >> $working_dir/input
                        #cat $working_dir/subs/$f/$f.charges >> $working_dir/input
                        #echo -e "\n===================\n" >> $working_dir/input
                fi
        fi
        #echo DEBUG
        #sleep 5
done
