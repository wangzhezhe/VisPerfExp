#!/bin/bash
 
#BSUB -P csc143
#BSUB -W 01:59
#BSUB -nnodes 32

#BSUB -J reader_vary_procs_seeds_cpu_32_small
#BSUB -o R_reader_vary_procs_seeds_cpu_32_small.%J.out
#BSUB -e R_reader_vary_procs_seeds_cpu_32_small.%J.err 

CURRDIR=$(pwd)

DATANAME=x_cloverleafRaw_128_128_256.640.4_4_4.128_128_128.visit
DATASETPATH=/gpfs/alpine/proj-shared/csc143/zhewang/datasets/streamlineexp/$DATANAME
DATA_DIRNAME=reader_vary_procs_seeds_cpu_32_small/$DATANAME

#rm -r $CURRDIR/$DATA_DIRNAME
mkdir -p $CURRDIR/$DATA_DIRNAME

cd $MEMBERWORK/csc143

rm -rf $DATA_DIRNAME
mkdir -p $DATA_DIRNAME
cd $DATA_DIRNAME

ln -s $CURRDIR/../../install/visReader/visitReaderAdev visitReaderAdev

FIELD=velocity

NUMSTEPS=1000

COREPERTASK=21
export OMP_NUM_THREADS=21

NUM_PROCS_LIST="2 4 8 16 32 64"
NUM_SEEDS_LIST="1000 100000"

for NUMSEEDS in ${NUM_SEEDS_LIST}
do

for NUM_PROCS in ${NUM_PROCS_LIST}
do


jsrun -n $NUM_PROCS -c $COREPERTASK ./visitReaderAdev \
--file=$DATASET \
--field-name=$FIELD \
--advect-seed-box-extents=1.5,2.5,1.5,2.5,3.0,5.0 \
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
