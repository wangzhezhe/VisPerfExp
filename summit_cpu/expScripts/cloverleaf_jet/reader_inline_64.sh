#!/bin/bash
 
#BSUB -P csc143
#BSUB -W 01:59
#BSUB -nnodes 32

#BSUB -J reader_inline_64
#BSUB -o R_reader_inline_64.%J.out
#BSUB -e R_reader_inline_64.%J.err 

CURRDIR=$(pwd)
DATA_DIRNAME=reader_inline_64

#rm -r $CURRDIR/$DATA_DIRNAME
mkdir -p $CURRDIR/$DATA_DIRNAME

cd $MEMBERWORK/csc143

rm -rf $DATA_DIRNAME
mkdir $DATA_DIRNAME
cd $DATA_DIRNAME

ln -s $CURRDIR/../../install/visReader/visitReaderAdev visitReaderAdev

#DATASET=../generatedData/x_clover_128_128_256.650.4_4_4.visit
DATASET=/gpfs/alpine/csc143/proj-shared/pugmire/forJay/clover.0700.64.visit
FIELD=mesh_mesh/velocity
SIMTASK=64

NUMSEEDS=1000
NUMSTEPS=1000

COREPERTASK=21
export OMP_NUM_THREADS=21

jsrun -n $SIMTASK -c $COREPERTASK ./visitReaderAdev \
--file=$DATASET \
--field-name=$FIELD \
--advect-seed-box-extents=1.5,2.5,1.5,2.5,0,8.0 \
--advect-num-steps=$NUMSTEPS \
--advect-num-seeds=$NUMSEEDS \
--advect-step-size=0.1 \
--record-trajectories=false \
--output-results=false \
--sim-code=cloverleaf

