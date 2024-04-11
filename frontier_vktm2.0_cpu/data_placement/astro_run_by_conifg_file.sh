#!/bin/bash
#SBATCH -A csc143
#SBATCH -J RunAstroDiffConfigs
#SBATCH -o %x-%j.out
#SBATCH -t 01:30:00
#SBATCH -p batch
#SBATCH -N 1

# This script using the results from workload estimation to generate the block assignment plan

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
echo "number of node ${1} number of ranks ${2}"
echo "executing astro on dataset ${3} execution index is ${4} strategy ${5}"
srun -N ${1} -n ${2} ../visitReaderAdev \
--vtkm-device serial \
--file=$DATADIR/${3} \
--advect-num-steps=$MAXSTEPS \
--advect-num-seeds=$NUM_SIM_POINTS_PER_DOM \
--seeding-method=domainrandom \
--advect-seed-box-extents=0.010000,0.990000,0.010000,0.990000,0.010000,0.990000 \
--field-name=velocity \
--advect-step-size=$STEPSIZE_ASTRO \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=${5} \
--block-manual-id=true \
--communication=async_probe &> readerlog_${4}.out
}

#executing the work
DATA_NAME=astro.2_4_4.visit
call_astro $NUM_NODE $NUM_RANK $DATA_NAME 0 roundroubin

# go back to the parent dir
cd ..

# Step 2 run with workload estimator
log_suffix=_r${NUM_RANK}_tp${NUM_TEST_POINTS}_nxyz${NXYZ}_pc${WIDTH_PCT}.log
estimate_log_file=sl2_estimate_astro${log_suffix}
srun -N $NUM_NODE -n $NUM_RANK ./StreamlineMPI2 $DATADIR/${DATA_NAME} velocity $STEPSIZE_ASTRO $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ &> ${estimate_log_file}

# Step 3
# parsing workload estimation results
# parsing original run resutls
# comparing the differences between these two
python3 $CURRDIR/parser_compare_actual_and_estimation_run.py $RUNDIR/one_data_per_rank $RUNDIR/${estimate_log_file} ${NUM_RANK} &> parser.log


# Step 4 run through rrb based on workload estimator results
# generate the rrb file firstly, replace the assign_options.config
mkdir rrb_placement
cd rrb_placement
NUM_RANK_REDUCED=8
python3 $CURRDIR/generate_assignment_rrb.py $NUM_BLOCKS $NUM_RANK_REDUCED
# the configuration is the rrb now
for run_index in {1..3}
do

call_astro $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file

done


# Step 5 run through first fit backpacking based on workload popularity from actual run log



# Step 5 run through first fit backpacking based on workload estimator results
cd ..
mkdir bpacking_placement
cd bpacking_placement
# generate the backpacking file, replace the assign config file
python3 $CURRDIR/generate_assignment_we_bpacking.py ../${estimate_log_file} $NUM_BLOCKS $NUM_RANK_REDUCED

# the configuration file is now updated into a new one now
sleep 1
# run the program
# run it three times
# keep the log for last time

for run_index in {1..3}
do
call_astro $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done


# Step 6 run through first fit backpacking with duplication based on workload estimator results
cd ..
mkdir bpacking_placement_dup
cd bpacking_placement_dup
# generate the backpacking file, replace the assign config file
python3 $CURRDIR/generate_assignment_we_bpacking_dup.py ../${estimate_log_file} $NUM_BLOCKS $NUM_RANK_REDUCED
sleep 1
# the configuration file is now updated into a new one now
# run the program
# run it three times
# keep the log for last time

for run_index in {1..3}
do
# setting block duplication as true
# and setting SetBlockIDs manually
call_astro $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file

done

