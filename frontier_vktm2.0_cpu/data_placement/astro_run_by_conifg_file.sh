#!/bin/bash
#SBATCH -A csc143
#SBATCH -J RunAstroDiffConfigs
#SBATCH -o %x-%j.out
#SBATCH -t 01:30:00
#SBATCH -p batch
#SBATCH -N 1

# it needs around 20 mins to complete the execution for whole execution (execution takes long time)
DATADIR=/lustre/orion/scratch/zw241/csc143/VisPerfData/resample2
RUNDIR=/lustre/orion/scratch/zw241/csc143/VisPerfExpAssignStrategeis
CURRDIR=$(pwd)

mkdir $RUNDIR

cd $RUNDIR

cp $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI StreamlineMPI
cp $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI2 StreamlineMPI2

# init parameters
STEPSIZE_ASTRO=0.005000

MAXSTEPS=2000
NUM_SIM_POINTS_PER_DOM=1000

NUM_TEST_POINTS=50
NXYZ=4
WIDTH_PCT_LIST=0.1

echo "NUM_TEST_POINTS:"$NUM_TEST_POINTS
echo "NXYZ:"$NXYZ
echo "WIDTH_PCT:"$WIDTH_PCT

# Step 1 run with one block per rank
NUM_NODE=1
# the total blocks should same with the total number of ranks
NUM_RANK=32
NUM_BLOCKS=32

DATA_NAME=astro.2_4_4.visit

srun -N $NUM_NODE -n $NUM_RANK ../visitReaderAdev \
--vtkm-device serial \
--file=$DATADIR/${DATA_NAME} \
--advect-num-steps=$MAXSTEPS \
--advect-num-seeds=$NUM_SIM_POINTS_PER_DOM \
--seeding-method=domainrandom \
--advect-seed-box-extents=0.010000,0.990000,0.010000,0.990000,0.010000,0.990000 \
--field-name=velocity \
--advect-step-size=$STEPSIZE_ASTRO \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=roundroubin \
--communication=async_probe &> readerlog.out


# Step 2 run with workload estimator
log_suffix=_r${NUM_RANK}_tp${NUM_TEST_POINTS}_nxyz${NXYZ}_pc${WIDTH_PCT}.log
srun -N $NUM_NODE -n $NUM_RANK ./StreamlineMPI2 $DATADIR/${DATA_NAME} velocity $STEPSIZE_ASTRO $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ &> sl2_estimate_astro${log_suffix}


# Step 3 run through rrb based on workload estimator results
# generate the rrb file firstly, replace the assign_options.config
NUM_RANK=8
python3 $CURRDIR/generate_assignment_rrb.py $NUM_BLOCKS $NUM_RANK
# the configuration is the rrb now
srun -N $NUM_NODE -n $NUM_RANK ../visitReaderAdev \
--vtkm-device serial \
--file=$DATADIR/astro.2_4_4.visit \
--advect-num-steps=$MAXSTEPS \
--advect-num-seeds=$NUM_SIM_POINTS_PER_DOM \
--seeding-method=domainrandom \
--advect-seed-box-extents=0.010000,0.990000,0.010000,0.990000,0.010000,0.990000 \
--field-name=velocity \
--advect-step-size=$STEPSIZE_ASTRO \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=file \
--communication=async_probe &> rrb_readerlog.out

# Step 4 run through first fit backpacking based on workload estimator results
# generate the backpacking file, replace the assign config file
python3 $CURRDIR/generate_assignment_we_bpacking.py sl2_estimate_astro${log_suffix} $NUM_BLOCKS $NUM_RANK
# the configuration file is now updated into a new one now
# run the program
srun -N $NUM_NODE -n $NUM_RANK ../visitReaderAdev \
--vtkm-device serial \
--file=$DATADIR/astro.2_4_4.visit \
--advect-num-steps=$MAXSTEPS \
--advect-num-seeds=$NUM_SIM_POINTS_PER_DOM \
--seeding-method=domainrandom \
--advect-seed-box-extents=0.010000,0.990000,0.010000,0.990000,0.010000,0.990000 \
--field-name=velocity \
--advect-step-size=$STEPSIZE_ASTRO \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=file \
--communication=async_probe &> bpacking_readerlog.out
