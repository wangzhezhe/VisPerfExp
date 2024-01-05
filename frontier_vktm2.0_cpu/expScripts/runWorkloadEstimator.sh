#!/bin/bash
#SBATCH -A csc143
#SBATCH -J RunWorkloadEstimator
#SBATCH -o %x-%j.out
#SBATCH -t 01:30:00
#SBATCH -p batch
#SBATCH -N 2

DATADIR=/lustre/orion/scratch/zw241/csc331/VisPerfData/resample2
RUNDIR=/lustre/orion/scratch/zw241/csc331/VisPerfExp
CURRDIR=$(pwd)

mkdir $RUNDIR

cd $RUNDIR

cp $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI StreamlineMPI

# <executable> <visitfileName> <fieldNm> <stepSize> <maxSteps> <NUM_TEST_POINTS> <NUM_SIM_POINTS_PER_DOM> <Nxyz> <WIDTH_PCT>

STEPSIZE_SYN=0.0005000
STEPSIZE_FUSION=0.005
STEPSIZE_ASTRO=0.005000
STEPSIZE_FISH=0.001
STEPSIZE_CLOVER=0.05

MAXSTEPS=2000
NUM_TEST_POINTS_LIST="100 1000"
NUM_SIM_POINTS_PER_DOM=5000
NXYZ=2
WIDTH_PCT=0.1

for NUM_TEST_POINTS in ${NUM_TEST_POINTS_LIST}
do
echo "NUM_TEST_POINTS:"$NUM_TEST_POINTS
#astro data
srun -N 1 -n 8 ./StreamlineMPI $DATADIR/astro.2_2_2.visit velocity $STEPSIZE_ASTRO $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_astro_r8_tp${NUM_TEST_POINTS}.log

srun -N 1 -n 16 ./StreamlineMPI $DATADIR/astro.2_2_4.visit velocity $STEPSIZE_ASTRO $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_astro_r16_tp${NUM_TEST_POINTS}.log

srun -N 1 -n 32 ./StreamlineMPI $DATADIR/astro.2_4_4.visit velocity $STEPSIZE_ASTRO $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_astro_r32_tp${NUM_TEST_POINTS}.log

#srun -N 2 -n 64 ./StreamlineMPI $DATADIR/astro.4_4_4.visit velocity $STEPSIZE_ASTRO $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_astro_r64_tp${NUM_TEST_POINTS}.log

#clover data
srun -N 1 -n 8 ./StreamlineMPI $DATADIR/clover.2_2_2.visit velocity $STEPSIZE_CLOVER $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_clover_r8_tp${NUM_TEST_POINTS}.log

srun -N 1 -n 16 ./StreamlineMPI $DATADIR/clover.2_2_4.visit velocity $STEPSIZE_CLOVER $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_clover_r16_tp${NUM_TEST_POINTS}.log

srun -N 1 -n 32 ./StreamlineMPI $DATADIR/clover.2_4_4.visit velocity $STEPSIZE_CLOVER $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_clover_r32_tp${NUM_TEST_POINTS}.log

#srun -N 2 -n 64 ./StreamlineMPI $DATADIR/clover.4_4_4.visit velocity $STEPSIZE_CLOVER $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_clover_r64_tp${NUM_TEST_POINTS}.log


# fusion data
srun -N 1 -n 8 ./StreamlineMPI $DATADIR/fusion.2_2_2.visit velocity $STEPSIZE_FUSION $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_fusion_r8_tp${NUM_TEST_POINTS}.log

srun -N 1 -n 16 ./StreamlineMPI $DATADIR/fusion.2_2_4.visit velocity $STEPSIZE_FUSION $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_fusion_r16_tp${NUM_TEST_POINTS}.log

srun -N 1 -n 32 ./StreamlineMPI $DATADIR/fusion.2_4_4.visit velocity $STEPSIZE_FUSION $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_fusion_r32_tp${NUM_TEST_POINTS}.log

#srun -N 2 -n 64 ./StreamlineMPI $DATADIR/fusion.4_4_4.visit velocity $STEPSIZE_FUSION $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_fusion_r64_tp${NUM_TEST_POINTS}.log

# syn data
srun -N 1 -n 8 ./StreamlineMPI $DATADIR/syn.2_2_2.visit velocity $STEPSIZE_SYN $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_syn_r8_tp${NUM_TEST_POINTS}.log

srun -N 1 -n 16 ./StreamlineMPI $DATADIR/syn.2_2_4.visit velocity $STEPSIZE_SYN $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_syn_r16_tp${NUM_TEST_POINTS}.log

srun -N 1 -n 32 ./StreamlineMPI $DATADIR/syn.2_4_4.visit velocity $STEPSIZE_SYN $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_syn_r32_tp${NUM_TEST_POINTS}.log

#srun -N 2 -n 64 ./StreamlineMPI $DATADIR/syn.4_4_4.visit velocity $STEPSIZE_SYN $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_syn_r64_tp${NUM_TEST_POINTS}.log


#fishtank data
srun -N 1 -n 8 ./StreamlineMPI $DATADIR/fishtank.2_2_2.visit velocity $STEPSIZE_FISH $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_fishtank_r8_tp${NUM_TEST_POINTS}.log

srun -N 1 -n 16 ./StreamlineMPI $DATADIR/fishtank.2_2_4.visit velocity $STEPSIZE_FISH $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_fishtank_r16_tp${NUM_TEST_POINTS}.log

srun -N 1 -n 32 ./StreamlineMPI $DATADIR/fishtank.2_4_4.visit velocity $STEPSIZE_FISH $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_fishtank_r32_tp${NUM_TEST_POINTS}.log

#srun -N 2 -n 64 ./StreamlineMPI $DATADIR/fishtank.4_4_4.visit velocity $STEPSIZE_FISH $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ $WIDTH_PCT &> estimate_fishtank_r64_tp${NUM_TEST_POINTS}.log

done

# create actual run
cp $CURRDIR/../install/visReader/visitReaderAdev visitReaderAdev

export OMP_NUM_THREADS=1

# go through astro data set
#RUN_INFO_LIST="8:astro.2_2_2.visit:1 16:astro.2_2_4.visit:1 32:astro.2_4_4.visit:1 64:astro.4_4_4.visit:2"
RUN_INFO_LIST="8:astro.2_2_2.visit:1 16:astro.2_2_4.visit:1 32:astro.2_4_4.visit:1"

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
--advect-step-size=$STEPSIZE_ASTRO \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=roundroubin \
--communication=async_probe &> readerlog.out
cd ..
done



# go through fusion data set
#RUN_INFO_LIST="8:fusion.2_2_2.visit:1 16:fusion.2_2_4.visit:1 32:fusion.2_4_4.visit:1 64:fusion.4_4_4.visit:2"
RUN_INFO_LIST="8:fusion.2_2_2.visit:1 16:fusion.2_2_4.visit:1 32:fusion.2_4_4.visit:1"

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
--advect-step-size=$STEPSIZE_FUSION \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=roundroubin \
--communication=async_probe &> readerlog.out
cd ..
done

# go through synthetic data set
#RUN_INFO_LIST="8:syn.2_2_2.visit:1 16:syn.2_2_4.visit:1 32:syn.2_4_4.visit:1 64:syn.4_4_4.visit:2"
RUN_INFO_LIST="8:syn.2_2_2.visit:1 16:syn.2_2_4.visit:1 32:syn.2_4_4.visit:1"

for INFO in ${RUN_INFO_LIST}
do
INFO_ARRAY=(${INFO//:/ })
NUM_RANK=${INFO_ARRAY[0]}
NAME_DATA=${INFO_ARRAY[1]}
NUM_NODE=${INFO_ARRAY[2]}

echo "Num of rank: ${NUM_RANK} Name of data: ${NAME_DATA} Numer of node: ${NUM_NODE}"

logdirname=actual_syn_$NUM_RANK
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
--advect-step-size=$STEPSIZE_SYN \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=roundroubin \
--communication=async_probe &> readerlog.out
cd ..
done


# go through clover data
#RUN_INFO_LIST="8:clover.2_2_2.visit:1 16:clover.2_2_4.visit:1 32:clover.2_4_4.visit:1 64:clover.4_4_4.visit:2"
RUN_INFO_LIST="8:clover.2_2_2.visit:1 16:clover.2_2_4.visit:1 32:clover.2_4_4.visit:1"

for INFO in ${RUN_INFO_LIST}
do
INFO_ARRAY=(${INFO//:/ })
NUM_RANK=${INFO_ARRAY[0]}
NAME_DATA=${INFO_ARRAY[1]}
NUM_NODE=${INFO_ARRAY[2]}

echo "Num of rank: ${NUM_RANK} Name of data: ${NAME_DATA} Numer of node: ${NUM_NODE}"

logdirname=actual_clover_$NUM_RANK
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
--advect-step-size=$STEPSIZE_CLOVER \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=roundroubin \
--communication=async_probe &> readerlog.out
cd ..
done


# go through fishtank data
#RUN_INFO_LIST="8:fishtank.2_2_2.visit:1 16:fishtank.2_2_4.visit:1 32:fishtank.2_4_4.visit:1 64:fishtank.4_4_4.visit:2"
RUN_INFO_LIST="8:fishtank.2_2_2.visit:1 16:fishtank.2_2_4.visit:1 32:fishtank.2_4_4.visit:1"

for INFO in ${RUN_INFO_LIST}
do
INFO_ARRAY=(${INFO//:/ })
NUM_RANK=${INFO_ARRAY[0]}
NAME_DATA=${INFO_ARRAY[1]}
NUM_NODE=${INFO_ARRAY[2]}

echo "Num of rank: ${NUM_RANK} Name of data: ${NAME_DATA} Numer of node: ${NUM_NODE}"

logdirname=actual_fishtank_$NUM_RANK
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
--advect-step-size=$STEPSIZE_FISH \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=roundroubin \
--communication=async_probe &> readerlog.out
cd ..
done
