#!/bin/bash
#SBATCH -A CSC331
#SBATCH -J RunWorkloadEstimator
#SBATCH -o %x-%j.out
#SBATCH -t 1:00:00
#SBATCH -p batch
#SBATCH -N 1

DATADIR=/lustre/orion/scratch/zw241/csc331/VisPerfData/resample2
RUNDIR=/lustre/orion/scratch/zw241/csc331/VisPerfExp
CURRDIR=$(pwd)

cd $RUNDIR

# create soft link
cp $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI StreamlineMPI

srun -N 1 -n 8 ./StreamlineMPI $DATADIR/astro.2_2_2.visit velocity &> astro_8.log

srun -N 1 -n 16 ./StreamlineMPI $DATADIR/astro.2_2_4.visit velocity &> astro_16.log

srun -N 1 -n 32 ./StreamlineMPI $DATADIR/astro.2_4_4.visit velocity &> astro_32.log

srun -N 1 -n 64 ./StreamlineMPI $DATADIR/astro.4_4_4.visit velocity &> astro_64.log


srun -N 1 -n 8 ./StreamlineMPI $DATADIR/fusion.2_2_2.visit velocity &> fusion_8.log

srun -N 1 -n 16 ./StreamlineMPI $DATADIR/fusion.2_2_4.visit velocity &> fusion_16.log

srun -N 1 -n 32 ./StreamlineMPI $DATADIR/fusion.2_4_4.visit velocity &> fusion_32.log

srun -N 1 -n 64 ./StreamlineMPI $DATADIR/fusion.4_4_4.visit velocity &> fusion_64.log

