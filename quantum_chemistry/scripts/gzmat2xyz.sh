#!/bin/bash

# Script to convert all .gzmat files in a directory into .xyz files with
# the same filenames. Assumes openbabel already loaded.


#home_dir=$(pwd)
help_msg="USAGE: gzmat2xyz.sh SRC DEST"
[ ! -z $1 ] && src_dir=$1 || { echo $help_msg; exit 1; }
[ ! -z $2 ] && dest_dir=$2 || { echo $help_msg; exit 1; }

# cd to the source directory because it's a pain to modify the paths otherwise
#cd $src_dir
for f in $src_dir/*.gzmat
do
    #echo $f
    #sleep 50
    #filename=${f:0:${#f}-6}
    filename=${f##*/}
    filename=${filename%%.*}
    touch $dest_dir/$filename.xyz
    obabel -igzmat "$f" -oxyz > "$dest_dir/$filename.xyz" 
    # echo $filename
done

# back home
#cd $home_dir
