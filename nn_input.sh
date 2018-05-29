#!/bin/bash

for f in subs/*
do
# f is the folder
    cd $f 
    
    cat $f.charges >> ../input_file
    cd ..
done
