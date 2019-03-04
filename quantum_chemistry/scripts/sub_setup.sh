#!/bin/bash
usage="USAGE: sub_setup.sh MOLECULE PBS_DIR SUBMISSION_DIR INP_DIR RUN_TEMPLATE BATCH_JOB_TEMPLATE"
[ ! -z $1 ] && molecule_name=$1 || { echo $usage; exit 1; }
[ ! -z $2 ] && pbs_folder=$2 || { echo $usage; exit 1; }
[ ! -z $3 ] && sub_folder=$3 || { echo $usage; exit 1; }
[ ! -z $4 ] && inp_folder=$4 || { echo $usage; exit 1; }
[ ! -z $5 ] && run_template=$5 || { echo $usage; exit 1; }
[ ! -z $6 ] && multijob_template=$6 || { echo $usage; exit 1; }

# load psi4 module (and dependencies)
module load intel/15.0
module load openmpi/1.8
module load mkl/11.2
module load python/2.7
module load boost/1.53.0
module load psi4

#echo $pbs_folder
#sleep 200
count=0

# create jobs.txt file in sub folder
jobs_file=$sub_folder/jobs.txt
# clears the file
> $jobs_file

for f in $pbs_folder/*.pbs
do
    #filename=${f:0:${#f}-4}
    #filename=${filename:4:${#f}}

    filename=${f##*/}
    #echo $filename
    #sleep 200

    # trims the longest match from the end (i.e. trim the longest sequence of characters beginning with 
    # a period from the end)
    filename=${filename%%.*}
    #molecule_name=${filename%%_*}
    inp_file="${filename}.inp"
    pbs_file="${filename}.pbs"
    #echo $filename
    #sleep 200
    #cd subs
    working_dir=$sub_folder/$filename
    mkdir -p $working_dir
    cp $inp_folder/$inp_file $working_dir/$inp_file
    cp $pbs_folder/$pbs_file $working_dir/$pbs_file
    # change the FILL in the inp file (no other better place to do it?)
    cat $working_dir/$inp_file | sed "s/FILL/${filename}/g" > $working_dir/temp_inp
    mv $working_dir/temp_inp $working_dir/$inp_file
    cp $run_template $working_dir/run_charges.sh
    chmod +x $working_dir/run_charges.sh
    #source ../load_psi4.sh
    cd $working_dir
    #qsub $working_dir/$pbs_file     

    echo "cd ${working_dir} ; bash ${pbs_file}" >> $jobs_file
    

    #cd ../..
    ((count+=1))
done

echo "Done creating jobs file"

echo "Creating batch job file..."
# fill jobs file with correct information (i.e. number of jobs and job name)
multijob_file=$sub_folder/multijob
cp $multijob_template $multijob_file

#cat $multijob_file
#sleep 100

#cat $multijob_file | sed "s/FILL_JOB_NAME/${molecule_name}/g" > $multijob_file
sed "s/FILL_JOB_NAME/${molecule_name}-$(date +%F_%H%M)/g" <$multijob_file >temp
mv temp $multijob_file
#cat $multijob_file | sed "s/FILL_NUM_JOBS/${count}/g" > $multijob_file
sed "s/FILL_NUM_JOBS/${count}/g" <$multijob_file >temp
mv temp $multijob_file
echo "..done"

echo "Submitting job..."

# have to submit from subs folder to make sure results file goes in right place
cd $sub_folder
qsub $multijob_file



