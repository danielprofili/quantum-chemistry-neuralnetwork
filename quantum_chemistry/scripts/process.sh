#!/bin/bash

# Script to automate entire process from perturb all the way to creating and 
# submitting input files
#
# 1. Perturb template gzmat and generate 360*10 new gzmat files with random
#    molecule configurations
# 2. Convert gzmat files to xyz files
# 3. Write xyz files to psi4 .inp files
# 4. Write .pbs PACE job files that reference the .inp files and run psi4

[ ! -z $1 ] && gzmat_temp=$1 || { echo "Specify a template"; exit 1; }
#gzmat_temp= [ ! -z $1 ] && $1 || "TFSI.gzmat"
xyz_folder="../xyz"
gzmat_folder="../gzmat"
inp_folder="../inp"
pbs_folder="../pbs"
sub_folder="../charge_submission"

# Perturb template gzmat file 3600 times
cd $gzmat_folder
python perturb.py $gzmat_temp 

# Convert gzmat files to xyz
./gzmat2xyz.sh
cd ..
mv $gzmat_folder/*.xyz $xyz_folder

# write xyz files to inp files
cd $xyz_folder
python make_inp.py
cd ..
mv $xyz_folder/*.inp $inp_folder

# Write pbs files
cd $inp_folder
source inp2pbs.sh
cd ..
mv $inp_folder/*pbs $pbs_folder

# set up the submission directories
./sub_setup.sh

# generate the input file
./nn_input.sh
