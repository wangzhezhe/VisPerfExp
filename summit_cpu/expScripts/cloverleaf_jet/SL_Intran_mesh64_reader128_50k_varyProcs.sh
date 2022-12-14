#!/bin/bash
 
#BSUB -P csc143
#BSUB -W 01:59
#BSUB -nnodes 28

#BSUB -J SL_Intran_mesh64_reader128_50k_varyProcs
#BSUB -o R_SL_Intran_mesh64_reader128_50k_varyProcs.%J.out
#BSUB -e R_SL_Intran_mesh64_reader128_50k_varyProcs.%J.err 

CURRDIR=$(pwd)
DATA_DIRNAME=SL_Intran_mesh64_reader128_50k_varyProcs_Data

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

NUM_SIM_PROC_LIST="1024 512 256 128"
NUM_SEEDS_LIST="50000"
NUM_READER_PROC_LIST="128"

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
sed -i "s/end_step=600/end_step=460/" clover.in
sed -i "s/visit_initial_delay=300/visit_initial_delay=450/" clover.in

cp ${scriptsDir}/ascent_actions_relay_adios_SST.yaml ascent_actions.yaml
# make it same with the value in clover.in
sed -i "s/endstep: 10/endstep: 460/" ascent_actions.yaml

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
--advect-seed-box-extents=1.5,2.5,1.5,2.5,0,8.0 \
--advect-num-seeds=${NUM_SEEDS} \
--advect-num-steps=1000 \
--record-trajectories=false \
--advect-step-size=0.1 \
--field-name=velocity \
--record-trajectories=false \
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
