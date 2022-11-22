#!/bin/bash
 
#BSUB -P csc143
#BSUB -W 01:59
#BSUB -nnodes 64

#BSUB -J reader_vary_procs_seeds_cpu_syn_streml
#BSUB -o R_reader_vary_procs_seeds_cpu_syn_streml.%J.out
#BSUB -e R_reader_vary_procs_seeds_cpu_syn_streml.%J.err 

CURRDIR=$(pwd)


DATANAME=x_syn_symm_100_100_100.4_4_8.32_32_32.visit
DATASETPATH=/gpfs/alpine/proj-shared/csc143/zhewang/datasets/streamlineexp/$DATANAME
DATA_DIRNAME=reader_vary_procs_seeds_cpu_syn_streml_data/$DATANAME

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

NUM_PROCS_LIST="2 4 8 16 32 64 128"

NUM_SEEDS_LIST="1000 10000 100000"

for NUMSEEDS in ${NUM_SEEDS_LIST}
do

for NUM_PROCS in ${NUM_PROCS_LIST}
do


jsrun -n $NUM_PROCS -c $COREPERTASK ./visitReaderAdev \
--file=$DATASETPATH \
--field-name=$FIELD \
--advect-seed-box-extents=0,96,0,96,0,96 \
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
