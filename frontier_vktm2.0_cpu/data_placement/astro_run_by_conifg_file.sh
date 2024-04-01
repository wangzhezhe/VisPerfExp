#!/bin/bash
#SBATCH -A csc143
#SBATCH -J RunAstroDiffConfigs
#SBATCH -o %x-%j.out
#SBATCH -t 01:30:00
#SBATCH -p batch
#SBATCH -N 1

# it needs around 20 mins to complete the execution for whole execution (execution takes long time)
DATADIR=/lustre/orion/scratch/zw241/csc143/VisPerfData/resample2
RUNDIR=/lustre/orion/scratch/zw241/csc143/VisPerfExpAssignStrategeis_${1}
CURRDIR=$(pwd)

mkdir $RUNDIR

cd $RUNDIR

ln -s $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI StreamlineMPI
ln -s $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI2 StreamlineMPI2
ln -s $CURRDIR/../install/visReader/visitReaderAdev visitReaderAdev

# init parameters
STEPSIZE_ASTRO=0.005000

MAXSTEPS=2000
NUM_SIM_POINTS_PER_DOM=1000

NUM_TEST_POINTS=50
NXYZ=4
WIDTH_PCT=0.1

echo "NUM_TEST_POINTS:"$NUM_TEST_POINTS
echo "NXYZ:"$NXYZ
echo "WIDTH_PCT:"$WIDTH_PCT

# Step 1 run with one block per rank
NUM_NODE=1
# the total blocks should same with the total number of ranks
NUM_RANK=32
NUM_BLOCKS=32

mkdir one_data_per_rank
cd one_data_per_rank

# define a function to execute on astro data
# first one is dataset and second one is execution index
call_astro () {
echo "executing astro on dataset ${1} execution index is ${2}"
srun -N $NUM_NODE -n $NUM_RANK ../visitReaderAdev \
--vtkm-device serial \
--file=$DATADIR/${1} \
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
--communication=async_probe &> readerlog_${2}.out
}

#executing the work
DATA_NAME=astro.2_4_4.visit
call_astro $DATA_NAME 0


# go back to the parend dir
cd ..

# Step 2 run with workload estimator
log_suffix=_r${NUM_RANK}_tp${NUM_TEST_POINTS}_nxyz${NXYZ}_pc${WIDTH_PCT}.log
estimate_log_file=sl2_estimate_astro${log_suffix}
srun -N $NUM_NODE -n $NUM_RANK ./StreamlineMPI2 $DATADIR/${DATA_NAME} velocity $STEPSIZE_ASTRO $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ &> ${estimate_log_file}


# Step 3 run through rrb based on workload estimator results
# generate the rrb file firstly, replace the assign_options.config
mkdir rrb_placement
cd rrb_placement
NUM_RANK_REDUCED=8
python3 $CURRDIR/generate_assignment_rrb.py $NUM_BLOCKS $NUM_RANK_REDUCED
# the configuration is the rrb now
for run_index in {1..3}
do

call_astro $DATA_NAME $run_index

done

# Step 4 run through first fit backpacking based on workload estimator results
cd ..
mkdir bpacking_placement
cd bpacking_placement
# generate the backpacking file, replace the assign config file
python3 $CURRDIR/generate_assignment_we_bpacking.py ../${estimate_log_file} $NUM_BLOCKS $NUM_RANK_REDUCED
# the configuration file is now updated into a new one now
# run the program
# run it three times
# keep the log for last time

for run_index in {1..3}
do
call_astro $DATA_NAME $run_index
done


# Step 5 run through first fit backpacking with duplication based on workload estimator results
cd ..
mkdir bpacking_placement_dup
cd bpacking_placement_dup
# generate the backpacking file, replace the assign config file
python3 $CURRDIR/generate_assignment_we_bpacking_dup.py ../${estimate_log_file} $NUM_BLOCKS $NUM_RANK_REDUCED
# the configuration file is now updated into a new one now
# run the program
# run it three times
# keep the log for last time

for run_index in {1..3}
do

call_astro $DATA_NAME $run_index

done

