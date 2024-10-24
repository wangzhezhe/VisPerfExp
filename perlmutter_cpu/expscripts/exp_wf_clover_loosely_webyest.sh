#!/bin/bash
#SBATCH -J ExpWFLooseWeByEstClover
#SBATCH -o %x-%j.out
#SBATCH -t 00:10:00
#SBATCH -q debug
#SBATCH -C cpu
#SBATCH --nodes=6

#export MARGO_ENABLE_MONITORING=1

# run by tightly coupled way
DATAPREFIX=/pscratch/sd/z/zw241/zw241/VisPerfStudy/dataset/cloverleaf_multistep_decomp/fb_cv_
DATASUFFIX=.4_4_8.128_128_128.visit
RUNDIR=/pscratch/sd/z/zw241/zw241/VisPerfStudy/Results/VisPerfExp_wf_loose_webyest_clover_${1}
CURRDIR=$(pwd)
SIMSLEEP=2
TOTALCYCLE=5

mkdir -p $RUNDIR

cd $RUNDIR

ln -s $CURRDIR/../install/visReader/looselyworkflow/looselyinsitu looselyinsitu
ln -s $CURRDIR/../install/visReader/looselyworkflow/tightlyinsitu_webyest tightlyinsitu_webyest


# start vis server using 16 processes
srun -N 2 -n 16 -c 8 --mem-per-cpu=5G --network=no_vni --cpu_bind=cores -l ./looselyinsitu --vtkm-device serial cxi info &> looselywf_we_est.log &

# when there existance of the config file
while [ ! -f ./masterinfo.conf ]
do
    sleep 0.5
done

# copy the data processing script into current dir
module load python/3.9-anaconda-2021.11

cp $CURRDIR/parser_block_workloads.py .
cp $CURRDIR/generate_assignment_actual_bpacking_dup_capacity_vector.py .

# TODO add parameter for 228 or 448 in pa 
srun -N 4 -n 128 -c 2 --mem-per-cpu=5G --network=no_vni --cpu_bind=cores -l ./tightlyinsitu_webyest cxi masterinfo.conf ${DATAPREFIX} ${DATASUFFIX} ${TOTALCYCLE} ${SIMSLEEP} &> tightlyinsitu_webyest.log


wait
