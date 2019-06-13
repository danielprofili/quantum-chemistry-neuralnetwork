#!/bin/bash

# Script to automate entire process from perturb all the way to creating and 
# submitting input files
#
# 1. Perturb template gzmat and generate 360*10 new gzmat files with random
#    molecule configurations
# 2. Convert gzmat files to xyz files
# 3. Write xyz files to psi4 .inp files
# 4. Write .pbs PACE job files that reference the .inp files and run psi4

[ ! -z $1 ] && molecule=$1 || { echo "USAGE: process.sh MOLECULE (COUNT) (NET CHARGE) (BATCHSIZE)"; exit 1; }
[ ! -z $2 ] && count=$2 || count=100
[ ! -z $3 ] && net_charge=$3 || net_charge=0
#[ ! -z $3 ] && batch_size=$3 || batch_size=1000
#gzmat_temp= [ ! -z $1 ] && $1 || "TFSI.gzmat"
root_dir="$(pwd)/output/${molecule}-$(date +%F)/$(date +%H%M)"
mkdir -p $root_dir

xyz_folder="$root_dir/xyz"
gzmat_folder="$root_dir/gzmat"
inp_folder="$root_dir/inp"
pbs_folder="$root_dir/pbs"
sub_folder="$root_dir/subs"
scripts_folder="$(pwd)/scripts"
templates_folder="$(pwd)/templates"

# set up directories
mkdir -p $xyz_folder
mkdir -p $gzmat_folder
mkdir -p $inp_folder
mkdir -p $pbs_folder
mkdir -p $sub_folder

# Generate the molecules
source $scripts_folder/make_molecules.sh $molecule $count $net_charge $scripts_folder $gzmat_temp $gzmat_folder $xyz_folder

# Submit to PACE
source $scripts_folder/pace_submit.sh $scripts_folder $pbs_template_path $pbs_folder $inp_folder $sub_folder $templates_folder

# generate the input file
#echo "\nGenerating neural network input file..."
#./nn_input.sh
#echo "...done"

echo "[$(date +"%F %T")]Process completed successfully!"
