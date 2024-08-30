#!/bin/bash
#SBATCH -J ExpBAWEClover
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

DATADIR=/pscratch/sd/z/zw241/zw241/VisPerfStudy/dataset/clover
RUNDIR=/pscratch/sd/z/zw241/zw241/VisPerfStudy/Results/VisPerfExp_ba_we_clover_32_244_${1}
CURRDIR=$(pwd)

mkdir -p $RUNDIR

cd $RUNDIR

ln -s $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI StreamlineMPI
ln -s $CURRDIR/../install/visReader/workloadEstimation/StreamlineMPI2 StreamlineMPI2
ln -s $CURRDIR/../install/visReader/visitReaderAdev visitReaderAdev

# init parameters
STEPSIZE_CLOVER=0.001

MAXSTEPS=2000
NUM_SIM_POINTS_PER_DOM=1000

NUM_NODE=1
# the total blocks should same with the total number of ranks
NUM_RANK=32
NUM_BLOCKS=32
NUM_RANK_REDUCED=8

DATA_NAME=fb_clover_0.2_4_4.128_128_128.visit

# define a function to execute on clover data
# first one is dataset and second one is execution index
call_adv () {
echo "number of node ${1} number of ranks ${2}"
echo "executing particle advection on dataset ${3} execution index is ${4} strategy ${5}"
srun -N ${1} -n ${2} --mem-per-cpu=10G ../visitReaderAdev \
--vtkm-device serial \
--file=$DATADIR/${3} \
--advect-num-steps=$MAXSTEPS \
--advect-num-seeds=$NUM_SIM_POINTS_PER_DOM \
--seeding-method=domainrandom \
--advect-seed-box-extents=0.010000,0.990000,0.010000,0.990000,0.010000,0.990000 \
--field-name=velocity \
--advect-step-size=$STEPSIZE_CLOVER \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=${5} \
--block-manual-id=true \
--communication=async_probe &> readerlog_${4}.out
}

# Step 1 run through rrb 
# generate the rrb file firstly, replace the assign_options.config
mkdir rrb_placement
cd rrb_placement

python3 $CURRDIR/generate_assignment_rrb.py $NUM_BLOCKS $NUM_RANK_REDUCED
sleep 1
# the configuration is the rrb now
for run_index in {1..3}
do
call_adv $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
cd ..


mkdir we_multi_stages 
cd we_multi_stages

export OMP_NUM_THREADS=1
NUM_TEST_POINTS=50
NXYZ=2
WIDTH_PCT=0.1

# there are three stages
srun -N $NUM_NODE -n $NUM_RANK ../StreamlineMPI2 $DATADIR/${DATA_NAME} velocity $STEPSIZE_CLOVER $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ true &> ./we_adv_3.log

# only one stage
srun -N $NUM_NODE -n $NUM_RANK ../StreamlineMPI2 $DATADIR/${DATA_NAME} velocity $STEPSIZE_CLOVER $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ false &> ./we_adv_1.log

cd ..

# Step 2 estimation data, bpcaking one stage
mkdir bpacking_placement_one_stage
cd bpacking_placement_one_stage

#python3 $CURRDIR/parser_compare_actual_run.py $RUNDIR/one_data_per_rank ${NUM_RANK} 3
python3 $CURRDIR/parser_estimation_run.py $RUNDIR/we_multi_stages/we_adv_1.log ${NUM_RANK} 1
sleep 1
python3 $CURRDIR/generate_assignment_actual_bpacking_dup_capacity_vector.py $NUM_BLOCKS $NUM_RANK_REDUCED ./adv_step_stages_list.json

sleep 1
for run_index in {1..3}
do
call_adv $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done

# go back to parent dir
cd ..


# Step 3 estimation data, back packing, three stages
mkdir bpacking_placement_three_stages
cd bpacking_placement_three_stages

#python3 $CURRDIR/parser_compare_actual_run.py $RUNDIR/one_data_per_rank ${NUM_RANK} 3
python3 $CURRDIR/parser_estimation_run.py $RUNDIR/we_multi_stages/we_adv_3.log ${NUM_RANK} 3
sleep 1


python3 $CURRDIR/generate_assignment_actual_bpacking_dup_capacity_vector.py $NUM_BLOCKS $NUM_RANK_REDUCED ./adv_step_stages_list.json 

sleep 5
for run_index in {1..3}
do
call_adv $NUM_NODE $NUM_RANK_REDUCED $DATA_NAME $run_index file
done
# go back to parent dir
cd ..
