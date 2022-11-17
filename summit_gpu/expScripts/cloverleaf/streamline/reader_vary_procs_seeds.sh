#!/bin/bash
 
#BSUB -P csc143
#BSUB -W 01:59
#BSUB -nnodes 32

#BSUB -J reader_vary_procs_seeds
#BSUB -o R_reader_vary_procs_seeds.%J.out
#BSUB -e R_reader_vary_procs_seeds.%J.err 

CURRDIR=$(pwd)
DATA_DIRNAME=reader_vary_procs_seeds_data

#rm -r $CURRDIR/$DATA_DIRNAME
mkdir -p $CURRDIR/$DATA_DIRNAME

cd $MEMBERWORK/csc143

rm -rf $DATA_DIRNAME
mkdir $DATA_DIRNAME
cd $DATA_DIRNAME

ln -s $CURRDIR/../../install/visReader/visitReaderAdev visitReaderAdev

#DATASET=../generatedData/x_clover_128_128_256.650.4_4_4.visit
#DATASET=/gpfs/alpine/csc143/proj-shared/pugmire/forJay/clover.0700.64.visit
DATASET=/gpfs/alpine/proj-shared/csc143/zhewang/datasets/streamlineexp/x_cloverleafRaw_128_128_256.640.3_4_5.visit
FIELD=velocity


NUMSTEPS=1000

COREPERTASK=6

# set GPU backend
export ASCENT_VTKM_BACKEND=cuda

NUM_PROCS_LIST="2 4 6 8 10"

NUM_SEEDS_LIST="1000 10000 100000"

for NUMSEEDS in ${NUM_SEEDS_LIST}
do

for NUM_PROCS in ${NUM_PROCS_LIST}
do


jsrun -n $NUM_PROCS -c $COREPERTASK ./visitReaderAdev \
--file=$DATASET \
--field-name=$FIELD \
--advect-seed-box-extents=1.5,2.5,1.5,2.5,0,8.0 \
--advect-num-steps=$NUMSTEPS \
--advect-num-seeds=$NUMSEEDS \
--advect-step-size=0.1 \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf &> reader.log

dirname=log_${NUMSEEDS}_${NUM_PROCS}

mkdir -p $dirname
mv reader.log $dirname
mv timing.*.out $dirname
mv counter*.out $dirname

# copy things back
cp -r $dirname $CURRDIR/$DATA_DIRNAME

done
done
