#!/bin/bash
 
#BSUB -P csc143
#BSUB -W 01:59
#BSUB -nnodes 10

#BSUB -J reader_vary_procs_seeds_gpu_ftle
#BSUB -o R_reader_vary_procs_seeds_gpu_ftle.%J.out
#BSUB -e R_reader_vary_procs_seeds_gpu_ftle.%J.err 

CURRDIR=$(pwd)


DATASET=/gpfs/alpine/proj-shared/csc143/zhewang/datasets/streamlineexp/x_cloverleafRaw_128_128_256.640.3_4_5.128_128_128.visit
DATA_DIRNAME=reader_vary_procs_seeds_gpu_ftle_data/x_cloverleafRaw_128_128_256.640.3_4_5.128_128_128


#rm -r $CURRDIR/$DATA_DIRNAME
mkdir -p $CURRDIR/$DATA_DIRNAME

cd $MEMBERWORK/csc143

rm -rf $DATA_DIRNAME
mkdir -p $DATA_DIRNAME
cd $DATA_DIRNAME

ln -s $CURRDIR/../../install/visReader/visitReaderAdev visitReaderAdev

FIELD=velocity

NUMSTEPS=100

COREPERTASK=1

# set GPU backend
export ASCENT_VTKM_BACKEND=cuda

NUM_PROCS_LIST="12 24 36 48 60"

NUM_SEEDS_LIST="1000000"

for NUMSEEDS in ${NUM_SEEDS_LIST}
do

for NUM_PROCS in ${NUM_PROCS_LIST}
do

# refer to https://github.com/olcf-tutorials/jsrun_quick_start_guide
# number of gpu per rs is fixed as 1
jsrun -n $NUM_PROCS -c $COREPERTASK -g1 -a1 ./visitReaderAdev \
--file=$DATASET \
--field-name=$FIELD \
--advect-seed-box-extents=1.5,2.5,1.5,2.5,0,7.9 \
--advect-num-steps=$NUMSTEPS \
--advect-num-seeds=$NUMSEEDS \
--advect-step-size=0.1 \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf &> reader.log

dirname=log_${NUMSEEDS}_${NUMSTEPS}_${NUM_PROCS}

mkdir -p $dirname
mv reader.log $dirname
mv timing.*.out $dirname
mv counter*.out $dirname

# copy things back
cp -r $dirname $CURRDIR/$DATA_DIRNAME

done
done
