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


# Perturb template gzmat file 
# convert to gzmat
source $scripts_folder/load_openbabel.sh
obabel -i xyz molecules/$molecule.xyz -o gzmat > molecules/$molecule.gzmat
#cd $gzmat_folder
echo "[$(date +"%F %T")] Perturbing $count molecules..."
gzmat_temp="molecules/${molecule}.gzmat"
python $scripts_folder/perturb.py $gzmat_temp --count $count --percent 0.05 --output-dir $gzmat_folder --reset 100
echo "[$(date +"%F %T")]...done"

# Convert gzmat files to xyz
echo "[$(date +"%F %T")]Converting to .gzmat..."
source $scripts_folder/load_openbabel.sh
source $scripts_folder/gzmat2xyz.sh $gzmat_folder $xyz_folder >/dev/null
echo "[$(date +"%F %T")]...done"

# write xyz files to inp files
#cd $xyz_folder
echo "[$(date +"%F %T")]Making input files..."

# create template, if necessary
inp_template_path=$templates_folder/$molecule/$molecule.inp
pbs_template_path=$templates_folder/$molecule/$molecule.pbs
if [ ! -d $templates_folder/$molecule ]; then
        mkdir -p $templates_folder/$molecule
        cp $templates_folder/inp $inp_template_path
        cp $templates_folder/pbs $pbs_template_path
        sed -i "s/MOLECULE_FLAG/${molecule}/" $inp_template_path
        sed -i "s/CHARGE_FLAG/${net_charge}/" $inp_template_path
fi

# run script
python $scripts_folder/make_inp.py --source-dir $xyz_folder --dest-dir $inp_folder --template $inp_template_path 
#cd ..
#mv $xyz_folder/*.inp $inp_folder
echo "[$(date +"%F %T")]...done"

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

# generate the input file
#echo "\nGenerating neural network input file..."
#./nn_input.sh
#echo "...done"

echo "[$(date +"%F %T")]Process completed successfully!"
