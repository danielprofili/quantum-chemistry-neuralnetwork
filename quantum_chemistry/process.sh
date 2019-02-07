#!/bin/bash

# Script to automate entire process from perturb all the way to creating and 
# submitting input files
#
# 1. Perturb template gzmat and generate 360*10 new gzmat files with random
#    molecule configurations
# 2. Convert gzmat files to xyz files
# 3. Write xyz files to psi4 .inp files
# 4. Write .pbs PACE job files that reference the .inp files and run psi4

[ ! -z $1 ] && molecule=$1 || { echo "USAGE: process.sh MOLECULE (COUNT)"; exit 1; }
[ ! -z $2 ] && count=$2 || count=100
#gzmat_temp= [ ! -z $1 ] && $1 || "TFSI.gzmat"
root_dir="$(pwd)/output/${molecule}_$(date +%F_%T)"
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


# Perturb template gzmat file 
#cd $gzmat_folder
echo "Perturbing $count molecules..."
gzmat_temp="molecules/${molecule}.gzmat"
python $scripts_folder/perturb.py $gzmat_temp --count $count --percent 0.05 --output-dir $gzmat_folder --reset 100
echo "...done"

# Convert gzmat files to xyz
echo "Converting to .gzmat..."
source $scripts_folder/load_openbabel.sh
source $scripts_folder/gzmat2xyz.sh $gzmat_folder $xyz_folder
#cd ..
#mv $gzmat_folder/*.xyz $xyz_folder
echo "...done"

# write xyz files to inp files
#cd $xyz_folder
echo "Making input files..."
python $scripts_folder/make_inp.py --source-dir $xyz_folder --dest-dir $inp_folder --template $templates_folder/$molecule.inp
#cd ..
#mv $xyz_folder/*.inp $inp_folder
echo "...done"

# Write pbs files
#cd $inp_folder
echo "Writing pbs files..."
source $scripts_folder/inp2pbs.sh $templates_folder/$molecule.pbs $pbs_folder $inp_folder
#cd ..
#mv $inp_folder/*pbs $pbs_folder
echo "...done"

# set up the submission directories
echo "Setting up submission directories..."
#cd ${molecule}_files
source $scripts_folder/sub_setup.sh $pbs_folder $sub_folder $inp_folder $templates_folder/run_charges.sh
echo "...done"

# generate the input file
#echo "\nGenerating neural network input file..."
#./nn_input.sh
#echo "...done"

echo "Process completed successfully!"
