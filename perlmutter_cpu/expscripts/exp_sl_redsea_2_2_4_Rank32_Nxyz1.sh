#!/bin/bash
#SBATCH -J ExpSlRedsea
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
RUNDIR=/pscratch/sd/z/zw241/zw241/VisPerfStudy/Results/VisPerfExpSl2_Redsea224_Rank32_Nxyz1_${1}
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

NUM_TEST_POINTS=50
NXYZ=1
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
echo "executing redsea on dataset ${3} execution index is ${4} strategy ${5}"
srun -N ${1} -n ${2} --mem-per-cpu=1G ../visitReaderAdev \
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

#executing the complete work
DATA_NAME=redsea_c0.4_4_2.128_128_128.visit
call_redsea $NUM_NODE $NUM_RANK $DATA_NAME 0 roundroubin

# go back to the parent dir
cd ..

# Step 2 run with workload estimator
log_suffix=_r${NUM_RANK}_tp${NUM_TEST_POINTS}_nxyz${NXYZ}_pc${WIDTH_PCT}.log
estimate_log_file_1=sl2_estimate_redsea_1thread_${log_suffix}
estimate_log_file_32=sl2_estimate_redsea_32thread_${log_suffix}

parser_log=parser_log.log

export OMP_NUM_THREADS=1
srun -N $NUM_NODE -n $NUM_RANK ./StreamlineMPI2 $DATADIR/${DATA_NAME} velocity $STEPSIZE_REDSEA $MAXSTEPS $NUM_TEST_POINTS $NUM_SIM_POINTS_PER_DOM $NXYZ &> ${estimate_log_file_1}


# compare estimation run with the actual run resutls
python3 $CURRDIR/parser_compare_actual_and_estimation_run.py $RUNDIR/one_data_per_rank $RUNDIR/${estimate_log_file_1} ${NUM_RANK} &> ${parser_log}
