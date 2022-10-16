#!/bin/bash
 
#BSUB -P csc143
#BSUB -W 00:59
#BSUB -nnodes 1

#BSUB -J InlineVarySeeds_4_Procs
#BSUB -o R_InlineVarySeeds_4_Procs.%J.out
#BSUB -e R_InlineVarySeeds_4_Procs%J.err 


CURRDIR=$(pwd)
DATA_DIRNAME=InlineVarySeeds_4_Procs_Data

#rm -r $CURRDIR/$DATA_DIRNAME
mkdir -p $CURRDIR/$DATA_DIRNAME

cd $MEMBERWORK/csc143

rm -rf $DATA_DIRNAME
mkdir $DATA_DIRNAME
cd $DATA_DIRNAME

ln -s $CURRDIR/../../../install/ascent/examples/ascent/proxies/cloverleaf3d/cloverleaf3d_par cloverleaf3d_par

# generate config file
# copy them into the current working dir

scriptsDir=$CURRDIR/../../../../commonScripts
cp ${scriptsDir}/clover.in_default clover.in

# large seeds number may take too longtime to execute
sed -i "s/end_step=200/end_step=50/" clover.in

NUM_SEEDS_LIST="1000 10000 100000 1000000 10000000"
#NUM_SEEDS_LIST="1000000 10000000"
# 1000000 seeds may takes around 1800 seconds, around 0.5 hour

for NUM_SEEDS in ${NUM_SEEDS_LIST}
do

echo "test the seeds number ${NUM_SEEDS}"

cp ${scriptsDir}/ascent_actions_streamline_box.yaml ascent_actions.yaml 
sed -i "s/num_seeds: 512/num_seeds: ${NUM_SEEDS}/" ascent_actions.yaml
sed -i "s/record_trajectories: true/record_trajectories: false/" ascent_actions.yaml


jsrun -n 4 ./cloverleaf3d_par &> sim.log

mkdir -p log_$NUM_SEEDS
mv sim.log log_$NUM_SEEDS
mv timing.*.out log_$NUM_SEEDS

# copy things back
cp -r log_$NUM_SEEDS $CURRDIR/$DATA_DIRNAME
done


