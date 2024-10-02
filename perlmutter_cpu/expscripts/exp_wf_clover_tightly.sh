#!/bin/bash
#SBATCH -J ExpWFTightClover
#SBATCH -o %x-%j.out
#SBATCH -t 00:29:00
#SBATCH -q debug
#SBATCH -C cpu
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=1

# run by tightly coupled way
DATAPREFIX=/pscratch/sd/z/zw241/zw241/VisPerfStudy/dataset/cloverleaf_multistep_decomp/fb_cv_
DATASUFFIX=.4_4_8.128_128_128.visit
RUNDIR=/pscratch/sd/z/zw241/zw241/VisPerfStudy/Results/VisPerfExp_wf_tight_clover_${1}
CURRDIR=$(pwd)
SIMSLEEP=20
TOTALCYCLE=5

mkdir -p $RUNDIR

cd $RUNDIR

ln -s $CURRDIR/../install/visReader/looselyworkflow/looselyinsitu looselyinsitu
ln -s $CURRDIR/../install/visReader/looselyworkflow/tightlyinsitu_pa tightlyinsitu_pa
ln -s $CURRDIR/../install/visReader/looselyworkflow/tightlyinsitu_we tightlyinsitu_we

mkdir -p tightinsituwf
cd tightinsituwf

# TODO add parameter for 228 or 448 in pa 
srun -N 4 -n 128 --mem-per-cpu=10G ../tightlyinsitu_pa \
--vtkm-device serial \
${DATAPREFIX} \
${SIMSLEEP} \
${TOTALCYCLE} ${DATASUFFIX} &> tightinsituwf.log


# run by loosely coupled way with rrb


# run by loosley coupled way with tracing+block assignment


# run by loosley couled way with estimation + block assignment


# run by loosley coupled way with estimation per two cycle + block assigment
