#!/bin/bash
# Sub-script to submit jobs to PACE. Don't use it on its own!

# lazy; should fix this
$scripts_folder=$1
$pbs_template_path=$2
$pbs_folder=$3
$inp_folder=$4
$sub_folder=$5
$templates_folder=$6

# Write pbs files
#cd $inp_folder
echo "[$(date +"%F %T")]Writing pbs files..."
source $scripts_folder/inp2pbs.sh $pbs_template_path $pbs_folder $inp_folder
#cd ..
#mv $inp_folder/*pbs $pbs_folder
echo "[$(date +"%F %T")]...done"

# set up the submission directories
echo "[$(date +"%F %T")]Setting up submission directories..."
#cd ${molecule}_files
source $scripts_folder/sub_setup.sh $molecule $pbs_folder $sub_folder $inp_folder $templates_folder/run_charges.sh $templates_folder/multijob
echo "[$(date +"%F %T")]...done"
