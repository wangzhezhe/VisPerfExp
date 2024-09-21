#!/bin/bash
#SBATCH -J ExpWFClover
#SBATCH -o %x-%j.out
#SBATCH -t 00:29:00
#SBATCH -q debug
#SBATCH -C cpu
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=1

# run by tightly coupled way
DATADIR=/pscratch/sd/z/zw241/zw241/VisPerfStudy/dataset/cloverleaf_multistep_decomp
RUNDIR=/pscratch/sd/z/zw241/zw241/VisPerfStudy/Results/VisPerfExp_wf_clover_${1}
CURRDIR=$(pwd)
SIMSLEEP=5

mkdir -p $RUNDIR

cd $RUNDIR

ln -s $CURRDIR/../install/visReader/looselyworkflow/looselyinsitu looselyinsitu
ln -s $CURRDIR/../install/visReader/looselyworkflow/tightlyinsitu_pa tightlyinsitu_pa
ln -s $CURRDIR/../install/visReader/looselyworkflow/tightlyinsitu_we tightlyinsitu_we

mkdir tightinsitu

srun -N 4 -n 128 --mem-per-cpu=10G ../tightlyinsitu_pa \
--vtkm-device serial \
${DATADIR} \
${SIMSLEEP} &> tightinsitu.log


# run by loosely coupled way with rrb


# run by loosley coupled way with tracing+block assignment


# run by loosley couled way with estimation + block assignment


# run by loosley coupled way with estimation per two cycle + block assigment