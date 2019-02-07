#!/bin/bash

# Script to convert all .gzmat files in a directory into .xyz files with
# the same filenames. Assumes openbabel already loaded.


home_dir=$(pwd)
help_msg="USAGE: gzmat2xyz.sh SRC DEST"
[ ! -z $1 ] && src_dir=$1 || { echo $help_msg; exit 1; }
[ ! -z $2 ] && dest_dir=$2 || { echo $help_msg; exit 1; }

# cd to the source directory because it's a pain to modify the paths otherwise
cd $src_dir
for f in *.gzmat
do
    filename=${f:0:${#f}-6}
    touch $home_dir/$dest_dir/$filename.xyz
    obabel -igzmat "$f" -oxyz > "$home_dir/$dest_dir/$filename.xyz"
    # echo $filename
done

# back home
cd $home_dir
