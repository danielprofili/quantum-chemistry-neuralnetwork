#!/bin/bash

# Script to convert all .gzmat files in a directory into .xyz files with
# the same filenames

source load_openbabel.sh

for f in *.gzmat
do
    filename=${f:0:${#f}-6}
    obabel -igzmat "$f" -oxyz > "$filename.xyz"
    # echo $filename

done
