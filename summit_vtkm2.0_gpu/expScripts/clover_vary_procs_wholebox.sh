#!/bin/bash
 
#BSUB -P csc143
#BSUB -W 01:59
#BSUB -nnodes 11

#BSUB -J clover_vary_procs_wholebox
#BSUB -o R_clover_vary_procs_wholebox.%J.out
#BSUB -e R_clover_vary_procs_wholebox.%J.err 

CURRDIR=$(pwd)

DATASET=/gpfs/alpine/proj-shared/csc143/zhewang/datasets/streamlineexp/x_cloverleafRaw_128_128_256.640.4_4_4.128_128_128.visit
DATA_DIRNAME=clover_vary_procs_wholebox/x_cloverleafRaw_128_128_256.640.4_4_4.128_128_128

mkdir -p $CURRDIR/$DATA_DIRNAME

cd $MEMBERWORK/csc143

rm -rf $DATA_DIRNAME
mkdir -p $DATA_DIRNAME
cd $DATA_DIRNAME

ln -s $CURRDIR/../install/visReader/visitReaderAdev visitReaderAdev

FIELD=velocity

NUMSTEPS=1000

export OMP_NUM_THREADS=7

#NUM_PROCS_LIST="4"
#the proc number should not be larger than the total number of blocks
#otherwise, there are empty seeds, todo, add this into the program checking
NUM_PROCS_LIST="8 16 32 64"

COMM_PATTERNS="sync async"

for NUM_PROCS in ${NUM_PROCS_LIST}
do

for COMM in ${COMM_PATTERNS}
do

# the NUM_PROCS is 6 for one node
# for 4 processes it needs 11 nodes in total
# refer to 
# https://docs.olcf.ornl.gov/systems/summit_user_guide.html#common-use-cases
# for one resource set, there is 7 cpu cores and one gpu core
jsrun -n $NUM_PROCS -a1 -c7 -bpacked:7 -g1 ./visitReaderAdev \
--vtkm-device openmp \
--file=$DATASET \
--field-name=$FIELD \
--advect-seed-box-extents=0,4,0,4,0,8 \
--seeding-method=boxfixed \
--seeding-sample=20,20,50 \
--advect-num-steps=$NUMSTEPS \
--advect-step-size=0.1 \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf \
--assign-strategy=roundroubin \
--communication=$COMM &> reader.log

# there are 60 blocks, using the continuous strategy can introduce extra overhead

dirname=${COMM}_log_${NUM_PROCS}

mkdir -p $dirname
mv reader.log $dirname
mv timetrace.*.out $dirname
mv counter.*.out $dirname

# copy things back
cp -r $dirname $CURRDIR/$DATA_DIRNAME

done
done