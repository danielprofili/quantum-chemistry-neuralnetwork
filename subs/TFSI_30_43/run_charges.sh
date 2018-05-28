#!/bin/bash

name=$1
np=$2

# these are codes and data files needed by job
# might want to change to global path here 
# as these will be used by every job
rootpath="/gpfs/pace1/project/chem-mcdaniel/dprofili3/NN_project/TFSI_charge_fitting/quantum_chemistry"
rundma="$rootpath/charge_submission/gdma"
dmatemplate="$rootpath/charge_submission/gdma_template.data"
#psi4template="psi4_template.inp"
runmpfit="$rootpath/charge_submission/mpfit"
runparse="$rootpath/charge_submission/parse_psiDMA.pl"

# these are i/o file names based on input name
dmainput="${name}_gdma.data"
dmaoutput="${name}.dma"
chargeoutput="${name}.charges"
ifile=${name}.inp
ofile=${name}.out
stdout=${name}.stdout

# temporary file, should be a safe name...
tempfile=testzzzz

#change name of .fchk output in input file
#cat ${psi4template} | sed "s/FILL/${name}/g" > $ifile
#change name of .fchk in gdma.data file for gdma code
cat $dmatemplate | sed "s/FILL/${name}/g" > $dmainput

# run psi4 calculation.  This will create rather large
# .fchk file which we delete when we're done with it
psi4 -n $np $ifile $ofile >& $stdout

# run dma code
$rundma < $dmainput > $dmaoutput
# now reove .fchk file
rm ${name}.fchk
# need to do this for parsing code
cat $ofile $dmaoutput > $tempfile
mv $tempfile $dmaoutput
#parse
$runparse $dmaoutput > $tempfile
mv $tempfile $dmaoutput
#finally charges
$runmpfit $dmaoutput > $chargeoutput
