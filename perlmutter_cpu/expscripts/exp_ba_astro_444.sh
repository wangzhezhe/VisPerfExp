#!/bin/bash
#SBATCH -J ExpBAAstro
#SBATCH -o %x-%j.out
#SBATCH -t 00:29:00
#SBATCH -q debug
#SBATCH -C cpu
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=1

# load necessary module
module load python/3.9-anaconda-2021.11

# This script using the results from workload estimation to generate the block assignment plan

DATADIR=/pscratch/sd/z/zw241/zw241/VisPerfStudy/dataset/astro
RUNDIR=/pscratch/sd/z/zw241/zw241/VisPerfStudy/Results/VisPerfExp_ba_astro_64_444_${1}
CURRDIR=$(pwd)

mkdir -p $RUNDIR

cd $RUNDIR

ln -s $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI StreamlineMPI
ln -s $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI2 StreamlineMPI2
ln -s $CURRDIR/../install/visReader/visitReaderAdev visitReaderAdev

# init parameters
STEPSIZE_ASTRO=0.005000

MAXSTEPS=2000
NUM_SIM_POINTS_PER_DOM=1000

# Step 1 run with one block per rank
NUM_NODE=2
# the total blocks should same with the total number of ranks
NUM_RANK=64
NUM_BLOCKS=64

mkdir one_data_per_rank
cd one_data_per_rank

# define a function to execute on astro data
# first one is dataset and second one is execution index
call_astro () {
echo "number of node ${1} number of ranks ${2}"
echo "executing astro on dataset ${3} execution index is ${4} strategy ${5}"
srun -N ${1} -n ${2} --mem-per-cpu=1G ../visitReaderAdev \
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
DATA_NAME=fb_astro_origin_0.4_4_4.128_128_128.visit
call_astro $NUM_NODE $NUM_RANK $DATA_NAME 0 roundroubin

# go back to the parent dir
cd ..


parser_log=parser.log

python3 $CURRDIR/parser_compare_actual_run.py $RUNDIR/one_data_per_rank ${NUM_RANK} &> ${parser_log}

# Step 2 run through rrb 
# generate the rrb file firstly, replace the assign_options.config
mkdir rrb_placement
cd rrb_placement

# there is memory issue using 8 ranks
NUM_RANK_REDUCED=16
python3 $CURRDIR/generate_assignment_rrb.py $NUM_BLOCKS $NUM_RANK_REDUCED
sleep 1
# the configuration is the rrb now
for run_index in {1..3}
do
call_astro $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
cd ..

# get the actual workload time


# Step 3 run through first fit backpacking based on workload popularity from actual run log
mkdir bpacking_placement_actual_log
cd bpacking_placement_actual_log

# parsing original run results
# using the results in parser log to generate assignment plan

python3 $CURRDIR/generate_assignment_actual_bpacking.py ../${parser_log} $NUM_BLOCKS $NUM_RANK_REDUCED
sleep 1
for run_index in {1..3}
do
call_astro $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
# go back to parent dir
cd ..

# Step 4 actual data, back packing and duplication
mkdir bpacking_dup_placement_actual_log
cd bpacking_dup_placement_actual_log

python3 $CURRDIR/generate_assignment_actual_bpacking_dup.py ../${parser_log} $NUM_BLOCKS $NUM_RANK_REDUCED
sleep 1
for run_index in {1..3}
do
call_astro $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
# go back to parent dir
cd ..

# Step 5 actual data, back packing, two stages
mkdir bpacking_dup_two_stages_actual_log
cd bpacking_dup_two_stages_actual_log
python3 $CURRDIR/generate_assignment_actual_bpacking_dup_stages2.py $RUNDIR $NUM_BLOCKS $NUM_BLOCKS $NUM_RANK_REDUCED 10 ../${parser_log}
sleep 1
for run_index in {1..3}
do
call_astro $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
# go back to parent dir
cd ..

