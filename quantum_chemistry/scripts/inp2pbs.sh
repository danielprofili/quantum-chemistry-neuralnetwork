#!/bin/bash

# Script to create a .pbs file for each .inp file
# This script relies on a molecule-specific .pbs template file with "FILL" placeholder strings
# wherever the name of the file/molecule needs to be inserted.

[ ! -z $1 ] && pbstemplate=$1 || { echo "USAGE: inp2pbs.sh TEMPLATE OUTPUT_DIR"; exit 1; }
[ ! -z $2 ] && output_dir=$2 || { echo "USAGE: inp2pbs.sh TEMPLATE OUTPUT_DIR"; exit 1; }
#pbstemplate="./pbs.template"

for f in ../inp/*.inp
do
    filename=${f:0:${#f}-4}
    filename=${filename:7:${#f}}
    # sed -i 's/FILL/$f/g' $filename.pbs  
    cat ${pbstemplate} | sed "s/FILL/${filename}/g" > $output_dir/${filename}.pbs
    #echo $filename
    

done
