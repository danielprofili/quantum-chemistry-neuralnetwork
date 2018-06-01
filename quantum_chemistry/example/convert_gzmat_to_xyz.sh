#!/bin/bash

module load eigen/3.0.5
module load python/2.7
module load wxWidgets/2.8.12
module load openbabel/2.3.2

files=gzmat/*.gzmat
for f in $files
do
    obabel -igzmat TFSI2.gzmat -oxyz > TFSI2.xyz
   
done



