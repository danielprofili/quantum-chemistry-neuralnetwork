#!/bin/bash

# Script to create a .pbs file for each .inp file
pbstemplate="./pbs.template"

for f in ../inp/*.inp
do
    filename=${f:0:${#f}-4}
    filename=${filename:7:${#f}}
    # sed -i 's/FILL/$f/g' $filename.pbs  
    cat ${pbstemplate} | sed "s/FILL/${filename}/g" > ${filename}.pbs
    #echo $filename
    

done
