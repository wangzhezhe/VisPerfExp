#!/bin/bash
 
#BSUB -P csc143
#BSUB -W 01:59
#BSUB -nnodes 2

#BSUB -J FTLE_Intran_mesh64
#BSUB -o R_FTLE_Intran_mesh64.%J.out
#BSUB -e R_FTLE_Intran_mesh64%J.err 

CURRDIR=$(pwd)
DATA_DIRNAME=FTLE_Intran_mesh64_Data

#rm -r $CURRDIR/$DATA_DIRNAME
mkdir -p $CURRDIR/$DATA_DIRNAME

cd $MEMBERWORK/csc143

rm -rf $DATA_DIRNAME
mkdir $DATA_DIRNAME
cd $DATA_DIRNAME

ln -s $CURRDIR/../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par
ln -s $CURRDIR/../../install/visReader/reader reader

# generate config file
# copy them into the current working dir

scriptsDir=$CURRDIR/../../../commonScripts

NUM_SIM_PROC_LIST="16 32"
NUM_SEEDS_LIST="100000 500000 1000000"
NUM_READER_PROC_LIST="2 4 8"

#NUM_PROCS_LIST="16"
#NUM_SEEDS_LIST="100000"
#NUM_SEEDS_LIST="1000000 10000000"
# 1000000 seeds may takes around 1800 seconds, around 0.5 hour

for NUM_READER_PROC in ${NUM_READER_PROC_LIST}
do

echo "test the reader number ${NUM_READER_PROC}"

for NUM_SIM_PROC in ${NUM_SIM_PROC_LIST}
do

echo "test the sim procs number ${NUM_SIM_PROC}"

for NUM_SEEDS in ${NUM_SEEDS_LIST}
do

echo "test the seeds number ${NUM_SEEDS}"

# prepare configuration files
# cp it every time since we move it away at the end
cp ${scriptsDir}/clover.in_jet clover.in

cp ${scriptsDir}/ascent_actions_relay_adios_SST.yaml ascent_actions.yaml
# make it same with the value in clover.in
sed -i "s/endstep: 10/endstep: 600/" ascent_actions.yaml

# this is for fides writer
cp ${scriptsDir}/adios2.xml adios2.xml
# this is for the fides write operation
cp ${scriptsDir}/cloverleaf.json cloverleaf.json

# if use the jet configuration
jsrun -n ${NUM_READER_PROC} ./reader \
--file=out.bp \
--read-method=SST \
--visualization-op=advect \
--seed-method=box \
--advect-seed-box-extents=0,4,0,4,0,8 \
--advect-num-seeds=${NUM_SEEDS} \
--advect-num-steps=20 \
--advect-step-size=0.1 \
--field-name=velocity \
--sst-json-file=./cloverleaf.json &> ./reader.log &

echo "reader started, prepar sim"

echo "start sim, executing"
jsrun -n ${NUM_SIM_PROC} ./cloverleaf3d_par &> sim.log

logdir=log_${NUM_READER_PROC}_${NUM_SIM_PROC}_${NUM_SEEDS}

mkdir -p ${logdir}
mv sim.log ${logdir}
mv reader.log ${logdir}
mv clover.in ${logdir}
mv ascent_actions.yaml ${logdir}
mv timing.*.out ${logdir}
mv counter*.out ${logdir}

sleep 1

# copy things back
cp -r ${logdir} $CURRDIR/$DATA_DIRNAME
done
done
done
