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
[ ! -z $2 ] && count=$2 || count=10000
#gzmat_temp= [ ! -z $1 ] && $1 || "TFSI.gzmat"
xyz_folder="${molecule}_files/xyz"
gzmat_folder="${molecule}_files/gzmat"
inp_folder="${molecule}_files/inp"
pbs_folder="${molecule}_files/pbs"
sub_folder="${molecule}_files/charge_submission"
scripts_folder="scripts"
templates_folder="templates"

# set up directories
mkdir -p $xyz_folder
mkdir -p $gzmat_folder
mkdir -p $inp_folder
mkdir -p $pbs_folder
mkdir -p $sub_folder

# Perturb template gzmat file 
#cd $gzmat_folder
echo "Perturbing molecules..."
gzmat_temp="molecules/${molecule}.gzmat"
python $scripts_folder/perturb.py $gzmat_temp --count $count --percent 0.05 --output-dir $gzmat_folder --reset 100
echo "...done"

# Convert gzmat files to xyz
echo "\nConverting to .gzmat..."
source $scripts_folder/load_openbabel.sh
source $scripts_folder/gzmat2xyz.sh $gzmat_folder $xyz_folder
#cd ..
#mv $gzmat_folder/*.xyz $xyz_folder
echo "...done"

# write xyz files to inp files
#cd $xyz_folder
echo "\nMaking input files..."
python ./scripts/make_inp.py --source_dir $xyz_folder --dest-dir $inp_folder --template $templates_folder/$molecule.inp
#cd ..
#mv $xyz_folder/*.inp $inp_folder
echo "...done"

# Write pbs files
#cd $inp_folder
echo "\nWriting pbs files..."
source inp2pbs.sh $templates_folder/$molecule.pbs $pbs_folder
#cd ..
#mv $inp_folder/*pbs $pbs_folder
echo "...done"

# set up the submission directories
echo "\nSetting up submission directories..."
./sub_setup.sh
echo "...done"

# generate the input file
#echo "\nGenerating neural network input file..."
#./nn_input.sh
#echo "...done"

echo "Process completed successfully!"
