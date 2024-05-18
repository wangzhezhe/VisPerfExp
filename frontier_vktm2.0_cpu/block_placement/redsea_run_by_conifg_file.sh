#!/bin/bash
#SBATCH -A csc143
#SBATCH -J RunRedSea
#SBATCH -o %x-%j.out
#SBATCH -t 01:30:00
#SBATCH -p batch
#SBATCH -N 1

# This script using the results from workload estimation to generate the block assignment plan

DATADIR=/lustre/orion/scratch/zw241/csc143/VisPerfData/RedSeaDecomposition
RUNDIR=/lustre/orion/scratch/zw241/csc143/VisPerfExpAssignStrategeis_RedSea_${1}
CURRDIR=$(pwd)

mkdir $RUNDIR

cd $RUNDIR

ln -s $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI StreamlineMPI
ln -s $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI2 StreamlineMPI2
ln -s $CURRDIR/../install/visReader/visitReaderAdev visitReaderAdev

# init parameters
STEPSIZE_REDSEA=0.1

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

# define a function to execute on redsea data
# first one is dataset and second one is execution index
call_redsea () {
echo "number of node ${1} number of ranks ${2}"
echo "executing streamline on dataset ${3} execution index is ${4} strategy ${5}"
srun -N ${1} -n ${2} ../visitReaderAdev \
--vtkm-device serial \
--file=$DATADIR/${3} \
--advect-num-steps=$MAXSTEPS \
--advect-num-seeds=$NUM_SIM_POINTS_PER_DOM \
--seeding-method=domainrandom \
--advect-seed-box-extents=0.010000,498.99,0.010000,498.99,0.010000,98.99 \
--field-name=velocity \
--advect-step-size=$STEPSIZE_REDSEA \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=${5} \
--block-manual-id=true \
--communication=async_probe &> readerlog_${4}.out
}

#executing the work
DATA_NAME=fb_RedSea0001.4_4_2.128_128_64.visit
call_redsea $NUM_NODE $NUM_RANK $DATA_NAME 0 roundroubin

# go back to the parent dir
cd ..

# Step 2 run with workload estimator
log_suffix=_r${NUM_RANK}_tp${NUM_TEST_POINTS}_nxyz${NXYZ}_pc${WIDTH_PCT}.log
estimate_log_file=sl2_estimate_redsea${log_suffix}
parser_log=parser_log.log

srun -N $NUM_NODE -n $NUM_RANK ./StreamlineMPI2 $DATADIR/${DATA_NAME} velocity $STEPSIZE_REDSEA $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ &> ${estimate_log_file}

# compare estimation run with the actual run resutls
python3 $CURRDIR/parser_compare_actual_and_estimation_run.py $RUNDIR/one_data_per_rank $RUNDIR/${estimate_log_file} ${NUM_RANK} &> ${parser_log}

# Step 3 run through rrb based on workload estimator results
# generate the rrb file firstly, replace the assign_options.config
mkdir rrb_placement
cd rrb_placement
NUM_RANK_REDUCED=8
python3 $CURRDIR/generate_assignment_rrb.py $NUM_BLOCKS $NUM_RANK_REDUCED
sleep 1
# the configuration is the rrb now
for run_index in {1..3}
do
call_redsea $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
cd ..

# Step 4 run through first fit backpacking based on workload popularity from actual run log
mkdir bpacking_placement_actual_log
cd bpacking_placement_actual_log

# parsing original run results
# using the results in parser log to generate assignment plan
python3 $CURRDIR/generate_assignment_actual_bpacking.py ../${parser_log} $NUM_BLOCKS $NUM_RANK_REDUCED
sleep 1
for run_index in {1..3}
do
call_redsea $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
# go back to parent dir
cd ..

# Step 5 actual data, back packing and duplication
mkdir bpacking_dup_placement_actual_log
cd bpacking_dup_placement_actual_log

python3 $CURRDIR/generate_assignment_actual_bpacking_dup.py ../${parser_log} $NUM_BLOCKS $NUM_RANK_REDUCED
sleep 1
for run_index in {1..3}
do
call_redsea $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
# go back to parent dir
cd ..

# Step 6 actual data, back packing, two stages
mkdir bpacking_dup_two_stages_actual_log
cd bpacking_dup_two_stages_actual_log
python3 $CURRDIR/generate_assignment_actual_bpacking_dup_stages2.py $RUNDIR $NUM_BLOCKS $NUM_BLOCKS $NUM_RANK_REDUCED 10 ../${parser_log}
sleep 1
for run_index in {1..3}
do
call_redsea $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
# go back to parent dir
cd ..

# #------using workload estimation data------
# # Step 6 run through first fit backpacking based on workload estimator results
# cd ..
# mkdir bpacking_placement
# cd bpacking_placement
# # generate the backpacking file, replace the assign config file
# python3 $CURRDIR/generate_assignment_we_bpacking.py ../${estimate_log_file} $NUM_BLOCKS $NUM_RANK_REDUCED

# # the configuration file is now updated into a new one now
# sleep 1
# # run the program
# # run it three times
# # keep the log for last time

# for run_index in {1..3}
# do
# call_redsea $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
# done


# # Step 7 run through first fit backpacking with duplication based on workload estimator results
# cd ..
# mkdir bpacking_placement_dup
# cd bpacking_placement_dup
# # generate the backpacking file, replace the assign config file
# python3 $CURRDIR/generate_assignment_we_bpacking_dup.py ../${estimate_log_file} $NUM_BLOCKS $NUM_RANK_REDUCED
# sleep 1
# # the configuration file is now updated into a new one now
# # run the program
# # run it three times
# # keep the log for last time

# for run_index in {1..3}
# do
# # setting block duplication as true
# # and setting SetBlockIDs manually
# call_redsea $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file

# done

