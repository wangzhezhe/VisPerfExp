#!/bin/bash
 
#BSUB -P csc143
#BSUB -W 01:59
#BSUB -nnodes 25

#BSUB -J SL_Inline_mesh256_varyProcs
#BSUB -o R_SL_Inline_mesh256_varyProcs.%J.out
#BSUB -e R_SL_Inline_mesh256_varyProcs.%J.err 

CURRDIR=$(pwd)
DATA_DIRNAME=SL_Inline_mesh256_varyProcs

#rm -r $CURRDIR/$DATA_DIRNAME
mkdir -p $CURRDIR/$DATA_DIRNAME

cd $MEMBERWORK/csc143

rm -rf $DATA_DIRNAME
mkdir $DATA_DIRNAME
cd $DATA_DIRNAME

ln -s $CURRDIR/../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par

# generate config file
# copy them into the current working dir

scriptsDir=$CURRDIR/../../../commonScripts

# it hangs here if the number of process is larger than mesh size
NUM_PROCS_LIST="32 64 128"
NUM_SEEDS_LIST="1000"

for NUM_PROCS in ${NUM_PROCS_LIST}
do

echo "test the procs number ${NUM_PROCS}"

for NUM_SEEDS in ${NUM_SEEDS_LIST}
do

echo "test the seeds number ${NUM_SEEDS}"

# prepare configuration files
# cp it every time since we move it away at the end

cp ${scriptsDir}/clover.in_jet clover.in
sed -i "s/visit_initial_delay=300/visit_initial_delay=800/" clover.in
sed -i "s/end_step=600/end_step=900/" clover.in

sed -i "s/64/256/" clover.in


cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml 
# set the record trajectories as fals to do the particle advecation instead of streamline filter
sed -i "s/record_trajectories: true/record_trajectories: false/" ascent_actions.yaml
sed -i "s/num_seeds: 512/num_seeds: ${NUM_SEEDS}/" ascent_actions.yaml
#sed -i "s/num_steps: 512/num_steps: 1000/" ascent_actions.yaml
sed -i "s/num_steps: 512/num_steps: 1000/" ascent_actions.yaml
sed -i "s/step_size: 0.01/step_size: 0.1/" ascent_actions.yaml
sed -i "s/endstep: 10/endstep: 900/" ascent_actions.yaml

# set bounds of the seeds method

sed -i "s/xmin: 0.0/xmin: 1.5/" ascent_actions.yaml
sed -i "s/xmax: 10.0/xmax: 2.5/" ascent_actions.yaml

sed -i "s/ymin: 0.0/ymin: 1.5/" ascent_actions.yaml
sed -i "s/ymax: 10.0/ymax: 2.5/" ascent_actions.yaml

sed -i "s/zmin: 0.0/zmin: 0.0/" ascent_actions.yaml
sed -i "s/zmax: 10.0/zmax: 6.0/" ascent_actions.yaml

jsrun -n ${NUM_PROCS} ./cloverleaf3d_par &> sim.log

mkdir -p log_${NUM_PROCS}_${NUM_SEEDS}
mv sim.log log_${NUM_PROCS}_${NUM_SEEDS}
mv clover.in log_${NUM_PROCS}_${NUM_SEEDS}
mv ascent_actions.yaml log_${NUM_PROCS}_${NUM_SEEDS}
mv timing.*.out log_${NUM_PROCS}_${NUM_SEEDS}
mv counter*.out log_${NUM_PROCS}_${NUM_SEEDS}

sleep 1

# copy things back
cp -r log_${NUM_PROCS}_${NUM_SEEDS} $CURRDIR/$DATA_DIRNAME
done
done
