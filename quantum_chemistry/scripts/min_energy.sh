#!/bin/bash
# min_energy

# Finds the minimum energy in all input files.
#
# 25 January 2019
#home=$(pwd)
help_msg="USAGE: ./min_energy.sh RESULTS_DIR"
[ ! -z $1 ] && results_dir=$1 || { echo $help_msg; exit 1; }
if [ -f $results_dir/min_energy ]; then
        cat $results_dir/min_energy 
else
        #cd subs
        min=0
        for f in *
        do
                # f is the folder name for the molecule output
                energy=$(grep "Total Energy" ${f}/${f}.out | grep -E -o "\-[0-9]+\.[0-9]+")
                #echo $energy
                # checks if the energy is empty
                flag=$(echo $energy | wc -w)
                #echo $flag
                #echo ${#flag}
                if [ $flag -ge 1 ]; then
                        #echo "flag passed"
                        comp=$(python ${home}/floating_comp.py ${min} ${energy})
                        #if (( $(echo "$min > $energy" | bc -l) )); then
                        #echo $comp
                        if [ $comp -eq 1 ]; then
                                #if [ ${energy} > ${min} ]; then
                                min=$energy
                                #echo "new min=$energy"
                                #sleep 1
                        fi
                fi
        done
        #cd $home
        echo $min > min_energy
        echo $min
fi
