#!/bin/bash
#SBATCH -A CSC331
#SBATCH -J RunWorkloadEstimator
#SBATCH -o %x-%j.out
#SBATCH -t 00:30:00
#SBATCH -p batch
#SBATCH -N 2

DATADIR=/lustre/orion/scratch/zw241/csc331/VisPerfData/resample2
RUNDIR=/lustre/orion/scratch/zw241/csc331/VisPerfExp
CURRDIR=$(pwd)

mkdir $RUNDIR

cd $RUNDIR

cp $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI StreamlineMPI


# <executable> <visitfileName> <fieldNm> <stepSize> <maxSteps> <NUM_TEST_POINTS> <NUM_SIM_POINTS_PER_DOM> <Nxyz>

STEPSIZE=0.005000
MAXSTEPS=2000
NUM_TEST_POINTS=10
NUM_SIM_POINTS_PER_DOM=100
NXYZ=2
# astro data
srun -N 1 -n 8 ./StreamlineMPI $DATADIR/astro.2_2_2.visit velocity $STEPSIZE $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ &> estimate_astro_8.log

srun -N 1 -n 16 ./StreamlineMPI $DATADIR/astro.2_2_4.visit velocity $STEPSIZE $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ &> estimate_astro_16.log

srun -N 1 -n 32 ./StreamlineMPI $DATADIR/astro.2_4_4.visit velocity $STEPSIZE $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ &> estimate_astro_32.log

srun -N 2 -n 64 ./StreamlineMPI $DATADIR/astro.4_4_4.visit velocity $STEPSIZE $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ &> estimate_astro_64.log

# fusion data
srun -N 1 -n 8 ./StreamlineMPI $DATADIR/fusion.2_2_2.visit velocity $STEPSIZE $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ &> estimate_fusion_8.log

srun -N 1 -n 16 ./StreamlineMPI $DATADIR/fusion.2_2_4.visit velocity $STEPSIZE $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ &> estimate_fusion_16.log

srun -N 1 -n 32 ./StreamlineMPI $DATADIR/fusion.2_4_4.visit velocity $STEPSIZE $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ &> estimate_fusion_32.log

srun -N 2 -n 64 ./StreamlineMPI $DATADIR/fusion.4_4_4.visit velocity $STEPSIZE $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ &> estimate_fusion_64.log

# create actual run
cp $CURRDIR/../install/visReader/visitReaderAdev visitReaderAdev

export OMP_NUM_THREADS=1

# go through astro data set
RUN_INFO_LIST="8:astro.2_2_2.visit:1 16:astro.2_2_4.visit:1 32:astro.2_4_4.visit:1 64:astro.4_4_4.visit:2"

for INFO in ${RUN_INFO_LIST}
do

INFO_ARRAY=(${INFO//:/ })
NUM_RANK=${INFO_ARRAY[0]}
NAME_DATA=${INFO_ARRAY[1]}
NUM_NODE=${INFO_ARRAY[2]}

echo "Num of rank: ${NUM_RANK} Name of data: ${NAME_DATA} Numer of node: ${NUM_NODE}"

logdirname=actual_astro_$NUM_RANK
rm -rf $logdirname
mkdir $logdirname
cd $logdirname

srun -N $NUM_NODE -n $NUM_RANK ../visitReaderAdev \
--vtkm-device serial \
--file=$DATADIR/$NAME_DATA \
--advect-num-steps=$MAXSTEPS \
--advect-num-seeds=5000 \
--seeding-method=domainrandom \
--advect-seed-box-extents=0.010000,0.990000,0.010000,0.990000,0.010000,0.990000 \
--field-name=velocity \
--advect-step-size=$STEPSIZE \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=roundroubin \
--communication=async_probe &> readerlog.out

cd ..

done


# go through fusion data set
RUN_INFO_LIST="8:fusion.2_2_2.visit:1 16:fusion.2_2_4.visit:1 32:fusion.2_4_4.visit:1 64:fusion.4_4_4.visit:2"

for INFO in ${RUN_INFO_LIST}
do

INFO_ARRAY=(${INFO//:/ })
NUM_RANK=${INFO_ARRAY[0]}
NAME_DATA=${INFO_ARRAY[1]}
NUM_NODE=${INFO_ARRAY[2]}

echo "Num of rank: ${NUM_RANK} Name of data: ${NAME_DATA} Numer of node: ${NUM_NODE}"

logdirname=actual_fusion_$NUM_RANK
rm -rf $logdirname
mkdir $logdirname
cd $logdirname

srun -N $NUM_NODE -n $NUM_RANK ../visitReaderAdev \
--vtkm-device serial \
--file=$DATADIR/$NAME_DATA \
--advect-num-steps=$MAXSTEPS \
--advect-num-seeds=5000 \
--seeding-method=domainrandom \
--advect-seed-box-extents=0.010000,0.990000,0.010000,0.990000,0.010000,0.990000 \
--field-name=velocity \
--advect-step-size=$STEPSIZE \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=roundroubin \
--communication=async_probe &> readerlog.out

cd ..

done
