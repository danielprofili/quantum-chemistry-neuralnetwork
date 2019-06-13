#!/bin/bash
usage="USAGE: ./make_molecules.sh MOLECULE COUNT NET_CHARGE BATCHSIZE SCRIPTS_FOLDER GZMAT_TEMPLATE GZMAT_FOLDER XYZ_FOLDER"
[ ! -z $1 ] && molecule=$1 || { echo $usage; exit 1; }
[ ! -z $2 ] && count=$2 || { echo $usage; exit 1; }
[ ! -z $3 ] && net_charge=$3 || { echo $usage; exit 1; }
[ ! -z $4 ] && scripts_folder=$4 || { echo $usage; exit 1; }
[ ! -z $5 ] && gzmat_temp=$5 || { echo $usage; exit 1; }
[ ! -z $6 ] && gzmat_folder=$6 || { echo $usage; exit 1; }
[ ! -z $7 ] && xyz_folder=$7 || { echo $usage; exit 1; }

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
