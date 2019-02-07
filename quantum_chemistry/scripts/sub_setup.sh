#!/bin/bash
usage="USAGE: sub_setup.sh PBS_DIR SUBMISSION_DIR INP_DIR RUN_TEMPLATE"
[ ! -z $1 ] && pbs_folder=$1 || { echo $usage; exit 1; }
[ ! -z $2 ] && sub_folder=$2 || { echo $usage; exit 1; }
[ ! -z $3 ] && inp_folder=$3 || { echo $usage; exit 1; }
[ ! -z $4 ] && run_template=$4 || { echo $usage; exit 1; }

# load psi4 module (and dependencies)
module load intel/15.0
module load openmpi/1.8
module load mkl/11.2
module load python/2.7
module load boost/1.53.0
module load psi4

#echo $pbs_folder
#sleep 200

for f in $pbs_folder/*.pbs
do
    #filename=${f:0:${#f}-4}
    #filename=${filename:4:${#f}}

    filename=${f##*/}
    #echo $filename
    #sleep 200

    # trims the longest match from the end (i.e. trim the longest sequence of characters beginning with 
    # a period from the end)
    filename=${filename%%.*}
    inp_file="${filename}.inp"
    pbs_file="${filename}.pbs"
    #echo $filename
    #sleep 200
    #cd subs
    working_dir=$sub_folder/$filename
    mkdir -p $working_dir
    cp $inp_folder/$inp_file $working_dir/$inp_file
    cp $pbs_folder/$pbs_file $working_dir/$pbs_file
    # change the FILL in the inp file (no other better place to do it?)
    cat $working_dir/$inp_file | sed "s/FILL/${filename}/g" > $working_dir/temp_inp
    mv $working_dir/temp_inp $working_dir/$inp_file
    cp $run_template $working_dir/run_charges.sh
    chmod +x $working_dir/run_charges.sh
    #source ../load_psi4.sh
    cd $working_dir
    qsub $working_dir/$pbs_file     
    #cd ../..
done

