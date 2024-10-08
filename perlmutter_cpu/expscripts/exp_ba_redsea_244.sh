#!/bin/bash
#SBATCH -J ExpBARedSea
#SBATCH -o %x-%j.out
#SBATCH -t 00:29:00
#SBATCH -q debug
#SBATCH -C cpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=1

# load necessary module
module load python/3.9-anaconda-2021.11

# This script using the results from workload estimation to generate the block assignment plan

DATADIR=/pscratch/sd/z/zw241/zw241/VisPerfStudy/dataset/redsea
RUNDIR=/pscratch/sd/z/zw241/zw241/VisPerfStudy/Results/VisPerfExp_ba_redsea_32_244_${1}
CURRDIR=$(pwd)

mkdir -p $RUNDIR

cd $RUNDIR

ln -s $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI StreamlineMPI
ln -s $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI2 StreamlineMPI2
ln -s $CURRDIR/../install/visReader/visitReaderAdev visitReaderAdev

# init parameters
STEPSIZE_REDSEA=0.1

MAXSTEPS=2000
NUM_SIM_POINTS_PER_DOM=1000

# Step 1 run with one block per rank
NUM_NODE=1
# the total blocks should same with the total number of ranks
NUM_RANK=32
NUM_BLOCKS=32

mkdir one_data_per_rank
cd one_data_per_rank

# define a function to execute on redsea data
# first one is dataset and second one is execution index
call_adv () {
echo "number of node ${1} number of ranks ${2}"
echo "executing redsea on dataset ${3} execution index is ${4} strategy ${5}"
srun -N ${1} -n ${2} --mem-per-cpu=8G ../visitReaderAdev \
--vtkm-device serial \
--file=$DATADIR/${3} \
--advect-num-steps=$MAXSTEPS \
--advect-num-seeds=$NUM_SIM_POINTS_PER_DOM \
--seeding-method=domainrandom \
--advect-seed-box-extents=0.010000,498.9,0.010000,498.9,0.010000,49.9 \
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
DATA_NAME=redsea_c0.4_4_2.128_128_128.visit
call_adv $NUM_NODE $NUM_RANK $DATA_NAME 0 roundroubin

# go back to the parent dir
cd ..


# Step 2 run through rrb 
# generate the rrb file firstly, replace the assign_options.config
mkdir rrb_placement
cd rrb_placement
NUM_RANK_REDUCED=8
python3 $CURRDIR/generate_assignment_rrb.py $NUM_BLOCKS $NUM_RANK_REDUCED
sleep 1
# the configuration is the rrb now
for run_index in {1..3}
do
call_adv $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
cd ..


# Step 3 run through first fit backpacking based on workload popularity from actual run log
mkdir bpacking_placement_one_stage
cd bpacking_placement_one_stage

# parsing original run results
# using the results in parser log to generate assignment plan

python3 $CURRDIR/parser_compare_actual_run.py $RUNDIR/one_data_per_rank ${NUM_RANK} 1
python3 $CURRDIR/generate_assignment_actual_bpacking_dup_capacity_vector.py $NUM_BLOCKS $NUM_RANK_REDUCED ./adv_step_stages_list.json

sleep 1
for run_index in {1..3}
do
call_adv $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
# go back to parent dir
cd ..

# Step 4 actual data, back packing and duplication
mkdir bpacking_placement_two_stages
cd bpacking_placement_two_stages

python3 $CURRDIR/parser_compare_actual_run.py $RUNDIR/one_data_per_rank ${NUM_RANK} 2
python3 $CURRDIR/generate_assignment_actual_bpacking_dup_capacity_vector.py $NUM_BLOCKS $NUM_RANK_REDUCED ./adv_step_stages_list.json
sleep 1
for run_index in {1..3}
do
call_adv $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
# go back to parent dir
cd ..

# Step 5 actual data, back packing, two stages
mkdir bpacking_placement_three_stages
cd bpacking_placement_three_stages

python3 $CURRDIR/parser_compare_actual_run.py $RUNDIR/one_data_per_rank ${NUM_RANK} 3
python3 $CURRDIR/generate_assignment_actual_bpacking_dup_capacity_vector.py $NUM_BLOCKS $NUM_RANK_REDUCED ./adv_step_stages_list.json

sleep 1
for run_index in {1..3}
do
call_adv $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
# go back to parent dir
cd ..
