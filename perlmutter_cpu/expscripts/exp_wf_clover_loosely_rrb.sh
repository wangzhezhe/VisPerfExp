#!/bin/bash
#SBATCH -J ExpWFLooseRRBClover
#SBATCH -o %x-%j.out
#SBATCH -t 00:10:00
#SBATCH -q debug
#SBATCH -C cpu
#SBATCH --nodes=5

#export MARGO_ENABLE_MONITORING=1

# run by tightly coupled way
DATAPREFIX=/pscratch/sd/z/zw241/zw241/VisPerfStudy/dataset/cloverleaf_multistep_decomp/fb_cv_
DATASUFFIX=.4_4_8.128_128_128.visit
RUNDIR=/pscratch/sd/z/zw241/zw241/VisPerfStudy/Results/VisPerfExp_wf_loose_rrb_clover_${1}
CURRDIR=$(pwd)
SIMSLEEP=2
TOTALCYCLE=5

mkdir -p $RUNDIR

cd $RUNDIR

ln -s $CURRDIR/../install/visReader/looselyworkflow/looselyinsitu looselyinsitu
ln -s $CURRDIR/../install/visReader/looselyworkflow/tightlyinsitu_rrb tightlyinsitu_rrb

# start vis server using 16 processes
srun -N 1 -n 16 -c 4 --mem-per-cpu=5G --network=no_vni -l ./looselyinsitu --vtkm-device serial cxi debug &> looselywf.log &

# when there existance of the config file
while [ ! -f ./masterinfo.conf ]
do
    sleep 0.5
done

# TODO add parameter for 228 or 448 in pa 
srun -N 4 -n 128 -c 2 --mem-per-cpu=5G --network=no_vni -l ./tightlyinsitu_rrb cxi masterinfo.conf ${DATAPREFIX} ${DATASUFFIX} ${TOTALCYCLE} ${SIMSLEEP} &> tightly_rrb.log


wait

# run by loosely coupled way with rrb


# run by loosley coupled way with tracing+block assignment


# run by loosley couled way with estimation + block assignment


# run by loosley coupled way with estimation per two cycle + block assigment
