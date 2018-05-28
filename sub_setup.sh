#!/bin/bash

for f in inp/*.pbs
do
    filename=${f:0:${#f}-4}
    filename=${filename:4:${#f}}
    inp_file="${filename}.inp"
    pbs_file="${filename}.pbs"
    echo $filename
    #sleep 2
    cd subs
    mkdir $filename
    cp ../inp/$inp_file $filename/$inp_file
    cp ../inp/$pbs_file $filename/$pbs_file
    # change the FILL in the inp file (no other better place to do it?)
    cat $filename/$inp_file | sed "s/FILL/${filename}/g" > $filename/temp_inp
    mv $filename/temp_inp $filename/$inp_file
    cp ../charge_submission/run_charges.sh $filename/run_charges.sh
    chmod +x $filename/run_charges.sh
    source ../load_psi4.sh
    cd $filename
    qsub $pbs_file     
    cd ../..
done

