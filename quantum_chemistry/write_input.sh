#!/bin/bash
# writes contents of data folder (first arg) to location (second arg)
f=$1
output_loc=$2

#echo $output_loc
touch $output_loc
echo -e "\n$f\n" >> "$output_loc"
cat xyz/$f.xyz >> "$output_loc"
echo -e "\n===================\n" >> "$output_loc"
cat gzmat/$f.gzmat >> "$output_loc"
echo -e "\n===================\n" >> "$output_loc"
echo -e "Begin charges\n" >> "$output_loc"
cat $working_dir/subs/$f/$f.charges >> "$output_loc"
echo -e "\n===================\n" >> "$output_loc"
